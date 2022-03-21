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

results = conn.runInstalledQuery('Document_Expansion', {'doc': '3649ae7f73d8cabf69d27e91ae7b28d6d6def898b0d8ffb21c38f4d6f8387308', 'max_results' : 5})

results = conn.runInstalledQuery('SDG_Expansion', {'sdg': '3.3', 'max_results' : 5})

print(results)