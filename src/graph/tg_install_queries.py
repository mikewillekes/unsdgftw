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
                FROM Start:s1 -(is_similar:sim1)- Sentence:st1 -()- Paragraph:p -()- Sentence:st2 -(is_similar:sim2)- SDG:s2
                WHERE s1 != s2 AND sim1.similarity > 0.6 AND sim2.similarity > 0.6
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


print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY Build_Comention_Edges() FOR GRAPH UNSDGs SYNTAX V2 {{ 
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Count the number of Paragraphs
  # This will be the denominator in the new
  # co_mention edge weight
  SumAccum<INT> @@paragraphCount;
  result = SELECT p
                FROM Document:d -()- Paragraph:p
                ACCUM
                  @@paragraphCount += 1;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Delete Old Edges
  result = SELECT a FROM SDG:a -(co_mention:c)- Topic:b ACCUM DELETE (c);
  result = SELECT a FROM SDG:a -(co_mention:c)- Entity:b ACCUM DELETE (c);
  result = SELECT a FROM Topic:a -(co_mention:c)- Entity:b ACCUM DELETE (c);
  result = SELECT a FROM SDG:a -(co_mention:c)- SDG:b ACCUM DELETE (c);
  result = SELECT a FROM Entity:a -(co_mention:c)- Entity:b ACCUM DELETE (c);
  # Note: there's no Topic -()- Topic Edge because the NLP/Topic-modelling step
  # only associates 1-topic per Paragraph
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  SumAccum<FLOAT> @visitCountA;
  SetAccum<VERTEX<SDG>> @srcNodesA;

  # Build SDG to Topic edges
  result = SELECT t
            FROM SDG:s1 -(is_similar:sim)- Sentence:st -()- Paragraph:p -()- Topic:t
            WHERE sim.similarity > 0.6
            ACCUM
              t.@visitCountA += 1.0,
              t.@srcNodesA += s1
            POST-ACCUM FOREACH x in t.@srcNodesA DO
              INSERT INTO co_mention (FROM, TO, weight) VALUES (x, t, t.@visitCountA / (@@paragraphCount * 1.0))
            END;
 
  # Build SDG to Entity edges
  result = SELECT e
            FROM SDG:s1 -(is_similar:sim)- Sentence:st -()- Paragraph:p -()- Mention:m -()- Entity:e
            WHERE sim.similarity > 0.6
            ACCUM
              e.@visitCountA += 1.0,
              e.@srcNodesA += s1
            POST-ACCUM FOREACH x in e.@srcNodesA DO
              INSERT INTO co_mention (FROM, TO, weight) VALUES (x, e, e.@visitCountA / (@@paragraphCount * 1.0))
            END;
  
  # Build Entity to Topic edges
  # Entity nodes already have a visitCount and srcNodes (coming from SDGs),
  # so we need new accumulators for this step
  SumAccum<FLOAT> @visitCountB;
  SetAccum<VERTEX<Topic>> @srcNodesB;
  
  result = SELECT e
            FROM Topic:t -()- Paragraph:p -()- Mention:m -()- Entity:e
            ACCUM
              e.@visitCountB += 1.0,
              e.@srcNodesB += t
            POST-ACCUM FOREACH x in e.@srcNodesB DO
              INSERT INTO co_mention (FROM, TO, weight) VALUES (x, e, e.@visitCountB / (@@paragraphCount * 1.0))
            END;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Build SDG to SDG edges (where a single Paragraph links to multiple SDGs)
  SumAccum<FLOAT> @visitCountC;
  SetAccum<VERTEX<SDG>> @srcNodesC;
  
  result = SELECT s2
            FROM SDG:s1 -(is_similar:sim1)- Sentence:st1 -()- Paragraph:p -()- Sentence:st2 -(is_similar:sim2)-  SDG:s2
            WHERE sim1.similarity > 0.6 AND sim2.similarity > 0.6 AND s1 != s2
            ACCUM
              s2.@visitCountC += 1.0,
              s2.@srcNodesC += s1
            POST-ACCUM FOREACH x in s2.@srcNodesC DO
              INSERT INTO co_mention (FROM, TO, weight) VALUES (x, s2, s2.@visitCountC / (@@paragraphCount * 1.0))
            END;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Build Entity to Entity edges (where a single Paragraph links to multiple Entities)
  SumAccum<FLOAT> @visitCountD;
  SetAccum<VERTEX<Entity>> @srcNodesD;
  
  result = SELECT e2
            FROM Entity:e1 -()- Mention:m1 -()- Paragraph:p -()- Mention:m2 -()- Entity:e2
            WHERE e1 != e2
            ACCUM
              e2.@visitCountD += 1.0,
              e2.@srcNodesD += e1
            POST-ACCUM FOREACH x in e2.@srcNodesD DO
              INSERT INTO co_mention (FROM, TO, weight) VALUES (x, e2, e2.@visitCountD / (@@paragraphCount * 1.0))
            END;
}}
INSTALL QUERY Build_Comention_Edges
'''))


# Label Propagaion from the TigerGraph Data Science Library
# https://docs.tigergraph.com/graph-ml/current/community-algorithms/label-propagation
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY tg_label_prop (SET<STRING> v_type, SET<STRING> e_type, INT max_iter, INT output_limit, 
  BOOL print_accum = TRUE, STRING file_path = "", STRING attr = "") FOR GRAPH UNSDGs  SYNTAX V1 {{

  # Partition the vertices into communities, according to the Label Propagation method.
  # Indicate community membership by assigning each vertex a community ID.

  OrAccum @@or_changed = true;
  MapAccum<INT, INT> @map;     # <communityId, numNeighbors>
  MapAccum<INT, INT> @@comm_sizes_map;   # <communityId, members>
  SumAccum<INT> @sum_label, @sum_num;  
  FILE f (file_path);
  Start = {{v_type}};

  # Assign unique labels to each vertex
  Start = SELECT s 
          FROM Start:s 
          ACCUM s.@sum_label = getvid(s);

  # Propagate labels to neighbors until labels converge or the max iterations is reached
  WHILE @@or_changed == true LIMIT max_iter DO
      @@or_changed = false;
      Start = SELECT s 
              FROM Start:s -(e_type:e)- :t
              ACCUM t.@map += (s.@sum_label -> 1)  # count the occurrences of neighbor's labels
              POST-ACCUM
                  INT max_v = 0,
                  INT label = 0,
                  # Iterate over the map to get the neighbor label that occurs most often
                  FOREACH (k,v) IN t.@map DO
                      CASE WHEN v > max_v THEN
                          max_v = v,
                          label = k
                      END
                  END,
                  # When the neighbor search finds a label AND it is a new label
                  # AND the label's count has increased, update the label.
                  CASE WHEN label != 0 AND t.@sum_label != label AND max_v > t.@sum_num THEN
                      @@or_changed += true,
                      t.@sum_label = label,
                      t.@sum_num = max_v
                  END,
                  t.@map.clear();
  END;

  Start = {{v_type}};
  Start =  SELECT s 
          FROM Start:s
          POST-ACCUM 
              IF attr != "" THEN 
                  s.setAttr(attr, s.@sum_label) 
              END,
                
              IF file_path != "" THEN 
                  f.println(s, s.@sum_label) 
              END,
                
              IF print_accum THEN 
                  @@comm_sizes_map += (s.@sum_label -> 1) 
              END
          LIMIT output_limit;

  IF print_accum THEN 
      PRINT @@comm_sizes_map;
      PRINT Start[Start.@sum_label];
  END;
}}
INSTALL QUERY tg_label_prop
'''))