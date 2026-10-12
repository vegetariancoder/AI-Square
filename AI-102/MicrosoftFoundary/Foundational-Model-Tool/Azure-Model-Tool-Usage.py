from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("MODEL_ENDPOINT"), api_key=os.getenv("MODEL_API_KEY")
)

response = client.responses.create(
    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    instructions="YOU ARE A HELPFUL ASSISTANCE THAT WILL ANSWER QUESTION BASED ON TOOLS ATTACHED. ALSO PROVIDE THE CITATION LINK OR SOURCE LINK OF YOUR ANSWER",
    input="What is the compound interest on $10,000 at 5 percent annual rate over 10 years?",
    tools=[{"type": "web_search"}, {"type": "code_interpreter", "container": {"type": "auto"}}],
    # max_output_tokens=1000,
    reasoning={"effort": "low"},
)


# Inspect what happened under the hood
for item in response.output:
    if item.type == "code_interpreter_call":
        print("=== Python Code the Model Wrote ===")
        print(item.code)
        print("\n=== Output from Execution ===")
        print(item.outputs)
    elif item.type == "message":
        print("\n=== Final Answer ===")
        print(response.output_text)
