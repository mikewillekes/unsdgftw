# Local application imports
from graph.graph_builder import stage_graph_data
from graph.graph_loader import *


def main():

    #
    # Assumption is that Graph Schema, Loader and Queries have
    # already been created and installed via:
    #
    #   tg_create_schema.py
    #   tg_install_queries.py
    #

    stage_graph_data('IPBES')
    stage_graph_data('IUCN')
    stage_graph_data('IPCC')
    stage_graph_data('MA')
    stage_graph_data('OKR')
    stage_graph_data('UNICEF')

    load_graph_data('IPBES')
    load_graph_data('IUCN')
    load_graph_data('IPCC')
    load_graph_data('MA')
    load_graph_data('OKR')
    load_graph_data('UNICEF')

    # Build the set of Hybrid edges between
    # SDG, Entity and Topic nodes 
    build_comention_edges()

    # Run community detection on the 
    # SDG, Entity and Topic nodes 
    run_community_detection()

    # Compute centrality on the 
    # SDG, Entity and Topic nodes 
    run_centrality()

if __name__ == "__main__":
    main()