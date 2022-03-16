# standard imports
import os 

# library imports
from dotenv import load_dotenv
import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from app.document_view import show_document_view
from app.sdg_view import show_sdg_view

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

st.sidebar.write(conn.echo())
st.sidebar.markdown("check out this [link](http://localhost:8501?sdg=1.2)")

def show_default_view():
    st.title('Default')

def show_entity_page(entity_id):
    st.title(f'Entity {entity_id}')
#
# For this hackathon project the Streamlit app will render a 
# small number of views based on the incoming query parameters.
#   Document View:  ?doc=3649ae7f73d8cabf69d27e91ae7b28d6d6def898b0d8ffb21c38f4d6f8387308
#
#   SDG View:       ?sdg=3.2
#
#   Entity View:    ?entity=121d4a17a8a9f4048b1898d482b368a303e13bf2e9a9166a36ae0d836be8804f
#
#   Default View:   0 or >1 Params (i.e. if URL has both ?doc=XXXX&sdg=Y.Z show the default)
query_parameters = st.experimental_get_query_params()

if len(query_parameters) == 0 or len(query_parameters) > 1:
    show_default_view()

elif 'doc' in query_parameters:
    show_document_view(conn, query_parameters['doc'][0], 25)

elif 'sdg' in query_parameters:
    show_sdg_view(conn, query_parameters['sdg'][0], 25)







