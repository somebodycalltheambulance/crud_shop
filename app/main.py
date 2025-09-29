from fastapi import FastAPI

from app.api import categories, products, users
from app.core.config import settings

app = FastAPI(title="Techly Marketplace(Backend)")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)

safe = settings.database_url
safe = safe.replace(safe.split("@")[0], "//***:***")
print(f"[DB_URL] {safe}")
