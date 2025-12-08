from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schema import Result

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
search_tool = TavilySearch()
llm_with_structured_output = llm.with_structured_output(Result)

prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
).partial(format_instructions="")

agent = create_react_agent(
    llm,
    tools=[search_tool],
    prompt=prompt_with_format_instructions,
)

agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)
extrct_output = RunnableLambda(lambda x: x["output"])
chain = agent_executor | extrct_output | llm_with_structured_output


def main():
    result = chain.invoke({"input": "What is the latest news about the stock market?"})
    print(result)

    
    


if __name__ == "__main__":
    main()
