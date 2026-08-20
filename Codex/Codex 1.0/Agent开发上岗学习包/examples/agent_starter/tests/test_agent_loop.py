import pytest
from app.agent.loop import AgentRunner,AgentConfig
from app.agent.state import AgentState
from app.agent.tools import ToolCall,ToolDef,ToolRegistry,TicketLookupArgs
from app.llm.base import ModelDecision
from app.schemas import PermissionContext
class FakeModel:
    def __init__(self): self.n=0
    async def decide(self,*,state,tool_schemas):
        self.n+=1
        if self.n==1: return ModelDecision(kind="tool",tool_call=ToolCall("ticket_lookup",{"ticket_id":"T-1"}))
        return ModelDecision(kind="final",text="done")
@pytest.mark.asyncio
async def test_agent_executes_tool_then_finishes():
    tools=ToolRegistry()
    async def lookup(args,ctx): return {"ticket_id":args.ticket_id,"tenant_id":ctx.tenant_id}
    tools.register(ToolDef("ticket_lookup","read ticket",TicketLookupArgs,lookup))
    state=AgentState.new("hello",PermissionContext(user_id="u1",tenant_id="acme"))
    result=await AgentRunner(FakeModel(),tools,AgentConfig(max_steps=4)).run(state)
    assert result.status=="completed"
    assert result.observations[0]["result"]["tenant_id"]=="acme"
