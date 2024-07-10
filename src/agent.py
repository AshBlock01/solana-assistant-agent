from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq

from utils import get_price_for_token, get_rug_score
from langgraph.checkpoint.sqlite import SqliteSaver

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

memory = SqliteSaver.from_conn_string(":memory:")

class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        return {'messages': results}

# Example usage
if __name__ == "__main__":
    prompt = """You are an expert smart assistant for crypto. Use the search API engine to look up information and provide your full analysis. \
    You are allowed to make multiple calls (either together or in sequence). \
    Only look up information when you are sure of what you want. \
    If you need to look up some information before asking a follow-up question, you are allowed to do that.
    """
    model = ChatGroq(model_name="gemma2-9b-it", api_key="Your groq api key here")

    agent = Agent(model, [get_price_for_token, get_rug_score], system=prompt,checkpointer=memory)

    # Example Input and Output
    messages = [HumanMessage(content="is this rug MAXt5moBxMd665GKPx6bammFf5t9pPSG6q7z9Adtm9Z")]
    thread = {"configurable": {"thread_id": "2"}}

    result = agent.graph.invoke({"messages": messages}, thread)
    print(result['messages'][-1].content)
