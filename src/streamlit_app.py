# standard imports
from linecache import cache
import os 
from PIL import Image

# library imports
from dotenv import load_dotenv
import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from app.default_view import show_default_view
from app.document_view import show_document_view
from app.sdg_view import show_sdg_view
from app.entity_view import show_entity_view

@st.cache
def load_sdg_images():
    images = {}
    images['1'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-01.png')
    images['2'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-02.png')
    images['3'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-03.png')
    images['4'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-04.png')
    images['5'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-05.png')
    images['6'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-06.png')
    images['7'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-07.png')
    images['8'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-08.png')
    images['9'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-09.png')
    images['10'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-10.png')
    images['11'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-11.png')
    images['12'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-12.png')
    images['13'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-13.png')
    images['14'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-14.png')
    images['15'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-15.png')
    images['16'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-16.png')
    images['17'] = Image.open(f'{config.SDG_IMAGES_FOLDER}/E-WEB-Goal-17.png')
    return images


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

st.set_page_config(
    page_title=f'Sustainable Development Goals',
    page_icon=':earth_africa:',
    layout='wide',
    initial_sidebar_state='auto')



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

images = load_sdg_images()

if len(query_parameters) == 0 or len(query_parameters) > 1:
    show_default_view(conn)

elif 'doc' in query_parameters:
    show_document_view(conn, query_parameters['doc'][0])

elif 'sdg' in query_parameters:
    show_sdg_view(conn, query_parameters['sdg'][0], 25, images)

elif 'entity' in query_parameters:
    show_entity_view(conn, query_parameters['entity'][0], 25, images)



