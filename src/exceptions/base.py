from abc import ABC

class ClientErrorBase(ABC, Exception):
    _status_code: int
    _message: str

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message

class InvalidOperationError(ClientErrorBase):
    _status_code = 400

class AuthenticationError(ClientErrorBase):
    _status_code = 401

class ResourceNotFoundError(ClientErrorBase):
    _status_code = 404
