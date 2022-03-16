import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config


def show_document_view(conn, document_id, max_results):
    st.title(f'Document {document_id}')
    results = conn.runInstalledQuery('Document_Expansion', {'doc': document_id, 'max_results' : max_results})
    st.write(results)