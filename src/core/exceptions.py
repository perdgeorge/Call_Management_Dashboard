class CallBaseException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class CallNotFoundError(CallBaseException):
    def __init__(
        self,
        call_id: int,
    ):
        super().__init__(
            message=f"Call with ID:{call_id} not found",
            error_code="Call Not Found",
            status_code=404,
        )
