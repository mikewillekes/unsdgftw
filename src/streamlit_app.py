# standard imports
import os 

# library imports
from dotenv import load_dotenv
import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config

load_dotenv()

#
# Connect to tgcloud.io instance
#
# Note: on TG Free Tier - the running solution is automatically stopped after ~1hr of idle.
#       Make sure it's actually running before freaking out about connections errors
#
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}',
    username=f'{os.environ.get("tg_username")}',
    password=f'{os.environ.get("tg_password")}',
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

st.write(conn.echo())

results = conn.getInstalledQueries()

#results = conn.runInstalledQuery('Document_Expansion', {'doc': '3649ae7f73d8cabf69d27e91ae7b28d6d6def898b0d8ffb21c38f4d6f8387308', 'max_results' : 5})
results = conn.runInstalledQuery('SDG_Expansion', {'sdg': '3.3', 'max_results' : 10})

st.write(results)