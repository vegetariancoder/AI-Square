import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy.exc import SQLAlchemyError

print("Loading environment variables...")
load_dotenv()
print("Environment variables loaded!")


DB_USER = "root"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "badminton"

db_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = SQLDatabase.from_uri(db_uri)


@tool
def sql_db_list_tables() -> str:
    """Input is an empty string, output is a comma-separated list of tables in the database."""
    return "Tables in database : " + ", ".join(db.get_usable_table_names())

@tool
def sql_db_schema(table_names: str) -> str:
    """Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling sql_db_list_tables first!
    Example Input: table1, table2, table3"""
    requested_tables = [name.strip() for name in table_names.split(",") if name.strip()]
    if not requested_tables:
        raise ValueError("Provide at least one table name.")

    available_tables = set(db.get_usable_table_names())
    missing_tables = [
        table_name for table_name in requested_tables if table_name not in available_tables
    ]
    if missing_tables:
        raise ValueError(
            f"Table(s) not found: {', '.join(missing_tables)}. "
            f"Available tables: {', '.join(sorted(available_tables))}"
        )

    return db.get_table_info(table_names=requested_tables)


@tool
def sql_db_query(query: str) -> str:
    """Input to this tool is a detailed and correct SQL query, output is a result from the database.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields."""
    if not query.strip():
        return "Error: SQL query cannot be empty."
    try:
        return db.run(query)
    except SQLAlchemyError as error:
        return f"Error: {error}"

tools = [sql_db_list_tables, sql_db_schema, sql_db_query]

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="sqlite",
    top_k=5,
)

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=2000)

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt=system_prompt,
)


question = "List all players who use a Yonex racket."

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": question}]},
    version="v3",
)
for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
    elif kind == "tool_calls":
        print(f"\nTool call: {item.tool_name}({item.input})")
        for delta in item.output_deltas:
            print(delta, end="", flush=True)
        print(f"\nTool result: {item.output}")

final_state = stream.output