from langchain_community.embeddings import OpenAIEmbeddings
from Project.Company_Assistant.config import load_dotenv, vector_store_name
from Project.Company_Assistant.ingestion.splitter import markdown_split_document, character_split_document, load_document
from langchain_community.vectorstores import Chroma

def get_embedding_model():

    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

    return embedding_model

def create_vector_store(documents, embedding_model ,persist_directory=vector_store_name):
    print("Start Creating Vector Store")
    vector_store = Chroma.from_documents(documents=documents,
                                         embedding=embedding_model,
                                         persist_directory=persist_directory)
    print("Vector Store Created")
    return vector_store

def load_vector_store(embedding_model):
    return Chroma(persist_directory=vector_store_name, embedding_function=embedding_model)



# word_doc = load_document("/Users/sahilnagpal/Desktop/AI-Square/Project/Company_Assistant/data/CompanyWFH.docx")
#
# md_split_doc = markdown_split_document(word_doc[0].page_content)
#
# ch_split_doc = character_split_document(md_split_doc)
#
# print(len(ch_split_doc))
#
# embedding_model = get_embedding_model()
#
#
#
#
# print(len(create_vector_store(embedding_model=embedding_model,
#                           documents=ch_split_doc)))







