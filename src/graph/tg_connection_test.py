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

conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_address")}', 
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

#
# Note: on TG Free Tier - the running solution is automatically stopped after ~1hr of idle.
#       Make sure it's actually running before freaking out about connections errors
#
results = conn.getEndpoints()
print(results)