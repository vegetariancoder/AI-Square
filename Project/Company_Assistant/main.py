from Project.Company_Assistant.ingestion.loader import load_document
from Project.Company_Assistant.ingestion.splitter import markdown_split_document, character_split_document
from Project.Company_Assistant.embeddings_store.embedding_model import get_embedding_model,create_vector_store,load_vector_store
from services.query_service import QueryService
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "/Users/sahilnagpal/Desktop/AI-Square/Project/Company_Assistant/data/CompanyWFH.docx"

def build_index():
    docs = load_document(DATA_PATH)
    md_chunks = markdown_split_document(docs[0].page_content)
    ch_chunks = character_split_document(md_chunks)

    embedding_model = get_embedding_model()
    vectordb = create_vector_store(ch_chunks, embedding_model)
    print("Length of the Vector Store: ", len(vectordb))

    return vectordb


def main():
    embedding_model = get_embedding_model()

    vectordb = load_vector_store(embedding_model)
    query_service = QueryService(vectordb)

    while True:
        question = input("Ask: ")
        if question == "exit":
            break

        answer = query_service.query(question, strategy="mmr")
        print("\nAnswer:", answer)


if __name__ == "__main__":
    build_index()
    main()