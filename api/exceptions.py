class ApiException(Exception):
    def __init__(self, status_code: int, response_bytes: bytes):
        super().__init__(
            f"Request error code: {status_code}: {response_bytes!r}"
        )
        self.status_code = status_code
        self.response_bytes = response_bytes
