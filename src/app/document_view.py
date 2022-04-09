import itertools
from turtle import position
import streamlit as st
import pyTigerGraph as tg
import plotly.figure_factory as ff
import numpy as np

# Local application imports
from config import config
from sdgs.sustainable_development_goals import *


def show_document_view(conn, document_id):

    sdg_categories = preload_sdg_categories()

    results = get_document_distribution(conn, document_id)
    document_summary = results[0]['res'][0]['attributes']
    document_dist = results[1]['@@dist']

    st.header(document_summary['title'])
    st.caption(f"{document_summary['organization']}: {document_summary['localFilename']}")
    st.markdown(f"""
        > {document_summary['summary']}
        - **Year** {document_summary['year']}
        - **Visit Source** [{document_summary['organization']}]({document_summary['aboutURL']})
        - **Download Raw Document** [{document_summary['localFilename']}]({document_summary['downloadURL']})
    """)

    plot_sdgs(document_dist, sdg_categories)


@st.cache
def preload_sdg_categories():
    # Return a Dictionary of SDGs
    return dict([(sdg.goal_category_num, sdg.goal_category_short) for sdg in load_sdgs()])


@st.cache
def get_document_distribution(conn, document_id):
    results = conn.runInstalledQuery('Document_Distribution', {'doc': document_id})
    return results


def plot_sdgs(document_dist, sdg_categories):
    
    distribution_labels = []
    distribution_data = []
    rug_text = []

    #
    # Histogram of Entities by Page-Number in the document
    #
    filter_just_entities = lambda x: x['vertex_type'] == 'Entity'
    entity = lambda x: x['vertex_label']
    
    entity_group = itertools.groupby(
                        sorted(filter(filter_just_entities, document_dist), key=entity, reverse=True),
                        entity
                    )

    entities = {}
    for (k, v) in entity_group:
        entities[k] = [entity for entity in v]


    # Get top N entities by number of occurences 
    top_N_entities = dict(
        sorted(
            [(k, v) for (k,v) in entities.items()],
            key=lambda x: x[1][0]['visit_count'],
            reverse=True
        )[:30]
    )

    for k, v in top_N_entities.items():
        sorted_values = sorted([entity for entity in v], key=lambda x: x['position'])
        if (len(sorted_values) > 1):
            distribution_labels.append(k)
            distribution_data.append([entity['position'] for entity in sorted_values])
            rug_text.append(k)

    #
    # Histogram of Topics by Page-Number in the document
    #
    filter_just_topics = lambda x: x['vertex_type'] == 'Topic'
    topic = lambda x: x['vertex_label'].split('_')[0]
    
    topic_group = itertools.groupby(
                    sorted(filter(filter_just_topics, document_dist), key=topic, reverse=True),
                    topic
                )

    topics = {}
    for (k, v) in topic_group:
        topics[k] = [topic for topic in v]

    # Get top N topics by number of occurences 
    top_N_topics = dict(
        sorted(
            [(k, v) for (k,v) in topics.items()],
            key=lambda x: x[1][0]['visit_count'],
            reverse=True
        )[:10]
    )

    for (k, v) in top_N_topics.items():
        sorted_values = sorted([topic for topic in v], key=lambda x: x['position'])
        if (len(sorted_values) > 1):
            distribution_labels.append(k)
            distribution_data.append([topic['position'] for topic in sorted_values])
            rug_text.append(k)

    #
    # Histogram of SDGs by Page-Number in the document
    #
    filter_just_sdgs = lambda x: x['vertex_type'] == 'SDG'
    sdg_by_category_number = lambda x: x['vertex_id'].split('.')[0]
    sdg_by_category_number_as_int = lambda x: int(sdg_by_category_number(x))

    sdg_dist = itertools.groupby(
                    sorted(filter(filter_just_sdgs, document_dist), key=sdg_by_category_number_as_int, reverse=True),
                    sdg_by_category_number
                )

    for (k, v) in sdg_dist:
        sorted_values = sorted([sdg for sdg in v], key=lambda x: x['position'])
        if (len(sorted_values) > 1):
            distribution_labels.append(f'SDG {k} {sdg_categories[k]}')
            distribution_data.append([sdg['position'] for sdg in sorted_values])
            rug_text.append([sdg['anchor_text'] for sdg in sorted_values])


    # Create distplot with custom bin_size
    fig = ff.create_distplot(
        distribution_data,
        distribution_labels,
        rug_text=rug_text,
        show_curve=False,
        bin_size=10)

    fig.update_layout(
        title='Sustainable Development Goals, Topics and Entities by Page Number',
        xaxis_title='Page Number',
        legend_title='Reference'
    )

    # Plot!
    st.plotly_chart(fig, use_container_width=True)


def plot_topics(document_dist):

    #
    # Histogram of SDGs by Page-Number in the document
    #
    filter_just_topics = lambda x: x['vertex_type'] == 'Topic'
    topic = lambda x: x['vertex_label'].split('_')[0]
    
    topic_dist = itertools.groupby(
                    sorted(filter(filter_just_topics, document_dist), key=topic, reverse=True),
                    topic
                )

    distribution_labels = []
    distribution_data = []
    rug_text = []

    for (k, v) in topic_dist:
        sorted_values = sorted([topic for topic in v], key=lambda x: x['position'])
        if (len(sorted_values) > 1):
            distribution_labels.append(k)
            distribution_data.append([topic['position'] for topic in sorted_values])
            rug_text.append([topic['vertex_label'] for topic in sorted_values])

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
        distribution_data,
        distribution_labels,
        rug_text=rug_text,
        show_curve=False,
        bin_size=10)

    fig.update_layout(
        title='Topics by Page Number',
        xaxis_title='Page Number',
        legend_title='Topic'
    )

    # Plot!
    st.plotly_chart(fig, use_container_width=True)