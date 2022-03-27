import os 
from dotenv import load_dotenv
import pyTigerGraph as tg

# Local application imports
from config import config

load_dotenv()

# Connect and built schema
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}', 
    username=f'{os.environ.get("tg_username")}',
    password=f'{os.environ.get("tg_password")}')

#
# Note: on TG Free Tier - the running solution is automatically stopped after ~1hr of idle.
#       Make sure it's actually running before freaking out about connections errors
#
#print(conn.echo())

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# NOTE: ONLY UNCOMMENT FOR EMERGENCIES!! IT WILL DELETE EVERYTHING FROM YOUR GRAPH!
#print(conn.gsql('''DROP ALL'''))
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#
# Create Global Schema
#
print(conn.gsql('''
CREATE VERTEX Mention(PRIMARY_ID id STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="false"
CREATE VERTEX Corpus(PRIMARY_ID id STRING, organization STRING, sourceURL STRING, summary STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX Document(PRIMARY_ID id STRING, organization STRING, localFilename STRING, aboutURL STRING, downloadURL STRING, title STRING, summary STRING, year INT) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX Paragraph(PRIMARY_ID id STRING, pageNumber INT, paragraphNumber INT, paragraphLen INT, text STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX Sentence(PRIMARY_ID id STRING, text STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX Entity(PRIMARY_ID id STRING, text STRING, entityType STRING, lid INT) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX SDG(PRIMARY_ID id STRING, text STRING, lid INT) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"
CREATE VERTEX Topic(PRIMARY_ID id STRING, topic INT, terms SET<STRING>, lid INT) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="true"

CREATE UNDIRECTED EDGE has_entity(FROM Mention, TO Entity)
CREATE UNDIRECTED EDGE has_mention(FROM Paragraph, TO Mention)
CREATE UNDIRECTED EDGE has_sentence(FROM Paragraph, TO Sentence)
CREATE UNDIRECTED EDGE has_paragraph(FROM Document, TO Paragraph)
CREATE UNDIRECTED EDGE has_document(FROM Corpus, TO Document)
CREATE UNDIRECTED EDGE is_similar(FROM Sentence, TO SDG, similarity FLOAT DEFAULT "0.0")
CREATE UNDIRECTED EDGE has_topic(FROM Paragraph, TO Topic, probability FLOAT DEFAULT "0.0")
CREATE UNDIRECTED EDGE co_mention(FROM Entity, TO Entity|FROM SDG, TO Entity|FROM SDG, TO SDG|FROM SDG, TO Topic|FROM Topic, TO Entity, weight FLOAT DEFAULT "0.0");
'''))

#
# Create Indices
#
print(conn.gsql(f'''
CREATE GLOBAL SCHEMA_CHANGE JOB schema_change_job_AddAttributeIndex {{
  ALTER VERTEX Document ADD INDEX document_year_idx ON (year);
  ALTER VERTEX Entity ADD INDEX entity_type_idx ON (entityType);
}}'''))
print(conn.gsql('RUN GLOBAL SCHEMA_CHANGE JOB schema_change_job_AddAttributeIndex'))
print(conn.gsql('DROP JOB schema_change_job_AddAttributeIndex'))


#
# Create Graph
#
print(conn.gsql(f'''
CREATE GRAPH {config.GRAPH_NAME}(
  Mention, Corpus, Document, Paragraph, Sentence, Entity, SDG, Topic,
  has_entity, has_mention, has_sentence, has_paragraph, has_document, is_similar, has_topic
)'''))


#
# Get Secret and Token
#
conn.graphname = config.GRAPH_NAME
secret = conn.createSecret()
token = conn.getToken(secret, setToken=True)[0]

# Re-connect to graph with token
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}',
    username=f'{os.environ.get("tg_username")}',
    password=f'{os.environ.get("tg_password")}',
    graphname=config.GRAPH_NAME,
    apiToken=token)

#
# Loading Jobs
#
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_corpus_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Corpus VALUES($0, $1, $2, $3) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_document_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
    DEFINE FILENAME MyDataSource;
    LOAD MyDataSource TO VERTEX Document VALUES($0, $1, $2, $3, $4, $5, $6, $7) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_paragraph_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Paragraph VALUES($0, $1, $2, $3, $4) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_sentence_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Sentence VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_sdg_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX SDG VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_mention_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Mention VALUES($0) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_entity_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Entity VALUES($0, $1, $2) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_topic_nodes_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO VERTEX Topic VALUES($1, $3, SET($4, $5, $6, $7, $8, $9, $10, $11, $12, $13)) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_corpus_to_document_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_document VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_document_to_paragraph_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_paragraph VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_paragraph_to_sentence_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_sentence VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
CREATE LOADING JOB load_job_sentence_to_sdg_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE is_similar VALUES($0, $1, $2) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_paragraph_to_mention_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_mention VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_mention_to_entity_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_entity VALUES($0, $1) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE LOADING JOB load_job_paragraph_to_topic_edges_csv FOR GRAPH {config.GRAPH_NAME} {{
      DEFINE FILENAME MyDataSource;
      LOAD MyDataSource TO EDGE has_topic VALUES($0, $1, $2) USING SEPARATOR=",", HEADER="true", EOL="\n", QUOTE="double";
}}'''))

# All Done - Echo the token for Future Use
print(f'token: {token}')
