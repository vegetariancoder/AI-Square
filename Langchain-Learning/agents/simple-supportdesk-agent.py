from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langsmith import traceable

print("Loading environment variables...")
load_dotenv()
print("Environment variables loaded!")


@tool
def get_user_account_info(user_id: str) -> str:
    """Looks up account details for a given user ID."""
    database = {
        "USR-101": {"name": "Alice", "plan": "Premium", "status": "Active"},
        "USR-102": {"name": "Bob", "plan": "Free", "status": "Suspended"},
    }
    return str(database.get(user_id, "User ID not found."))


@tool
def create_support_ticket(
    user_id: str, issue_description: str, priority: str
) -> str:
    """Creates a support ticket for a user issue. Priority must be 'Low', 'Medium', or 'High'."""
    ticket_id = "TCK-8821"
    return f"Ticket {ticket_id} created successfully for {user_id} with priority '{priority}'."


tools = [get_user_account_info, create_support_ticket]

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=2000)
llm_with_tools = llm.bind_tools(tools)



@traceable(name="LangChain Support Agent")
def run_agent(question: str) -> str:
    SYSTEM_MESSAGE = """You are a precise, professional Support Desk Assistant equipped with specialized internal tools.

    Your Primary Objective:
    Assist users with account inquiries and technical issue resolution by properly leveraging your available tools.

    Guidelines for Tool Usage:
    1. Identify Required Information: Carefully analyze user requests to determine which tool calls are necessary before generating a final response.
    2. Exact Argument Extraction: Extract precise identifiers (such as User IDs) and parameters directly from the user's input. Do not guess or fabricate missing IDs.
    3. Sequential Execution: If a task requires inspecting data before taking action (e.g., verifying account status before logging a ticket), request the lookup tool first, evaluate the result, and then proceed with necessary secondary actions.
    4. Error Handling: If a tool returns an error or indicates a user/entity is not found, clearly communicate this limitation to the user without making assumptions.
    5. Response Style: Provide clear, concise, and friendly updates after receiving tool outputs. Do not expose raw JSON or internal call IDs unless explicitly requested."""

    messages = [
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content=question),
    ]

    tools_by_name = {t.name: t for t in tools}

    # Loop until the LLM stops requesting tools
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool calls are requested, we reached the final response
        if not response.tool_calls:
            return response.content

        # Execute all tool calls requested in this turn
        for tool_call in response.tool_calls:
            selected_tool = tools_by_name[tool_call["name"]]
            print(tool_call["name"],": as tool used")
            tool_output = selected_tool.invoke(tool_call["args"])
            print(tool_output, ": as tool output")
            messages.append(
                ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"])
            )


# Test the agent
output = run_agent(
    question="First, check account USR-101. Then create a High priority ticket for them saying 'Unable to access billing dashboard'."
)
print("\n--- Final Agent Output ---")
print(output)