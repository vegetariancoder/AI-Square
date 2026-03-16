from Project.Customer_Support_Ticket_Analyser.prompts.reply_prompts import reply_prompt
from Project.Customer_Support_Ticket_Analyser.config import get_chat_model


# create chat
chat = get_chat_model()


# create chain
reply_chain = reply_prompt | chat