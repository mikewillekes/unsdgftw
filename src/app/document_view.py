import itertools
from turtle import position
import streamlit as st
import pyTigerGraph as tg
import plotly.figure_factory as ff
import numpy as np

# Local application imports
from config import config


def show_document_view(conn, document_id):
    st.title(f'Document {document_id}')
    
    results = get_document_distribution(conn, document_id)
    document_summary = results[0]['res'][0]['attributes']
    doucment_dist = results[1]['@@dist']

    st.write(document_summary)

    # ------
    # sdg_dist = [sdg for sdg in filter(lambda x: x['vertex_type'] == 'SDG', doucment_dist)]        
    # st.write(sdg_dist)
    # sdg_dist_dict = dict([
    #         (sdg['vertex_id'],
    #         filter(lambda x: x['vertex_type'] == 'SDG', doucment_dist)
    #          for sdg in filter(lambda x: x['vertex_type'] == 'SDG', doucment_dist)]        

    filter_just_sdgs = lambda x: x['vertex_type'] == 'SDG'
    sdg_by_category_number = lambda x: x['vertex_id'].split('.')[0]
    sdg_by_category_number_as_int = lambda x: int(sdg_by_category_number(x))

    sdg_dist = itertools.groupby(
                    sorted(filter(filter_just_sdgs, doucment_dist), key=sdg_by_category_number_as_int, reverse=True),
                    sdg_by_category_number
                )

    distribution_labels = []
    distribution_data = []
    rug_text = []

    for (k, v) in sdg_dist:
        positions = sorted([sdg['position'] for sdg in v])
        if (len(positions) > 1):
            distribution_labels.append('SDG ' + k)
            distribution_data.append(positions)
            rug_text.append('The distplot figure factory displays a combination of statistical representations of\nnumerical data, such as histogram, kernel density\nestimation or normal curve, and rug plot.')

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
        distribution_data,
        distribution_labels,
        rug_text=rug_text,
        show_curve=False,
        
        bin_size=10)

    # Plot!
    st.plotly_chart(fig, use_container_width=True)



@st.cache
def get_document_distribution(conn, document_id):
    results = conn.runInstalledQuery('Document_Distribution', {'doc': document_id})
    return results


