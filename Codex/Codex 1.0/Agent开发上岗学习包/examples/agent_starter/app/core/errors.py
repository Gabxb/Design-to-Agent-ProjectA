class AppError(Exception):
    def __init__(self, code: str, *, retryable: bool = False):
        self.code, self.retryable = code, retryable
        super().__init__(code)
class ToolExecutionError(AppError): pass
class PermissionDenied(AppError): pass
class AgentLimitError(AppError): pass
