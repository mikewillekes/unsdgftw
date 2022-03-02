import os 
from dotenv import load_dotenv
import pyTigerGraph as tg

load_dotenv()

#
# Here's how to get the API token from the Secret
# See: https://colab.research.google.com/drive/1sYv3Jvc6KYsqC4D-Rxkvjh4iPnrp4rg7
#
#graph = tg.TigerGraphConnection(host='os.environ.get("tg_graphname")', graphname='SDGs')
#auth_token = graph.getToken('GET_IT_FROM_1PASSWORD')
#print(auth_token)

graph = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_address")}', 
    graphname=f'{os.environ.get("tg_graphname")}', 
    apiToken=f'{os.environ.get("tg_token")}')

#
# Note: on TG Free Tier - the running solution is automatically stopped after ~1hr of idle.
#       Make sure it's actually running before freaking out about connections errors
#
results = graph.getEndpoints()
print(results)