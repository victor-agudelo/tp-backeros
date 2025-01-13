from typing import Any, Optional, Dict
from starlette.exceptions import HTTPException as StarletteHTTPException


class InvalidRequest(StarletteHTTPException):
    def __init__(
        self,
        status_code: int = 400,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        fund_name: Optional[str] = None
    ):
        if not detail:
            detail = f'No es posible realizar la operación'
        super().__init__(status_code=status_code, detail=detail, headers=headers)