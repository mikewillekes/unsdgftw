# Semantic Graph Explorer for Sustainable Development

A submission for the [TigerGraph Graph for All Challenge](https://www.tigergraph.com/graph-for-all/) by Mike Willekes
- [Mail](mailto:mikewillekes@gmail.com)
- [Twitter](https://twitter.com/mikewillekes)
- [GitHub](https://github.com/mikewillekes)
- [LinkedIn](https://www.linkedin.com/in/mikewillekes/)

## **Graph for a Better World:** Enable Search for United Nations Sustainable Development Goals

![UN Sustainable Development Goals](images/sdg-intro.png)

The Sustainable Development Goals are highly interconnected: for example, goals targeting resilience of the poor and sustainable food production are linked to adverse impacts of climate change and improving food production by combating desertification and improving  soil quality.

![Visual examination of connected SDGs](images/linked-sdg-highlight.gif)

At a small scale it’s easy to visually identify these links and interconnected themes, but at a large scale this can be exceedingly difficult. Researchers and domain experts typically publish their findings in lengthy books, scientific papers and institutional reports.

A researcher, development analyst or project coordinator looking for findings that link SDG 2.4 _"sustainable and resilient agricultural practices"_ and SDG 15.3 _"combating desertification and soil restoration"_ in Central America with topics-or-themes of  _"property rights of indigenous communities"_ has to search through hundreds or thousands of pages of PDFs from organizations like:
- [UNICEF](https://data.unicef.org/resources/)
- [The World Bank Open Data Repository](https://openknowledge.worldbank.org/)
- [The International Union for Conservation of Nature](https://portals.iucn.org/library/dir/publications-list)
- [Intergovernmental Platform for Biodiversity and Ecosystem Services](https://ipbes.net/assessing-knowledge)
- [IPCC The Intergovernmental Panel on Climate Change](https://www.ipcc.ch/report/sixth-assessment-report-cycle/)

## Natural Language Processing and TigerGraph to the Rescue!

The concept of applying Natural Language Processing techniques to extract and construct knowledge graphs from unstructured text is not new. I personally began working on projects in this techncial domain more than ten years ago. However, what once took years of R&D by a team of researchers and engineers, is now achieveable by a proficient solo-developer in a few weeks on commodity hardware. What *has* changed recently is:

- The availability of powerful, pre-trained NLP Language Models
- SaaS graph database platforms, like [TigerGraph](https://www.tigergraph.com/), with great community support and a low barrier to entry

![NLP to Graph](images/nlp-to-graph.gif)

The goal of this project was to build a solution that empowered non-technical (about programming, web-crawling, machine learning or graph databases) users to easily discover links between Documents, SDGs, Entities (people, places and organizations) and Topics, while always retaining the link back to a source document or paragraph.


### A Single Document
![Graph representation of one document](images/single-document.gif)

### Multiple Documents
![Graph representation of multiple documents](images/multiple-documents.png)

This final aspect significanly increased the technical complexity of the solution. Many described and published approaches focus only on extracting and building a Knowledge Graph, presenting their results as a [traditional node-linked diagram](https://www.google.com/search?q=nlp+build+knowledge+graph&tbm=isch&chips=q:nlp+build+knowledge+graph,online_chips:named+entity+recognition), which great for conveying the results to other graph professionals, but difficult to navigate for non-technical users. A user-frendly Web Application front-end would need to be built backed by TigerGraph as the data engine.


Use the **Semantic Graph Explorer for Sustinable Development** to find links between SDG 15.7 _"Take urgent action to end poaching and trafficking of protected species of flora and fauna and address both demand and supply of illegal wildlife products"_ and the topic "Women, rights and Gender-Based Violence" which are linked in the document [Gender-based violance and environment linkages (IUCN 2020)](https://portals.iucn.org/library/node/48969)
![SDG 15.7 and GBV](images/ui-sdg-to-topic.gif)



Explain what your project is trying to accomplish and how you utilized graph technology to achieve those goals. 
Describe how your submission is relevant to the problem statement and why it is impactful to the world. Remember to link your submission video here. 

Tell us how your entry was the most...					

- Impactful in solving a real world problem 
- Innovative use case of graph
- Ambitious and complex graph
- Applicable graph solution 

Other additions: 

 - **Data**: Give context for the dataset used and give full access to judges if publicly available or metadata otherwise. 
 - **Technology Stack**: Describe technologies and programming languages used. 
 - **Visuals**: Feel free to include other images or videos to better demonstrate your work.
 - Link websites or applications if needed to demonstrate your work. 

## Dependencies

State any dependencies and their versions needed to be installed to test this project. This may include programming languages, frameworks, libraries, and etc. 

## Installation

Please give detailed instructions on installing, configuring, and running the project so judges can fully replicate and assess it. 

This can include:
1. Clone repository
2. Install dependencies
3. Access data
4. Steps to build/run project


## Reflections

### What Went Well

- From early-on, a priority was placed on scripts to automate the end-to-end flow: regenerating datasets from raw PDFs, to dropping-and-recreating the TigerGraph schema and installing queries, loading data and enriching the graphs with augmented edges, centrality and community detection; This enabled fast, frequent iteration as all of the moving parts started coming together
- The graph schema worked very well from inception to delivery
![Graph Schema](images/schema.png)
- The TigerGraph and GSQL tools were easy get started, well documented and performed extremely well; however it did take a while to adjust to thinking in terms of GSQL and Accumulators vs. relational SQL

### Known Issues and Future Improvements

- It was out of scope to build a semantic _search_ interface, only exploration; a future improvement would be to include a semantic search solution via vector similarity.
- Semantic similarity (cosine distance) was calculated between each sentence and each SDG sub-goal using a pre-trained transformer model. This simple unsupervised ML approach often had diffiulties distinguishing between multiple but similar SGS. Likely a supervised multi-class classifier approach could achieve better results.
- Research documents themselves contains numerous references to other publications. These were *not* taken into account when building the Knowledge Graph. 
- Topics, extracted as a collection of words, are _weird_ for displaying to non-NLP enthusiasts. We understand what _"fgm|girls|practice|women|undergone|aged|who|prevalence|years|15"_ is about, but it's not a user-friendly way to display data.
- SDGs, Entities and Topics were considered 'related' if they co-occurred in the same Paragraph. This is a naive rule that doesn't always hold true (i.e. for very long paragraphs).
- More Data! About 200 PDFs (~21K Paragraphs of text) were crawled across 5 organizations. The focus of this project was on the NLP, graph algorithms and UI development instead. However with a bit more work, this approach could easily scale to 1000s of documents. 
- The TigerGraph CSV API is clunky to use as schema changes. Late in the project, a few new fields were added to nodes and edges to explore capabilties of the TigerGraph data science library; but this broke all the existing loading scripts as positional CSV column designations match anymore.
- It could be compelling to explore a proof-of-concept using this Knowledge Graph to generate graph embedding that could be shared to enrich other downstream machine learning tasks. 


### Open Source Tools
- [Hugging Face: Transformers](https://huggingface.co/docs/transformers/index)
- [spaCy](https://spacy.io/)
- [BERTopic: Topic modelling with Transformers](https://maartengr.github.io/BERTopic/index.html)
- [Apache Tika: PDF Text Extraction](https://tika.apache.org/)
- [Beautiful Soup: HTML processing](https://beautiful-soup-4.readthedocs.io/en/latest/)

### Blog Posts and Videos
- [Use PyTorch and TensorFlow with an NVIDIA GPU in the Windows Linux Subsystem (WSL)
](https://youtu.be/mWd9Ww9gpEM)
- [Organizing your scholarly PDFs to easily find keywords using pdfminer.six](https://medium.com/@boilertoad_30976/organizing-your-scholarly-pdfs-to-easily-find-keywords-using-pdfminer-six-b50409b5015f)
- [Semantic Search with Sentence Transformers](https://github.com/UKPLab/sentence-transformers/tree/master/examples/applications/semantic-search)
- [Fast Clustering with Sentence Transformers](https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/fast_clustering.py)
