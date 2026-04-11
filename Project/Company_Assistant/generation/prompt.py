from langchain.prompts import PromptTemplate

def get_prompt():
    template = """
You are an enterprise AI assistant.

Use the following context to answer the question.
If you don't know, say you don't know.

Context:
{context}

Question:
{question}

At the end of the response, specify the name of the Section this context is taken from in the format:
Resources:*Section*
where *Section* is the name of the Heading in the context.

Answer:
"""
    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )