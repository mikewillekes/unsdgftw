import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_sdg_view(conn, sdg_id, max_results):

    sdgs = preload_sdgs()

    # Get primary results from TigerGraph
    results = preload_query(conn, sdg_id, max_results)
    page_sdg = get_current_sdg(sdgs, results)

    write_titles(page_sdg)
    write_sdgs(page_sdg, sdgs, results)
    write_topics(page_sdg, results)
    write_documents(page_sdg, results)
    write_entities(page_sdg, results)


@st.cache
def preload_sdgs():
    # Return a Dictionary of SDGs
    return dict([(sdg.goal_num, sdg) for sdg in load_sdgs()])


@st.cache
def preload_query(conn, sdg_id, max_results):
    return conn.runInstalledQuery('SDG_Expansion', {'sdg': sdg_id, 'max_results' : max_results})


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
        - [Related SDGs](#related-sdgs)
        - [Related Topics](#related-topics)
        - [Related Documents](#related-documents)
        - [Related Entities](#related-entities)
    ''')


def write_sdgs(page_sdg, all_sdgs, results):
    #
    # Write Related SDGs
    #
    st.header('Related SDGs')
    st.markdown(f'These other SDGs are related to SDG {page_sdg.goal_num}')

    documents = dict([
        (d['attributes']['id'], d['attributes']) for d in results[1]['Documents']
    ])

    for result in results[2]['SDGs']:
        if result['v_id'] in all_sdgs and result['v_id'] != page_sdg.goal_num:
            
            s = all_sdgs[result["v_id"]]
            paragraphs = sorted(result['attributes']['@relatedParagraphs'], key = lambda x: x['similarity'], reverse = True)
            st.markdown(f'###### {s.goal_num} - {s.goal}')    

            # Because of how graph walking works there may be duplicate paragraphs
            num_unique_paragraphs = len(set([p['text'] for p in paragraphs]))

            with st.expander(f'SDG {page_sdg.goal_num} and {s.goal_num} are linked via {num_unique_paragraphs} paragraphs. Read more...'):
                
                st.markdown(f'[Click here to explore SDG {s.goal_num}](./?sdg={s.goal_num})')
                
                rendered_paragraphs = set()
                for paragraph in paragraphs[:10]:

                    if paragraph['text'] in rendered_paragraphs:
                        continue

                    ids = paragraph['paragraph_id'].split('.')
                    document_id = ids[0]
                    page_number = ids[1][2:]
                    if document_id in documents:
                        st.markdown(f'''
                            - {paragraph["text"]} [{documents[document_id]["title"]} ({documents[document_id]["organization"]}, Page {page_number})](./?doc={document_id})''')
                    else:
                        st.markdown(f'''
                            - {paragraph["text"]} [Document {document_id} (Page {page_number})](./?doc={document_id})''')

                    rendered_paragraphs.add(paragraph['text'])


def write_topics(page_sdg, results):
    #
    # Write Topics
    #
    st.header('Related Topics')
    st.markdown(f'These topics are groups of words and concepts that are related to SDG {page_sdg.goal_num}')
    
    documents = dict([
        (d['attributes']['id'], d['attributes']) for d in results[1]['Documents']
    ])

    for result in results[4]['Topics']:
        paragraphs = sorted(result['attributes']['@relatedParagraphs'], key = lambda x: x['similarity'], reverse = True)
        st.markdown(f'###### {", ".join(result["attributes"]["terms"])}')    

        # Because of how graph walking works there may be duplicate paragraphs
        num_unique_paragraphs = len(set([p['text'] for p in paragraphs]))

        with st.expander(f'SDG {page_sdg.goal_num} is linked to this topic via {num_unique_paragraphs} paragraphs. Read more...'):

            rendered_paragraphs = set()
            for paragraph in paragraphs[:10]:

                if paragraph['text'] in rendered_paragraphs:
                    continue

                ids = paragraph['paragraph_id'].split('.')
                document_id = ids[0]
                page_number = ids[1][2:]
                if document_id in documents:
                    st.markdown(f'''
                        - {paragraph["text"]} [{documents[document_id]["title"]} ({documents[document_id]["organization"]}, Page {page_number})](./?doc={document_id})''')
                else:
                    st.markdown(f'''
                        - {paragraph["text"]} [Document {document_id} (Page {page_number})](./?doc={document_id})''')     

                rendered_paragraphs.add(paragraph['text'])            


def write_documents(page_sdg, results):
    #
    # Write Documents
    #
    st.header('Related Documents')
    st.markdown(f'These documents are related to SDG {page_sdg.goal_num}')

    for doc in results[1]['Documents']:
        
        st.markdown(f"###### {doc['attributes']['title']} ({doc['attributes']['organization']}, {doc['attributes']['year']})")    
        with st.expander(f"SDG {page_sdg.goal_num} is linked to this document via {doc['attributes']['@visitCount']} sentences. Read more..."):

            st.markdown(f"""
                [Click here to explore SDGs in this document](./?doc={doc['attributes']['id']})

                > {doc['attributes']['summary']}
                - **Year** {doc['attributes']['year']}
                - **Visit Source** [{doc['attributes']['organization']}]({doc['attributes']['aboutURL']})
                - **Download Raw Document** [{doc['attributes']['localFilename']}]({doc['attributes']['downloadURL']})
            """)

def write_entities(page_sdg, results):
    #
    # Write Entities
    #
    st.header('Related Entities')
    st.markdown(f'These entities are extracted from paragraphs related to SDG {page_sdg.goal_num}')

    entities = []
    for entity in results[3]['Entities']:
        entities.append(f"- [{entity['attributes']['text']} ({entity['attributes']['@visitCount']} mentions)](./?entity={entity['attributes']['id']})")
        
    st.markdown('\n'.join(sorted(entities)))