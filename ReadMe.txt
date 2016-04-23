Running Environment Set up:

Go to https://www.python.org/install to install python 2.7.10

Install Natural Language Toolkit (nltk) from http://www.nltk.org/install.html 

Install Unirest http://unirest.io/python.html

Install Eclipse to run Lucene model


For each SE run, only run the .py files in the corresponding folder.



Phase 1, Task 1:

Go to “Phase1_Indexing and Retrieval” folder

Go to “Task1” folder

Go to “BM25_RUN” folder to run BM25 search engine: 
1. run indexer.py
2. run queryTokenize.py
3. run BM25.py
4. Ranking result is stored in “BM25_Ranking_Result” folder

Go to “TF-IDF_RUN” folder to run TF-IDF search engine:
1. run indexer.py
2. run queryTokenize.py
3. run tf-idf.py
4. Ranking result is stored in “TF-IDF_Ranking_Result” folder

Import “Lucene_RUN” folder as an existing project to Eclipse:
1. Run the project
2. Ranking result is stored in the “result” folder under the project root folder.



Phase 1, Task 2 (Based on BM25 with relevance information):

Go to “Phase1_Indexing and Retrieval” folder

Go to “Task2” folder

Go to “Pseudo_Relevance_Feedback_Expansion” folder to run query expansion using pseudo relevance feedback and retrieve based on BM25:
1. Run indexer.py
2. Run queryTokenize.py
3. Run BM25.py
4. Run query_expansion_pseudo_rf.py
5. Run PRF_BM25.py
6. Ranking result is stored in “PRF_BM25_Ranking_Result” Folder


Go to “Thesauri_Expansion” folder to run query expansion using Thesauri and retrieve based on BM25:
1. Run indexer.py
2. Run queryTokenize.py
3. Run BM25.py
4. Run query_expansion_Thesaurus.py
5. Run Thesauri_BM25.py
6. Ranking result is stored in “Thesauri_BM25_Ranking_Result” Folder


Phase 1, Task 3 (Based on BM25):

Go to “stopping” folder to run stopped version of the search engine based on BM25:
1. Run indexer_stopped.py
2. Run queryTokenize_stopped.py
3. Run Stopping_BM25.py
4. Ranking result is stored in “Stopping_BM25_Ranking_Result” folder 

Go to “stemming” folder to run stopped version of the search engine based on BM25:
1. Run clean_stem.py
2. Run indexer_stemming.py
3. Run Stemming_BM25.py
4. Ranking result is stored in “stemming_BM25_Ranking_result” folder 


Phase 2, Combine query expansion with pseudo relevance feedback with stopping based on BM25:
1. Go to “Phase2_Evaluation” folder
2. Go to “Combine_query_expansion_stopping_RUN” folder
3. Run indexer_stopped.py
4. Run queryTokenize_stopped.py
5. Run Stopping_BM25.py
6. Run query_expansion_pseudo_rf.py
7. RUN PRF_Expansion_Stopping_BM25.py
8. Ranking result is stored in “Combine_query_expansion_stopping_BM25_Ranking_result” folder.








 