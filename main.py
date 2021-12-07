import uvicorn

from typing import Optional
from fastapi import FastAPI, Depends

from utils.auth import verify_token
from core.es_client import es


app = FastAPI()


@app.on_event("startup")
async def startup():
    from core.es_client import connect_elasticsearch

    connect_elasticsearch()


@app.on_event('shutdown')
async def shutdown():
    from core.es_client import close_elasticsearch

    close_elasticsearch()


@app.post("/search", dependencies=[Depends(verify_token)])
def search():
    body = {
        "params": {
            "condition": False,
            "query_string": "hello world",
            "from": 20,
            "size": 10
        }
    }
    template = es.client.render_search_template(id="my-search-template", body=body)
    query = template['template_output']['query']
    es.client.search(index="some_index", query=query)


@app.post("/export", dependencies=[Depends(verify_token)])
def export():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
