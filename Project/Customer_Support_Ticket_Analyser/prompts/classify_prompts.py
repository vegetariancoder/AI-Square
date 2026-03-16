from langchain_core.prompts import ChatPromptTemplate
from Project.Customer_Support_Ticket_Analyser.config import get_chat_model
from langchain_core.runnables import RunnableLambda

# output type list

outputType = ['Category Name', 'Urgency', 'Sentiment', 'Small Summary']

# Create the CHAT PROMPT for ChatPromptTemplate

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI system that classifies customer support tickets.

Categories:
- Billing
- Technical Issue
- Account Access
- Feature Request
- Complaint

Return ONLY the category name, urgency, sentiment and small summary of the ticket.
"""
        ),
        ("human", "{ticket}")
    ]
)





# define chat template
ticket_dict = {
    'ticket': 'My credit card was charged twice'
}

chat_template = CLASSIFY_PROMPT.invoke(ticket_dict)

# use open ai chat completion to classify the ticket

chat = get_chat_model()


