from elasticsearch import Elasticsearch

from core.logging import logger
from core.config import config

class ElasticsearchClient:
    client: Elasticsearch = None


es = ElasticsearchClient()

def connect_elasticsearch():
    es.client = Elasticsearch(config.elasticsearch_url,
                                Timeout=30,
                                max_retries=10,
                                retry_on_timeout=True)
    logger.info(f'Connected to Elasticsearch')


def close_elasticsearch():
    if es.client is not None:
        es.client.close()
        logger.info('Closed connect to Elasticsearch')
