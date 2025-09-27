from fastapi import FastAPI

app = FastAPI(title="Techly Marketplace")


@app.get("/health")
async def health():
    return {"status": "ok"}
