from Project.Customer_Support_Ticket_Analyser.prompts.classify_prompts import CLASSIFY_PROMPT
from Project.Customer_Support_Ticket_Analyser.config import get_chat_model



# create chat
chat = get_chat_model()


# create chain
ticket_dict = {
    'ticket': 'My credit card was charged twice'
}

classify_chain = CLASSIFY_PROMPT | chat


