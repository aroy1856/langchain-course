
from callbacks import AgentCallbackHandler
from langchain_classic.agents.format_scratchpad.log import format_log_to_str
from langchain_core.tools.simple import Tool
from langchain_core.agents import AgentFinish
from langchain_core.agents import AgentAction
from typing import Union
import re
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_openai import ChatOpenAI

load_dotenv()

def find_tool_by_name(tools: list[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool {name} not found")

@tool
def get_text_length(text: str) -> int:
    """Get the length of the text."""
    print(f"Text: {text}")
    text = text.strip("'\n'").strip('"')
    return len(text)

def main():
    tools = [get_text_length]
    template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template).partial(
        tools=render_text_description(tools), 
        tool_names=[tool.name for tool in tools])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        stop_sequences=["\nObservation", "Observation:", "Observation"],
        callbacks=[AgentCallbackHandler()]
    )
    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]) 
        } 
        | prompt 
        | llm 
        | ReActSingleInputOutputParser()
    )

    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the text 'Hello, world!'?", 
                "agent_scratchpad": intermediate_steps
            }
        )

        if isinstance(agent_step, AgentAction):
            tool_name_raw = agent_step.tool
            match = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)", tool_name_raw)
            if match:
                tool_name = match.group(1)
            else:
                tool_name = tool_name_raw.strip("[]'\" ")
            
            print(f"Tool name: {tool_name}")
            
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input.strip("'\"")
            tool_output = tool_to_use.func(tool_input)
            print(f"Tool output: {tool_output}")
            
            intermediate_steps.append((agent_step, str(tool_output)))

    if isinstance(agent_step, AgentFinish):
        print(f"Final answer: {agent_step.return_values['output']}")


if __name__ == "__main__":
    main()
