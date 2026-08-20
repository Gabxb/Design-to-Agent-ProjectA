from __future__ import annotations
import json
from openai import AsyncOpenAI
from app.llm.base import ModelDecision
from app.agent.tools import ToolCall
class OpenAIResponsesClient:
    def __init__(self, api_key: str, model: str, timeout_s: float = 30.0):
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout_s, max_retries=2)
        self.model = model
    async def decide(self, *, state, tool_schemas):
        tools=[{"type":"function","name":s["name"],"description":s["description"],"parameters":s["parameters"],"strict":True} for s in tool_schemas]
        response=await self.client.responses.create(model=self.model,input=state.as_model_input(),tools=tools)
        for item in response.output:
            if getattr(item,"type",None)=="function_call":
                return ModelDecision(kind="tool", tool_call=ToolCall(name=item.name, arguments=json.loads(item.arguments)))
        return ModelDecision(kind="final", text=response.output_text or "")
