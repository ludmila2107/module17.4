from fastapi import FastAPI
from user import router  # Импортируем маршруты

app = FastAPI()

app.include_router(router, prefix="/users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)