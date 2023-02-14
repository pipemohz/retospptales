from pydantic import BaseModel, Extra
from typing import Optional, TypedDict
from datetime import datetime as dt


class BaseValidator(BaseModel, extra=Extra.forbid):
    id: int
    month: Optional[int] = dt.now().month
    year: Optional[int] = dt.now().year


class ProductValidator(TypedDict):
    code: int
    value: int


class CommissionsValidator(BaseValidator):
    products: list[ProductValidator]
