def get_similarity_retriever(vectordb, k=5):
    return vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k,'lambda_mult':0.8}
    )


def get_mmr_retriever(vectordb, k=5):
    return vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k,'lambda_mult':0.8}
    )