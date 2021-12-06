from typing import Optional
import uvicorn

from fastapi import FastAPI, Header

from utils.auth import auth_decorator


app = FastAPI()


@app.on_event("startup")
async def startup():
    from core.es_client import connect_elasticsearch

    connect_elasticsearch()


@app.on_event('shutdown')
async def shutdown():
    from core.es_client import close_elasticsearch

    close_elasticsearch()


@app.get("/search")
@auth_decorator
def search(session_token: Optional[str] = Header(None)):
    pass


@app.get("/export")
@auth_decorator
def export(session_token: Optional[str] = Header(None)):
    return "Hello World!"


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
