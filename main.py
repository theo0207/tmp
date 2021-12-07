import uvicorn

from typing import Optional
from fastapi import FastAPI, Depends

from utils.auth import verify_token


app = FastAPI()


@app.on_event("startup")
async def startup():
    from core.es_client import connect_elasticsearch

    connect_elasticsearch()


@app.on_event('shutdown')
async def shutdown():
    from core.es_client import close_elasticsearch

    close_elasticsearch()


@app.get("/search", dependencies=[Depends(verify_token)])
def search():
    pass


@app.get("/export", dependencies=[Depends(verify_token)])
def export():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
