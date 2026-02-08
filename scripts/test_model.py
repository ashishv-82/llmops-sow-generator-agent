
import sys
from pathlib import Path
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
import os

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agent.config import config

def test_model():
    print(f"Testing model: {config.bedrock_model_id}")
    try:
        llm = ChatBedrock(
            model_id=config.bedrock_model_id,
            client=config.bedrock_runtime,
            model_kwargs={
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
            },
        )
        response = llm.invoke([HumanMessage(content="Hello, are you working?")])
        print("Success!")
        print(response.content)
    except Exception as e:
        print(f"Error: {e}")
        # diagnostic for Nova
        if "nova" in config.bedrock_model_id:
             print("Trying with max_new_tokens...")
             try:
                llm = ChatBedrock(
                    model_id=config.bedrock_model_id,
                    client=config.bedrock_runtime,
                    model_kwargs={
                        "temperature": config.temperature,
                        "max_new_tokens": config.max_tokens,
                    },
                )
                response = llm.invoke([HumanMessage(content="Hello, are you working?")])
                print("Success with max_new_tokens!") 
                print(response.content)
             except Exception as e2:
                 print(f"Error 2: {e2}")

if __name__ == "__main__":
    test_model()
