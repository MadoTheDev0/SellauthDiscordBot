from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    event = data.get("event", "unbekannt")
    print(f"📩 Webhook Event: {event}")
    print(f"📦 Payload: {data}")
    return {"status": "erhalten"}
