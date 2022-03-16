import uvicorn
import shopify

from typing import Optional
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from config import get_config
from schemas import CreateCustomerParams
import shopify_patch


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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/customers")
def create_customer_route(
    request: Request, response: Response, params: CreateCustomerParams
):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    customer = shopify.Customer().find_first(email=params.email, phone=params.phone)
    if not customer:
        print("missing customer")
        customer = shopify.Customer()
        customer.email = params.email
        customer.phone = params.phone

    customer.first_name = params.first_name
    customer.last_name = params.last_name

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

    if request.headers.get("HX-Request"):
        return HTMLResponse(content="<div>Success!</div>", status_code=200)

    return {"status": "ok"}


@app.get("/customers")
def get_customer_route(email: str, phone: str):
    customer = get_customer(email, phone)
    return {"status": "ok", "customer": { "name": customer.first_name }}


def get_customer(email: str, phone: str):
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    # there could be multiple customers with email via find()
    try:
        # try email first then phone
        customer = shopify.Customer().find_first(email=email, phone=phone)
        if not customer:
            shopify.ShopifyResource.clear_session()
            return None
        else:
            # [print(c.verified_email) for c in customer]
            print(customer.first_name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="derp")
    finally:
        shopify.ShopifyResource.clear_session()

    return customer


app.mount("/", StaticFiles(directory="static/src", html=True), name="static")

kwargs = {"host": "0.0.0.0", "port": 9000, "reload": config.RELOAD}

if __name__ == "__main__":
    uvicorn.run("main:app", **kwargs)
