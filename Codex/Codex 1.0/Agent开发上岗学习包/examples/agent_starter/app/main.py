from fastapi import FastAPI, Header, HTTPException
from app.core.logging import configure_logging
from app.schemas import ChatRequest, ChatResponse, PermissionContext
from app.agent.state import AgentState
configure_logging(); app=FastAPI(title="Agent Starter")
@app.get("/health")
def health(): return {"ok":True}
@app.post("/chat",response_model=ChatResponse)
async def chat(req:ChatRequest, x_user_id:str=Header(default="demo")):
    if req.tenant_id=="forbidden": raise HTTPException(403,"tenant denied")
    state=AgentState.new(req.message,PermissionContext(user_id=x_user_id,tenant_id=req.tenant_id))
    # Demo endpoint: wiring a real ModelClient/ToolRegistry is intentionally application-specific.
    state.status="completed"; state.final_answer="starter ready; wire AgentRunner in your service layer"
    return ChatResponse(run_id=state.run_id,status=state.status,answer=state.final_answer)
