from posixpath import split
import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_sdg_view(conn, sdg_id, max_results):

    sdgs = preload_sdgs()

    # Get primary results from TigerGraph
    results = conn.runInstalledQuery('SDG_Expansion', {'sdg': sdg_id, 'max_results' : max_results})
    page_sdg = get_current_sdg(sdgs, results)

    #
    # Write title/info
    #
    write_titles(page_sdg)

    #
    # Write Topics
    st.header('Related Topics')
    st.markdown(f'These topics are groups of words and concepts that frequently occur alongside SDG {page_sdg.goal_num}')
    topics = []
    for topic in results[4]['Topics']:
        topics.append('- ' + ', '.join(topic['attributes']['terms']))
    st.markdown('\n'.join(topics))

    write_sdgs(page_sdg, sdgs, results)

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
    st.sidebar.markdown(sdg.goal_category_long)
    st.sidebar.markdown(sdg.goal)

    st.sidebar.markdown('''
        - [Related Topics](#related-topics)
        - [Related SDGs](#related-sdgs)
        - [Documents](#documents)
    ''')


def write_sdgs(page_sdg, all_sdgs, results):
    #
    # Write Related SDGs
    #
    st.header('Related SDGs')

    documents = dict([
        (d['attributes']['id'], d['attributes']) for d in results[1]['Documents']
    ])

    for result in results[2]['SDGs']:
        if result['v_id'] in all_sdgs and result['v_id'] != page_sdg.goal_num:
            
            s = all_sdgs[result["v_id"]]
            paragraphs = sorted(result['attributes']['@relatedParagraphs'], key = lambda x: x['similarity'], reverse = True)
            st.markdown(f'###### {s.goal_num} - {s.goal} _({len(paragraphs)} paragraphs)_')    

            with st.expander('Explore from here...'):
                st.markdown(f'Explore **SDG [{s.goal_num}](./?sdg={s.goal_num}) - {s.goal}**')
                for paragraph in paragraphs[:5]:

                    ids = paragraph['paragraph_id'].split('.')
                    document_id = ids[0]
                    page_number = ids[1][2:]
                    if document_id in documents:
                        st.markdown(f'''
                            {paragraph["text"]}
                            [{documents[document_id]["organization"]}, {documents[document_id]["title"]}, Page {page_number}](./?doc={document_id})''')
                    else:
                        st.markdown(f'''
                            {paragraph["text"]}
                            [Document {document_id}, Page {page_number}](./?doc={document_id})''')

                 
