from fastapi import FastAPI

from app.api import auth, categories, products, users
from app.core.error import ErrorMiddleware

app = FastAPI(title="Techly Marketplace(Backend)")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(auth.router)
app.add_middleware(ErrorMiddleware)
