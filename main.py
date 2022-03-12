from typing import Optional

from fastapi import FastAPI, Response, status
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import shopify
from config import get_config

from schemas import CreateCustomerParams


config = get_config()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

shop_url = config.SHOP_URL
access_token = config.ACCESS_TOKEN
api_version = "2022-01"


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/customers")
def create_customer(response: Response, params: CreateCustomerParams):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer = shopify.Customer()
    customer.first_name = params.first_name
    customer.last_name = params.last_name
    customer.email = params.email
    # customer.phone = params.phone
    success = customer.save()
    shopify.ShopifyResource.clear_session()

    if not success:
        print(customer.errors.full_messages())
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": customer.errors.full_messages()}

    return {"status": "ok"}


@app.get("/customers")
def get_customer(email: str):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer = shopify.Customer().find(email=email)
    if not customer:
        print(customer.errors.full_messages())
    else:
        [print(c.verified_email) for c in customer]

    shopify.ShopifyResource.clear_session()
    return {"status": "ok"}


kwargs = {"host": "0.0.0.0", "port": 9000, "reload": True}

if __name__ == "__main__":
    uvicorn.run("main:app", **kwargs)
