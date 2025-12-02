from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class Source(BaseModel):
    """Schema for a source used by the Agent."""
    url: str = Field(description="URL of the source")

class AgentResponse(BaseModel):
    """Schema for the response from the Agent."""
    answer: str = Field(description="Answer to the question")
    sources: List[Source] = Field(description="List of sources used to answer the question", default_factory=list)
    
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
tools = [TavilySearch()]
agent = create_agent(llm, tools, response_format=AgentResponse)

def main():
    print("Hello from search-agent!")
    result = agent.invoke({"messages":HumanMessage(content="What is the weather like in India?")})
    print(result)
    


if __name__ == "__main__":
    main()
