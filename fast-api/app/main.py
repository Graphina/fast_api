from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from ddtrace import patch, config

from .router import router
from .errors import unicorn_exception_handler, UnicornException
from .middleware import add_process_time_header

patch(fastapi=True,logging=True)
app = FastAPI()

config.fastapi['service_name'] = 'fast-api-test'
config.fastapi['span_name'] = 'fast-api-test-request'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProxyHeadersMiddleware)
# app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)

app.add_exception_handler(UnicornException, handler=unicorn_exception_handler)

app.include_router(router)

@app.get("/fast-api")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup():
    print("do stufwdwdf")