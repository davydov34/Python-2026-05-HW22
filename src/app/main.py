import uvicorn
from fastapi import Depends, FastAPI, Request

from src.app.database.db import increase_http_counter
from src.app.endpoints.admin.routes import router as r_admin
from src.app.endpoints.auth.routes import router as r_auth
from src.app.endpoints.me.routes import router as r_me
from src.app.endpoints.predict.routes import router as r_predict
from src.app.logger_app.app_logger import logger as to_log

app = FastAPI(title="ONNX diabetes model with JWT")


@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    to_log.info(
        f"Method: {request.method} | "
        f"Path: {request.url.path} | "
        f"Status: {response.status_code}"
    )
    increase_http_counter()
    return response


@app.get("/")
def root():
    return {"message": "Добро пожаловать, Пользователь"}


app.include_router(r_auth)
app.include_router(r_predict)
app.include_router(r_admin)
app.include_router(r_me)


def main():
    to_log.info("Приложение запущено...")
    uvicorn.run(app="src.app.main:app", host="0.0.0.0", port=8100, reload=True)
    to_log.info("Приложение остановлено...")
