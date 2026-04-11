from Project.Company_Assistant.retrieval.retriever import get_similarity_retriever, get_mmr_retriever
from generation.rag_chain import build_rag_chain

class QueryService:
    def __init__(self, vectordb):
        self.vectordb = vectordb

    def query(self, question: str, strategy="mmr"):
        if strategy == "mmr":
            retriever = get_mmr_retriever(self.vectordb)
        else:
            retriever = get_similarity_retriever(self.vectordb)

        rag_chain = build_rag_chain(retriever)

        response = rag_chain.run(question)
        return response