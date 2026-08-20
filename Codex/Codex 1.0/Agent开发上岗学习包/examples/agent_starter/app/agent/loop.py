from __future__ import annotations
import asyncio, hashlib, json
from dataclasses import dataclass
from app.agent.state import AgentState
from app.agent.tools import ToolRegistry
from app.core.errors import AgentLimitError, ToolExecutionError
from app.llm.base import ModelClient
@dataclass(frozen=True)
class AgentConfig:
    max_steps: int=8; model_timeout_s: float=30.0; tool_timeout_s: float=15.0
class AgentRunner:
    def __init__(self, model:ModelClient, tools:ToolRegistry, config:AgentConfig|None=None): self.model,self.tools,self.config=model,tools,config or AgentConfig()
    async def run(self,state:AgentState)->AgentState:
        seen:set[str]=set()
        for step in range(self.config.max_steps):
            state.step=step+1
            decision=await asyncio.wait_for(self.model.decide(state=state,tool_schemas=self.tools.schemas()),timeout=self.config.model_timeout_s)
            if decision.kind=="final": state.final_answer=decision.text or ""; state.status="completed"; return state
            if decision.kind!="tool" or decision.tool_call is None: state.status="failed"; state.error="invalid_model_decision"; return state
            call=decision.tool_call
            fp=hashlib.sha256(f"{call.name}:{json.dumps(call.arguments,sort_keys=True,ensure_ascii=False)}".encode()).hexdigest()
            if fp in seen: state.status="failed"; state.error="repeated_tool_call"; return state
            seen.add(fp)
            try: result=await asyncio.wait_for(self.tools.execute(call,state.permission_context),timeout=self.config.tool_timeout_s)
            except asyncio.TimeoutError as exc: raise ToolExecutionError("tool_timeout",retryable=True) from exc
            state.observations.append({"tool":call.name,"result":result})
        raise AgentLimitError(f"max_steps_exceeded:{self.config.max_steps}")
