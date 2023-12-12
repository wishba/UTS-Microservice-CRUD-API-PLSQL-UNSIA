from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def HOME():
  return "Selamat Datang"