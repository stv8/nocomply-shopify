from typing import Optional
from pydantic import BaseModel


class CreateCustomerParams(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address1: str
    address2: Optional[str]
    city: str
    state: str
    zip: str