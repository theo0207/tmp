import uvicorn

from typing import Optional
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from core.auth import verify_token
from core.es_client import es
from core.config import config


app = FastAPI()


# ip whitelist
# @app.middleware("http")
# async def check_ip(request: Request, call_next):
#     if request.client.host not in config.ip_whitelist:
#         return JSONResponse(status_code=403, content={'reason': "IP address rejected"})
    
#     response = await call_next(request)
    
#     return response


@app.on_event("startup")
def startup():
    from core.es_client import connect_elasticsearch

    connect_elasticsearch()


@app.on_event('shutdown')
def shutdown():
    from core.es_client import close_elasticsearch

    close_elasticsearch()


@app.post("/search", dependencies=[Depends(verify_token)])
def search():
    pit_id = es.client.open_point_in_time(index=config.index_name, keep_alive="5m")['id']
    body = {
        "params": {
            "from": 0,
            "size": 10000,
        }
    }
    template = es.client.render_search_template(id="search-template", body=body)
    query = template['template_output']['query']
    pit = {
        "id":  pit_id, 
        "keep_alive": "5m"
    }


    registerd = None
    shard_doc = None
    search_after = None
    response = []

    while True:
        if registerd and shard_doc:
            search_after = [registerd, shard_doc]

        result = es.client.search(query=query, size=10, pit=pit, sort={"registered":{"order":"desc"}}, 
                                search_after=search_after)
        hits = result['hits']['hits']

        if not hits:
            break

        registerd, shard_doc = hits[-1]['sort']

        for doc in hits:
            del doc['sort']
            response.append(doc)
    
    return response


@app.post("/export", dependencies=[Depends(verify_token)])
def export():
    pass


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
