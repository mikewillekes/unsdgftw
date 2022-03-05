# Local application imports
from graph.graph_builder import stage_graph_data
from graph.graph_loader import load_graph_data


def main():
    stage_graph_data('IPBES')
    stage_graph_data('IUCN')
    stage_graph_data('IPCC')
    stage_graph_data('MA')

    load_graph_data('IPBES')
    load_graph_data('IUCN')
    load_graph_data('IPCC')
    load_graph_data('MA')


if __name__ == "__main__":
    main()