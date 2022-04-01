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
CREATE QUERY SDG_Expansion(VERTEX<SDG> sdg, INT max_results) FOR GRAPH {config.GRAPH_NAME} {{ 
  
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
CREATE QUERY Sentence_Expansion(SET<VERTEX<Sentence>> sentences, INT max_results) FOR GRAPH {config.GRAPH_NAME} {{ 
    
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
CREATE QUERY Build_Comention_Edges() FOR GRAPH {config.GRAPH_NAME} SYNTAX V2 {{ 
  
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
            FROM SDG:s1 -(is_similar:sim)- Sentence:st -()- Paragraph:p -(has_topic:ht)- Topic:t
            WHERE sim.similarity > 0.6 AND ht.probability > 0.6
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
            FROM Topic:t -(has_topic:ht)- Paragraph:p -()- Mention:m -()- Entity:e
            WHERE ht.probability > 0.6
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


# Closeness Centrality from the TigerGraph Data Science Library
# https://docs.tigergraph.com/graph-ml/current/centrality-algorithms/closeness-centrality
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY Homepage(INT max_results) FOR GRAPH {config.GRAPH_NAME} {{ 
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Step 1: Get all the clusters (from the label ID attribute: 'lid')
  SetAccum<INT> @@clusters;
  results = SELECT s1
              FROM SDG:s1
              ACCUM
                @@clusters += s1.lid;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # For Each cluster get the SDGs and top N Topics and top N Entities
  # (where order is determined by a previous run of Centrality algorithm)
  
  MapAccum<INT, ListAccum<VERTEX<Topic>>> @@topicsByCluster;
  SetAccum<VERTEX<Topic>> @@topics;
  
  MapAccum<INT, ListAccum<VERTEX<Entity>>> @@entitiesByCluster;
  SetAccum<VERTEX<Entity>> @@entities;

  MapAccum<INT, ListAccum<VERTEX<SDG>>> @@sdgsByCluster;
  SetAccum<VERTEX<SDG>> @@sdgs;
  
  FOREACH cluster in @@clusters DO

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Topics
    top_N_topics = SELECT t 
                    FROM Topic:t
                    WHERE t.lid == cluster 
                    ORDER BY t.cent DESC LIMIT max_results;
    
    res = SELECT t
          FROM top_N_topics:t
          ACCUM
            @@topicsByCluster += (cluster -> t),
            @@topics += t;
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Entites  
    top_N_entities = SELECT e 
                    FROM Entity:e
                    WHERE e.lid == cluster 
                    ORDER BY e.cent DESC LIMIT max_results;
    
    res = SELECT e
          FROM top_N_entities:e
          ACCUM
            @@entitiesByCluster += (cluster -> e),
            @@entities += e;
  
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SDGs  
    top_N_sdgs = SELECT s 
                    FROM SDG:s
                    WHERE s.lid == cluster 
                    ORDER BY s.cent DESC LIMIT max_results;
    
    res = SELECT s
          FROM top_N_sdgs:s
          ACCUM
            @@sdgsByCluster += (cluster -> s),
            @@sdgs += s;
  
  END;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Print/Return Topics
  Start = @@topics;
  Topics = SELECT t FROM Start:t;
  PRINT Topics;
  PRINT @@topicsByCluster;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Print/Return Entities
  Start = @@entities;
  Entities = SELECT e FROM Start:e;
  PRINT Entities;
  PRINT @@entitiesByCluster;
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Print/Return SDGs
  Start = @@sdgs;
  SDGs = SELECT s FROM Start:s;
  PRINT SDGs;
  PRINT @@sdgsByCluster;
  
}}
INSTALL QUERY Homepage
'''))


# Label Propagaion from the TigerGraph Data Science Library
# https://docs.tigergraph.com/graph-ml/current/community-algorithms/label-propagation
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY tg_label_prop (SET<STRING> v_type, SET<STRING> e_type, INT max_iter, INT output_limit, 
  BOOL print_accum = TRUE, STRING file_path = "", STRING attr = "") FOR GRAPH {config.GRAPH_NAME}  SYNTAX V1 {{

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


# Closeness Centrality from the TigerGraph Data Science Library
# https://docs.tigergraph.com/graph-ml/current/centrality-algorithms/closeness-centrality
print(conn.gsql(f'''
USE GRAPH {config.GRAPH_NAME}
CREATE QUERY tg_closeness_cent(SET<STRING> v_type, SET<STRING> e_type, STRING re_type,INT max_hops = 10,
  INT top_k = 100, BOOL wf = TRUE, BOOL print_accum = True, STRING result_attr = "",
  STRING file_path = "", BOOL display_edges = FALSE) FOR GRAPH {config.GRAPH_NAME} SYNTAX V1 {{
  
  /* Compute Closeness Centrality for each VERTEX. 
  Use multi-sourse BFS.
  Link of the paper: http://www.vldb.org/pvldb/vol8/p449-then.pdf
  Parameters:
  v_type: vertex types to traverse                 print_accum: print JSON output
  e_type: edge types to traverse                   result_attr: INT attr to store results to
  re_type: reverse edge type in directed graph, in undirected graph set re_type=e_type
  max_hops: look only this far from each vertex    file_path: file to write CSV output to
  top_k: report only this many top scores          display_edges: output edges for visualization
  wf: Wasserman and Faust normalization factor for multi-component graphs */ 
  
  TYPEDEF TUPLE<VERTEX Vertex_ID, FLOAT score> Vertex_Score; #tuple to store closeness centrality score
  HeapAccum<Vertex_Score>(top_k, score DESC) @@top_scores_heap; #heap to store top K score
  SumAccum<INT> @@sum_curr_dist; #current distance
  BitwiseOrAccum @bitwise_or_visit_next; #use bitwise instead of setAccum
  SumAccum<INT> @sum_res; #Result, sum of distance
  SumAccum<INT> @sum_size; #get graph size
  SumAccum<FLOAT> @sum_score;
  BitwiseOrAccum @bitwise_or_seen;
  BitwiseOrAccum @bitwise_or_visit; 
  SumAccum<INT> @@sum_count=1;#used to set unique ID
  SumAccum<INT> @sum_id; #store the unique ID
  SetAccum<INT> @@batch_set; #used to set unique ID
  MapAccum<INT,INT> @@map; #used to set unique ID 
  SetAccum<EDGE> @@edge_set;
  INT empty=0;
  FILE f (file_path);
  INT num_vert;
  INT batch_number;
# Compute closeness  
  all = {{v_type}};
  
  num_vert = all.size();
  batch_number = num_vert/60;
  IF batch_number==0 THEN batch_number=1; END;
    
  #Calculate the sum of distance to other vertex for each vertex
  FOREACH i IN RANGE[0, batch_number-1] DO
          Start = SELECT s 
                  FROM all:s
                  WHERE getvid(s)%batch_number == i
                  POST-ACCUM 
            @@map+=(getvid(s)->0),
                        @@batch_set+=getvid(s);
  
          FOREACH ver in @@batch_set DO 
              @@map+=(ver->@@sum_count); 
        @@sum_count+=1;
          END; #set a unique ID for each vertex, ID from 1-63
    
          Start = SELECT s 
                  FROM Start:s 
                  POST-ACCUM 
             s.@sum_id=@@map.get(getvid(s));
    
          Start = Select s 
                  FROM Start:s
                  POST-ACCUM 
             s.@bitwise_or_seen=1<<s.@sum_id,
                         s.@bitwise_or_visit=1<<s.@sum_id; # set initial seen and visit s.@seen1 s.@seen2 
          @@batch_set.clear();
          @@map.clear();
          @@sum_count=0;
      
          WHILE (Start.size() > 0) LIMIT max_hops DO
                @@sum_curr_dist+=1;
                Start = SELECT t FROM Start:s -(re_type:e)-v_type:t
                        WHERE s.@bitwise_or_visit&-t.@bitwise_or_seen-1>0 and s!=t #use -t.@seen-1 to get the trverse of t.@seen
                        ACCUM
                              INT c = s.@bitwise_or_visit&-t.@bitwise_or_seen-1,
                              IF c>0 THEN
                                  t.@bitwise_or_visit_next+=c,
                                  t.@bitwise_or_seen+=c
                              END
                        POST-ACCUM
                              t.@bitwise_or_visit=t.@bitwise_or_visit_next,
                              INT r = t.@bitwise_or_visit_next,
                              WHILE r>0 DO 
                                    r=r&(r-1),t.@sum_res+=@@sum_curr_dist,t.@sum_size+=1 #count how many 1 in the number, same as setAccum,size()
                              END,
                              t.@bitwise_or_visit_next=0;
          END;
          @@sum_curr_dist=0;
          Start = SELECT s 
                  FROM all:s 
                  POST-ACCUM 
                        s.@bitwise_or_seen=0,s.@bitwise_or_visit=0;
  END;
  
  #Output
  IF file_path != "" THEN
      f.println("Vertex_ID", "Closeness");
  END;
  
  Start = SELECT s 
          FROM all:s
    # Calculate Closeness Centrality for each vertex
          WHERE s.@sum_res>0
          POST-ACCUM 
                IF wf THEN 
                    s.@sum_score = (s.@sum_size*1.0/(num_vert-1))*(s.@sum_size*1.0/s.@sum_res) 
                ELSE 
                    s.@sum_score = s.@sum_size*1.0/s.@sum_res*1.0 
                END,
    
                IF result_attr != "" THEN 
                    s.setAttr(result_attr, s.@sum_score) 
                END,
    
                IF print_accum THEN 
                    @@top_scores_heap += Vertex_Score(s, s.@sum_score) 
                END,
    
                IF file_path != "" THEN 
                    f.println(s, s.@sum_score) 
                END;
   #test

   IF print_accum THEN
       Start = SELECT s 
               FROM all:s
               WHERE s.@sum_res<=0 
               POST-ACCUM 
                     @@top_scores_heap += Vertex_Score(s, -1);
       PRINT @@top_scores_heap AS top_scores;
       IF display_edges THEN
     PRINT Start[Start.@sum_score];
       Start = SELECT s
         FROM Start:s -(e_type:e)-:t
         ACCUM 
                     @@edge_set += e;
         PRINT @@edge_set;
       END;
    END;
}}
INSTALL QUERY tg_closeness_cent
'''))