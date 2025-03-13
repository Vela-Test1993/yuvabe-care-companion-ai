from services.pinecone_service import retrieve_relevant_metadata
from services.supabase_service import store_chat_history
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_results(query, results):
    pairs = [(query, result["metadata"]["text"]) for result in results]
    scores = reranker.predict(pairs)
    return [x for _, x in sorted(zip(scores, results), key=lambda pair: pair[0], reverse=True)]

def chatbot_response(query):
    results = retrieve_relevant_metadata(query)
    if results:
        reranked_results = rerank_results(query, results)
        best_answer = reranked_results[0]["metadata"]["question"]
    else:
        best_answer = "I'm sorry, I couldn't find an answer for your query."

    # store_chat_history(query, best_answer)
    return best_answer
