import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config


def show_sdg_view(conn, sdg_id, max_results):
    st.title(f'SDG {sdg_id}')
    results = conn.runInstalledQuery('SDG_Expansion', {'sdg': sdg_id, 'max_results' : max_results})
    st.write(results)