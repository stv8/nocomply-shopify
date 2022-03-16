import uvicorn
import shopify

from typing import Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

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


app.mount("/", StaticFiles(directory="static/src", html=True), name="static")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/customers")
def create_customer(request: Request, response: Response, params: CreateCustomerParams):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer = shopify.Customer()
    customer.first_name = params.first_name
    customer.last_name = params.last_name
    customer.email = params.email
    customer.phone = params.phone

    address = shopify.Address()
    address.address1 = params.address1
    address.address2 = params.address2
    address.city = params.city
    address.province = params.state
    address.zip = params.zip
    address.country = "US"
    address.default = True

    customer.addresses = [address]
    success = customer.save()
    shopify.ShopifyResource.clear_session()

    # success = True
    if not success:
        print(customer.errors.full_messages())
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": customer.errors.full_messages()}

    if request.headers.get('HX-Request'):
        return HTMLResponse(content="<div>Success!</div>", status_code=200)

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


kwargs = {"host": "0.0.0.0", "port": 9000, "reload": config.RELOAD}

if __name__ == "__main__":
    uvicorn.run("main:app", **kwargs)
