from nbformat import current_nbformat
import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_default_view(conn):
       
    sdgs = preload_sdgs()
    
    write_sidebar_stats(conn)

    homepage_results = preload_homepage_query(conn, 10)
    sdgs_centrality = extract_sdg_centrality_scores(homepage_results)

    st.header('Explore Sustainable Development Goals')
    st.markdown(f'''
        - :high_brightness::high_brightness::high_brightness::high_brightness::high_brightness: Very highly connected to other SDGs, Entitys and Topics
        - :high_brightness::high_brightness::high_brightness::high_brightness: Highly connected to other SDGs, Entitys and Topics
        - :high_brightness::high_brightness::high_brightness: Medium number of connections to other SDGs, Entitys and Topics
        - :high_brightness::high_brightness: Medium-low number of connections to other SDGs, Entities and Topics
        - :high_brightness: Minimal connections to other SDGs, Entities and Topics
        - No connections to other SDGs, Entities or Topics
    
    ''')
    current_group = '##### 1. No Poverty'
    st.markdown(current_group)  
    st.caption('Click to explore any Sustainable Development Goal')
    for key, value in sdgs.items():

        #
        # Display Headings
        #
        next_group = f'##### {value.goal_category_num}. {value.goal_category_short}'
        if next_group != current_group:
            current_group = next_group
            st.markdown(current_group)
            st.caption('Click to explore any Sustainable Development Goal')
        
        score = calculate_sdg_score(sdgs_centrality[value.goal_num])
        st.markdown(f'''-  [{echo_sdg_score_emoji(':high_brightness:', score)} {value.goal_num}](./?sdg={value.goal_num}) {value.goal}''')
   

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


@st.cache
def get_page_count(conn):
    results = conn.runInterpretedQuery(f'''
    INTERPRET QUERY () FOR GRAPH {config.GRAPH_NAME} {{ 
    
    MaxAccum<INT> @maxPage;
    res = SELECT d 
            FROM Document:d -()- Paragraph:p
            ACCUM
                d.@maxPage += p.pageNumber;
            
    SumAccum<INT> @@totalPages;
    res = SELECT c 
            FROM Corpus:c -()- Document:d
            ACCUM
                @@totalPages += d.@maxPage;
    
    PRINT @@totalPages;
    }}
    ''')
    return results[0]['@@totalPages']


@st.cache
def preload_homepage_query(conn, max_results):
    return conn.runInstalledQuery('Homepage', {'max_results' : max_results})


def write_sidebar_stats(conn):

    stats = get_summary_stats(conn)
    pages = get_page_count(conn)

    # Write summary results into Sidebar
    st.sidebar.header(f'Data Sources')
    st.sidebar.caption(f'Exploring {pages} pages from {sum(stats.values())} documents from these sources')
    st.sidebar.markdown('\n'.join([f'- {k}' for k in stats.keys()]))


def extract_sdg_centrality_scores(homepage_results):
    return dict([(sdg['v_id'], sdg['attributes']['cent']) for sdg in homepage_results[0]['(SDGs)']])


def calculate_sdg_score(centrality_score):
    # Calculate a numeric score from 0..5 based on the centrality
    if centrality_score > 0.4: 
        return 5
    elif centrality_score > 0.35:
        return 4
    elif centrality_score > 0.3:
        return 3
    elif centrality_score > 0.25:
        return 2
    elif centrality_score > 0.2:
        return 1
    else:
        return 0


def echo_sdg_score_emoji(shortcode, score):
    return ''.join([shortcode] * score)