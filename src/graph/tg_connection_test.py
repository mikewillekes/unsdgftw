import os 
from dotenv import load_dotenv
import pyTigerGraph as tg

# Local application imports
from config import config

load_dotenv()

#
# Here's how to get the API token from the Secret
# See: https://colab.research.google.com/drive/1sYv3Jvc6KYsqC4D-Rxkvjh4iPnrp4rg7
#
#conn = tg.TigerGraphConnection(host='os.environ.get("tg_graphname")', graphname='SDGs')
#auth_token = conn.getToken('GET_IT_FROM_1PASSWORD')
#print(auth_token)

# Connect and built schema
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}',
    username=f'{os.environ.get("tg_username")}',
    password=f'{os.environ.get("tg_password")}',
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

print(conn.echo())

#
# Note: on TG Free Tier - the running solution is automatically stopped after ~1hr of idle.
#       Make sure it's actually running before freaking out about connections errors
#
results = conn.getInstalledQueries()
print(results)

#results = conn.runInstalledQuery('Document_Expansion', {'doc': '3649ae7f73d8cabf69d27e91ae7b28d6d6def898b0d8ffb21c38f4d6f8387308', 'max_results' : 5})
#print(results)

#results = conn.runInstalledQuery('SDG_Expansion', {'sdg': '3.3', 'max_results' : 5})
#print(results)

# https://docs.tigergraph.com/tigergraph-server/current/api/built-in-endpoints#_run_an_installed_query_post
#results = conn.runInstalledQuery('tg_louvain', params='v_type=Paragraph')

#results = conn.runInstalledQuery('tg_louvain', params='v_type=Paragraph&v_type=Topic&v_type=Mention&v_type=Entity&v_type=Sentence&v_type=SDG&e_type=has_topic&e_type=has_mention&e_type=has_entity&e_type=has_sentence&e_type=is_similar')


#results = conn.runInstalledQuery('tg_louvain', {'v_type': ['Paragraph', 'Topic', 'Mention', 'Entity', 'Sentence', 'SDG'], 'e_type': ['has_topic', 'has_mention', 'has_entity', 'has_sentence', 'is_similar'], 'wt_attr': '', 'max_iter': 10, 'result_attr': '', 'file_path': '', 'print_info': False})

params = {
    'v_type': ['Entity'],
    'e_type': 'co_mention',
    'wt_attr': 'weight',
    'max_iter': 10,
    'output_limit': 100,
    'print_accum': True,
    'attr': 'lid'
}

#results = conn.runInstalledQuery('tg_label_prop', params, usePost=True)

#results = conn.runInstalledQuery('tg_label_prop', params={'v_type': ['Entity','Topic','SDG'], 'e_type': 'co_mention'})


#results = conn.runInstalledQuery('tg_label_prop', params='v_type=Entity&v_type=Topic&e_type=co_mention')

results = conn.runInstalledQuery('tg_label_prop', params='v_type=Entity&v_type=Topic&v_type=SDG&e_type=co_mention&wt_attr=weight&max_iter=30&output_limit=100&print_accum=true&attr=lid')


print(results)

