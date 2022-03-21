import os
import json
from dotenv import load_dotenv
import pyTigerGraph as tg

# Local application imports
from config import config

load_dotenv()

# Connect and built schema
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}',
    username=f'{os.environ.get("tg_username")}',
    password=f'{os.environ.get("tg_password")}',
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

print(conn.echo())

#
# Install Queries. See https://docs.tigergraph.com/tigergraph-server/current/api/built-in-endpoints#_run_an_installed_query_get for how to execute!
#
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY Document_Expansion(VERTEX<Document> doc, INT max_results) FOR GRAPH {config.GRAPH_NAME} {{ 
    
  #
  # For the incoming Document, walk the graph to find linked
  # Entities, Topics and SDGs 
  #
  Start = {{doc}};
 
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # SDGs
  SetAccum<INT> @pageNumber;
  AvgAccum @avgSimilarity;
  SumAccum<INT> @visitCount;
  SDGs = SELECT s 
            FROM Start:d -()- Paragraph:p -()- Sentence:st -(is_similar:sim)- SDG:s
            WHERE sim.similarity > 0.6
            ACCUM
              s.@pageNumber += p.pageNumber,
              s.@visitCount += 1,
              s.@avgSimilarity += sim.similarity,
              p.@visitCount += 1
            ORDER BY s.@visitCount DESC
            LIMIT max_results;
    
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Entities
  Entities = SELECT e 
              FROM Start:d -()- Paragraph:p -()- Mention:m -()- Entity:e
              ACCUM
                e.@pageNumber += p.pageNumber,
                e.@visitCount += 1,
                p.@visitCount += 1
              ORDER BY e.@visitCount DESC
              LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Topics
  Topics = SELECT t 
              FROM Start:d -()- Paragraph:p -()- Topic:t
              ACCUM
                t.@pageNumber += p.pageNumber,
                t.@visitCount += 1,
                p.@visitCount += 1
              ORDER BY t.@visitCount DESC
              LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Paragraphs
  Paragraphs = SELECT p 
                FROM Start:d -()- Paragraph:p
                ORDER BY p.@visitCount DESC
                LIMIT max_results;
  
  PRINT Start;
  PRINT Paragraphs;
  PRINT SDGs;
  PRINT Entities;
  PRINT Topics;
}}
INSTALL QUERY Document_Expansion
'''))


print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY SDG_Expansion(VERTEX<SDG> sdg, INT max_results) FOR GRAPH UNSDGs {{ 
  
  TYPEDEF TUPLE <STRING paragraph_id, STRING text, FLOAT similarity> PARAGRAPH_SDG_RECORD;
  
  Start = {{sdg}};
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Other highly-similar SDGs 
  AvgAccum @avgSimilarity;
  SumAccum<INT> @visitCount;
  ListAccum<PARAGRAPH_SDG_RECORD> @relatedParagraphs;
  SDGs = SELECT s2
                FROM Start:s1 -(is_similar:sim1)- Sentence:st -()- Paragraph:p -()- Sentence:st -(is_similar:sim2)- SDG:s2
                WHERE sim1.similarity > 0.6 AND sim2.similarity > 0.6
                ACCUM
                  s2.@avgSimilarity += (sim1.similarity + sim2.similarity) / 2,
                  s2.@visitCount += 1,
                  s2.@relatedParagraphs += PARAGRAPH_SDG_RECORD(p.id, p.text,  (sim1.similarity + sim2.similarity) / 2)
                ORDER BY s2.@visitCount DESC
                LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Documents linked to Paragraphs
  Documents = SELECT d
                FROM Start:s1 -(is_similar:sim1)- Sentence:st -()- Paragraph:p -()- Document:d
                ACCUM
                  d.@avgSimilarity += sim1.similarity,
                  d.@visitCount += 1
                ORDER BY d.@visitCount DESC
                LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Entities linked by mention in Paragraph
  Entities = SELECT e
              FROM Start:s1 -(is_similar:sim1)- Sentence:st -()- Paragraph:p -()- Mention:m -()- Entity:e
              ACCUM
                e.@avgSimilarity += sim1.similarity,
                e.@visitCount += 1
              ORDER BY e.@visitCount DESC
              LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Topics linked by Paragraph
  Topics = SELECT t
              FROM Start:s1 -(is_similar:sim1)- Sentence:st -()- Paragraph:p -()- Topic:t
              ACCUM
                t.@avgSimilarity += sim1.similarity,
                t.@visitCount += 1,
                t.@relatedParagraphs += PARAGRAPH_SDG_RECORD(p.id, p.text, sim1.similarity)
              ORDER BY t.@visitCount DESC
              LIMIT max_results;
  
  PRINT Start;
  PRINT Documents;
  PRINT SDGs;
  PRINT Entities;
  PRINT Topics;
}}
INSTALL QUERY SDG_Expansion
'''))


print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY Sentence_Expansion(SET<VERTEX<Sentence>> sentences, INT max_results) FOR GRAPH UNSDGs {{ 
    
  Start = {{sentences}};
       
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # SDGs linked to those Sentences
  AvgAccum @avgSimilarity;
  SumAccum<INT> @visitCount;
  SDGs = SELECT s 
                FROM Start:st -(is_similar:sim)- SDG:s
                WHERE sim.similarity > 0.6
                ACCUM
                  s.@avgSimilarity += sim.similarity,
                  s.@visitCount += 1
                ORDER BY s.@visitCount DESC
                LIMIT max_results;
 
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Documents linked to Paragraphs
  Documents = SELECT d
                FROM Start:st -()- Paragraph:p -()- Document:d
                ACCUM
                  d.@visitCount += 1
                ORDER BY d.@visitCount DESC
                LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Entities linked by mention in Paragraph
  Entities = SELECT e
              FROM Start:st -()- Paragraph:p -()- Mention:m -()- Entity:e
              ACCUM
                e.@visitCount += 1
              ORDER BY e.@visitCount DESC
              LIMIT max_results;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Topics linked by Paragraph
  Topics = SELECT t
              FROM Start:st -()- Paragraph:p -()- Topic:t
              ACCUM
                t.@visitCount += 1
              ORDER BY t.@visitCount DESC
              LIMIT max_results;
  
  PRINT Start;
  PRINT Documents;
  PRINT SDGs;
  PRINT Entities;
  PRINT Topics;
}}
INSTALL QUERY Sentence_Expansion
'''))

