# No-Comply/SXSW Shopify Registration Form

## About
A small site which can register a customer to a shopify account. This was used specifically to help [No-Comply SkateShop](https://nocomplyatx.com/)
register users in line for a Vans shoe release SXSW event.

The back end is generic and can be used to point to any shopify account by setting the `SHOP_URL` and `ACCESS_TOKEN` env vars.

### Stack
* [FastAPI](https://fastapi.tiangolo.com/)
* [HTMX](https://htmx.org/)
* [Water.css](https://watercss.kognise.dev/)
* Deployed via Digital Ocean Apps

### Some helpful things

#####  Handle Shopify 429 Limit
Shopify limits base account `/admin` API calls to 2 reqs/second. This small gist can be used to add basic retry logic if you are rate limited.
https://gist.github.com/wowkin2/079844c867a1a06ce15ea1e4ffdee8e
