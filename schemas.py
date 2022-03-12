from typing import Optional
from pydantic import BaseModel


class CreateCustomerParams(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]