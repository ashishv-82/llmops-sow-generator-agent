"""
Planner/Orchestrator for the SOW Generator agent.

Uses LangGraph to orchestrate tool execution and generate responses.
"""

from typing import Annotated, Any, Literal, TypedDict

from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from src.agent.config import config
from src.agent.prompts import get_system_prompt
from src.agent.tools import ALL_TOOLS


class AgentState(TypedDict):
    """State for the agent graph."""

    messages: Annotated[list[BaseMessage], add_messages]


class SOWAgent:
    """Main SOW Generator agent with LangGraph orchestration."""

    def __init__(self) -> None:
        """Initialize the agent with LLM and tools."""
        # Initialize LLM
        self.llm = ChatBedrock(
            model=config.bedrock_model_id,
            client=config.bedrock_runtime,
            model_kwargs={
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
            },
        )

        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(ALL_TOOLS)

        # Load system prompt
        self.system_prompt = get_system_prompt("planner")

        # Create graph
        self.graph = self._create_graph()

    def _create_graph(self) -> Any:
        """Create the LangGraph state graph."""
        # Define the graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("tools", ToolNode(ALL_TOOLS))

        # Set entry point
        workflow.set_entry_point("planner")

        # Add conditional edges
        workflow.add_conditional_edges(
            "planner",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )

        # Add edge from tools back to planner
        workflow.add_edge("tools", "planner")

        return workflow.compile()

    def _planner_node(self, state: AgentState) -> AgentState:
        """
        Main planner node that decides which tools to call.

        Args:
            state: Current agent state

        Returns:
            Updated state with planner's response
        """
        messages = state["messages"]

        # Add system prompt if this is the first message
        if len(messages) == 1 and isinstance(messages[0], HumanMessage):
            messages = [SystemMessage(content=self.system_prompt)] + messages

        # Invoke LLM
        response = self.llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """
        Determine if the agent should continue or end.

        Args:
            state: Current agent state

        Returns:
            "continue" if there are tool calls, "end" otherwise
        """
        last_message = state["messages"][-1]

        # If there are tool calls, continue
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        # Otherwise, end
        return "end"

    def run(self, user_request: str) -> str:
        """
        Run the agent with a user request.

        Args:
            user_request: User's request string

        Returns:
            Agent's final response
        """
        # Create initial state
        initial_state = {"messages": [HumanMessage(content=user_request)]}

        # Run the graph
        final_state = self.graph.invoke(initial_state)

        # Extract final response
        final_message = final_state["messages"][-1]

        if isinstance(final_message, AIMessage):
            from typing import cast
            return cast(str, final_message.content)

        return str(final_message)

    async def arun(self, user_request: str) -> str:
        """
        Run the agent asynchronously.

        Args:
            user_request: User's request string

        Returns:
            Agent's final response
        """
        # Create initial state
        initial_state = {"messages": [HumanMessage(content=user_request)]}

        # Run the graph asynchronously
        final_state = await self.graph.ainvoke(initial_state)

        # Extract final response
        final_message = final_state["messages"][-1]

        if isinstance(final_message, AIMessage):
            from typing import cast
            return cast(str, final_message.content)

        return str(final_message)


# Singleton instance
_agent_instance = None


def get_agent() -> SOWAgent:
    """Get or create the agent singleton instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SOWAgent()
    return _agent_instance
