import os
import uvicorn

from fastapi import FastAPI, Depends, Request, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.background import BackgroundTasks

from core.auth import verify_token
from core.config import config
from models.reqeusts import ExportReqeust, SearchRequest
from utils.search_util import get_pit, get_query_from_template, pagenated_search
from utils.export_util import save_data_to_excel_file


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
def search(request: SearchRequest=None):
    request = request.dict()
    pit = get_pit()
    query = get_query_from_template(**request)
    response = pagenated_search(pit, query)

    return response


@app.post("/export")
def export(background_tasks: BackgroundTasks, request:ExportReqeust=None, id:int = Depends(verify_token)):
    request = request.dict()
    pit = get_pit()
    query = get_query_from_template(**request)
    docs = pagenated_search(pit, query)

    columns = request['columns']
    save_data_to_excel_file(columns, docs, id)

    file_path = config.excel_file_path+f'{id}.xlsx'
    background_tasks.add_task(os.remove, file_path)

    return FileResponse(file_path)




if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
