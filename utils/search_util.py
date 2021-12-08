from core.es_client import es
from core.config import config


def get_pit():
    pit_id = es.client.open_point_in_time(index=config.index_name, keep_alive="5m")['id']
    pit = {
        "id":  pit_id, 
        "keep_alive": "5m"
    }
    return pit

def get_query_from_template(**kwargs):
    template_body = {
        "params": {
            "from": kwargs['from_'],
            "size": kwargs['size'],
            "search_fied": kwargs['search_field'],
            "search_keyword": kwargs['search_keyword'],
            "sort_field": kwargs['sort_field'],
            "order": kwargs['order']
        }
    }

    template = es.client.render_search_template(id="search-template", body=template_body)
    return template['template_output']['query']

def pagenated_search(pit, query):
    response = []

    registerd = None
    shard_doc = None
    search_after = None

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