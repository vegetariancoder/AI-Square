from langchain.chains import RetrievalQA
from Project.Company_Assistant.config import get_chat_model
from generation.prompt import get_prompt

def build_rag_chain(retriever):
    llm = get_chat_model()

    prompt = get_prompt()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain