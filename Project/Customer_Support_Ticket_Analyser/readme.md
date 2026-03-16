## Project: AI Customer Support Ticket Analyzer


### Real-world use case

- Companies receive thousands of customer support tickets daily. They need AI to:
  - Classify the ticket 
  - Extract important details 
  - Prioritize the issue 
  - Suggest a response

We will build an AI pipeline using LangChain + LCEL to automate this.

This is actually similar to systems used at companies like **Zendesk** or **Freshworks**.


### Features Your Project Should Include
#### 1. Ticket Classification

Classify tickets into categories:
- Billing 
- Technical Issue 
- Account Access 
- Feature Request 
- Complaint

Use:

- ChatPromptTemplate 
- SystemMessage 
- HumanMessage

Example ticket: