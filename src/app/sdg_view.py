import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_sdg_view(conn, sdg_id, max_results):

    sdgs = preload_sdgs()

    # Get primary results from TigerGraph
    results = conn.runInstalledQuery('SDG_Expansion', {'sdg': sdg_id, 'max_results' : max_results})
    current_sdg = get_current_sdg(sdgs, results)

    #
    # Write title/info
    #
    write_titles(current_sdg)

    #
    # Write Topics
    st.header('Related Topics')
    st.caption(f'These topics are groups of words and concepts that frequently occur alongside SDG {current_sdg.goal_num}')
    topics = []
    for topic in results[4]['Topics']:
        topics.append('- ' + ', '.join(topic['attributes']['terms']))
    st.markdown('\n'.join(topics))

    #
    # Write SDGs
    st.header('Related SDGs')
    related_sdgs = []
    for s in results[2]['SDGs']:
        if s['v_id'] in sdgs:
            goal_num = sdgs[s["v_id"]].goal_num
            related_sdgs.append(f'- [{goal_num}](./?sdg={goal_num}) {sdgs[s["v_id"]].goal}')         
    st.markdown('\n'.join(related_sdgs))

    #
    # Write Documents
    st.header('Documents')
    for doc in results[1]['Documents']:
        
        st.markdown(f'''
            ---------
            ##### {doc['attributes']['title']}
            {doc['attributes']['summary']}
            - **{doc['attributes']['year']}** [{doc['attributes']['organization']}]({doc['attributes']['aboutURL']})
            - **Download** [{doc['attributes']['localFilename']}]({doc['attributes']['downloadURL']})
        ''')

    st.write(results)


@st.cache
def preload_sdgs():
    # Return a Dictionary of SDGs
    return dict([(sdg.goal_num, sdg) for sdg in load_sdgs()])


def get_current_sdg(sdgs, results):
    # Return the detailed record for the current SDG
    return sdgs[results[0]['Start'][0]['v_id']]


def write_titles(sdg):
    # Write summary results into Sidebar
    st.sidebar.title(sdg.goal_num)
    st.sidebar.header(sdg.goal_category_short)
    st.sidebar.caption(sdg.goal_category_long)
    st.sidebar.subheader(f'{sdg.goal_num} - {sdg.goal}')

    st.sidebar.markdown('''
        - [Related Topics](#related-topics)
        - [Related SDGs](#related-sdgs)
        - [Documents](#documents)
    ''')


def write_documents(sdgs, results):

    # Write summary results into Sidebar
    sdg = sdgs[results[0]['Start'][0]['v_id']]
    st.sidebar.title(sdg.goal_category_short)
    st.sidebar.caption(sdg.goal_category_long)

    # Write Page title
    st.write(f'{sdg.goal}')