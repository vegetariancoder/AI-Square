from langchain_core.prompts import ChatPromptTemplate
from Project.Customer_Support_Ticket_Analyser.config import get_chat_model


reply_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful customer support agent.

Write polite and professional responses to customer tickets.
"""
        ),

        # Few-shot example
        (
            "human",
            "Ticket: I was charged twice for my subscription."
        ),
        (
            "ai",
            "We apologize for the duplicate charge. Our billing team will review your account and issue a refund within 24 hours."
        ),

        (
            "human",
            "Ticket: I cannot login to my account."
        ),
        (
            "ai",
            "We are sorry you are experiencing login issues. Please try resetting your password using the password recovery option."
        ),

        ("human", "Ticket: {ticket}")
    ]
)

chat = get_chat_model()

