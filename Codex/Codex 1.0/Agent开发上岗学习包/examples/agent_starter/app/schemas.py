from pydantic import BaseModel, Field
class PermissionContext(BaseModel):
    user_id: str
    tenant_id: str
    roles: set[str] = Field(default_factory=set)
    permissions: set[str] = Field(default_factory=set)
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    tenant_id: str = Field(min_length=2, max_length=64)
class ChatResponse(BaseModel):
    run_id: str
    status: str
    answer: str | None = None
    error: str | None = None
