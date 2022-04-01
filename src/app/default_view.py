import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_default_view(conn):

    sdgs = preload_sdgs()
    
    write_sidebar_stats(conn)


@st.cache
def preload_sdgs():
    # Return a Dictionary of SDGs
    return dict([(sdg.goal_num, sdg) for sdg in load_sdgs()])


@st.cache
def get_summary_stats(conn):
    results = conn.runInterpretedQuery(f'''
    INTERPRET QUERY () FOR GRAPH {config.GRAPH_NAME} {{ 

    MapAccum<STRING, INT> @@graphStatsAccum;
    results = SELECT d
                FROM Corpus:c -()- Document:d
                ACCUM
                    @@graphStatsAccum += (c.sourceURL -> 1);

    PRINT @@graphStatsAccum;
    }}
    ''')
    return results[0]['@@graphStatsAccum']


def write_sidebar_stats(conn):

    stats = get_summary_stats(conn)

    # Write summary results into Sidebar
    st.sidebar.title('Datasets')
    for k,v in stats.items():
        st.sidebar.markdown(k)
        st.sidebar.markdown(f'- {v} documents')
        st.sidebar.markdown('----------')

