import streamlit as st
import pyTigerGraph as tg

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *

def show_entity_view(conn, entity_id, max_results):

    sdgs = preload_sdgs()

    # Get primary results from TigerGraph
    results = preload_query(conn, entity_id, max_results)
    page_entity = get_current_entity(results)
    write_titles(page_entity)

    write_sdgs(page_entity, sdgs, results)
    write_topics(page_entity, results)
    write_documents(page_entity, results)
    write_entities(page_entity, results)


@st.cache
def preload_sdgs():
    # Return a Dictionary of SDGs
    return dict([(sdg.goal_num, sdg) for sdg in load_sdgs()])


@st.cache
def preload_query(conn, entity_id, max_results):
    return conn.runInstalledQuery('Entity_Expansion', {'entity': entity_id, 'max_results' : max_results})


def get_current_entity(results):
    return results[0]['Start'][0]['attributes']


def write_titles(page_entity):
    # Write summary results into Sidebar
    st.sidebar.title(page_entity['text'])

    st.sidebar.markdown('''
        - [Related SDGs](#related-sdgs)
        - [Related Topics](#related-topics)
        - [Related Documents](#related-documents)
        - [Related Entities](#related-entities)
    ''')


def write_sdgs(page_entity, all_sdgs, results):
    #
    # Write Related SDGs
    #
    st.header('Related SDGs')
    st.markdown(f'These other SDGs are related to {page_entity["text"]}')

    documents = dict([
        (d['attributes']['id'], d['attributes']) for d in results[1]['Documents']
    ])

    for result in results[2]['SDGs']:

        s = all_sdgs[result["v_id"]]
        paragraphs = result['attributes']['@relatedParagraphs']
        st.markdown(f'###### {s.goal_num} - {s.goal}')    

        with st.expander(f'{page_entity["text"]} and SDG {s.goal_num} are linked via {len(paragraphs)} paragraphs. Read more...'):
            st.markdown(f'[Click here to explore SDG {s.goal_num}](./?sdg={s.goal_num})')
            for paragraph in paragraphs[:25]:

                ids = paragraph['paragraph_id'].split('.')
                document_id = ids[0]
                page_number = ids[1][2:]
                if document_id in documents:
                    st.markdown(f'''
                        - {paragraph["text"]} [{documents[document_id]["title"]} ({documents[document_id]["organization"]}, Page {page_number})](./?doc={document_id})''')
                else:
                    st.markdown(f'''
                        - {paragraph["text"]} [Document {document_id} (Page {page_number})](./?doc={document_id})''')


def write_topics(page_entity, results):
    #
    # Write Topics
    #
    st.header('Related Topics')
    st.markdown(f'These topics are groups of words and concepts that are related to {page_entity["text"]}')
    
    documents = dict([
        (d['attributes']['id'], d['attributes']) for d in results[1]['Documents']
    ])

    for result in results[4]['Topics']:
        paragraphs = result['attributes']['@relatedParagraphs']
        st.markdown(f'###### {", ".join(result["attributes"]["terms"])}')    

        with st.expander(f'{page_entity["text"]} is linked to this topic via {len(paragraphs)} paragraphs. Read more...'):

            for paragraph in paragraphs[:25]:

                ids = paragraph['paragraph_id'].split('.')
                document_id = ids[0]
                page_number = ids[1][2:]
                if document_id in documents:
                    st.markdown(f'''
                        - {paragraph["text"]} [{documents[document_id]["title"]} ({documents[document_id]["organization"]}, Page {page_number})](./?doc={document_id})''')
                else:
                    st.markdown(f'''
                        - {paragraph["text"]} [Document {document_id} (Page {page_number})](./?doc={document_id})''')                 


def write_documents(page_entity, results):
    #
    # Write Documents
    #
    st.header('Related Documents')
    st.markdown(f'These documents are related to {page_entity["text"]}')

    for doc in results[1]['Documents']:
        
        st.markdown(f"###### {doc['attributes']['title']} ({doc['attributes']['organization']}, {doc['attributes']['year']})")    
        with st.expander(f"{page_entity['text']} is linked to this document via {doc['attributes']['@visitCount']} sentences. Read more..."):

            st.markdown(f"""
                [Click here to explore SDGs in this document](./?doc={doc['attributes']['id']})

                > {doc['attributes']['summary']}
                - **Year** {doc['attributes']['year']}
                - **Visit** [{doc['attributes']['organization']}]({doc['attributes']['aboutURL']})
                - **Download Raw Document** [{doc['attributes']['localFilename']}]({doc['attributes']['downloadURL']})
            """)


def write_entities(page_entity, results):
    #
    # Write Entities
    #
    st.header('Related Entities')
    st.markdown(f'These entities are extracted from paragraphs related to SDG {page_entity["text"]}')

    entities = []
    for entity in results[3]['Entities']:
        entities.append(f"- [{entity['attributes']['text']} ({entity['attributes']['@visitCount']} mentions)](./?entity={entity['attributes']['id']})")
        
    st.markdown('\n'.join(sorted(entities)))