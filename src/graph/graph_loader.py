import os
import json
from dotenv import load_dotenv
import pyTigerGraph as tg

# Local application imports
from config import config
from graph import graph_config

load_dotenv()

# Connect and built schema
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}', 
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

print(conn.echo())


def main():
    load_graph_data('IUCN')


def load_graph_data(document_collection_name):

    res = conn.uploadFile(
        f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.CORPUS_NODES}', 
        fileTag='MyDataSource',
        jobName='load_job_corpus_nodes_csv')
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
