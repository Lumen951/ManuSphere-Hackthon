from pydantic import Field

from app.agent.browser import BrowserAgent
from app.config import config
from app.prompt.browser import NEXT_STEP_PROMPT as BROWSER_NEXT_STEP_PROMPT
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, ToolCollection, WaitForUserInput
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.python_execute import PythonExecute
from app.tool.str_replace_editor import StrReplaceEditor
from app.prompt.tool_guide import get_tool_selection_prompt
from app.tool.md2card import MD2Card
from app.tool.time import CalendarTool

class Manus(BrowserAgent):
    """
    A versatile general-purpose agent that uses planning to solve various tasks.

    This agent extends BrowserAgent with a comprehensive set of tools and capabilities,
    including Python execution, web browsing, file operations, and information retrieval
    to handle a wide range of user requests.
    """

    name: str = "Manus"
    description: str = (
        "A versatile agent that can solve various tasks using multiple tools"
    )

    system_prompt: str = SYSTEM_PROMPT.format(directory=config.workspace_root)
    next_step_prompt: str = NEXT_STEP_PROMPT

    max_observe: int = 10000
    max_steps: int = 20

    # Add general-purpose tools to the tool collection
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            PythonExecute(), BrowserUseTool(), StrReplaceEditor(), Terminate(), WaitForUserInput(), MD2Card(), CalendarTool()
        )
    )

    async def think(self) -> bool:
        """Process current state and decide next actions with appropriate context."""
        # 记录原始提示
        original_prompt = self.next_step_prompt

        # 从消息历史中获取最后一条用户消息作为用户查询
        user_query = ""
        for msg in reversed(self.memory.messages):
            if msg.role == "user" and hasattr(msg, "content") and msg.content:
                user_query = msg.content
                break

        # 检查是否多次没有选择工具
        no_tool_count = 0
        for i in range(min(5, len(self.memory.messages))):
            if i >= len(self.memory.messages):
                break
            msg = self.memory.messages[-(i+1)]
            if msg.role == "assistant" and not getattr(msg, "tool_calls", None):
                no_tool_count += 1
            else:
                break

        # 如果连续多次没有选择工具，添加更强的提示
        if no_tool_count >= 1:  # 只要一次没选就提示
            # 使用工具选择指南
            if user_query:
                tool_guide = get_tool_selection_prompt(user_query)
                self.next_step_prompt = tool_guide + "\n\n" + original_prompt
            else:
                tool_names = [tool.name for tool in self.available_tools.tools]
                # 构建更直接的提示
                action_prompt = f"""
    CRITICAL INSTRUCTION: You MUST use a tool now instead of just planning.

    Available tools: {', '.join(tool_names)}

    Based on the conversation history,
    You should immediately use one of these tools to make progress.
    For information tasks, use web_search.
    For web interactions, use browser_use.
    For file or data processing, use python_execute.
    For generating a beautiful card, use md2card.
    SELECT A TOOL NOW AND TAKE ACTION.
    """
                self.next_step_prompt = action_prompt + "\n" + original_prompt

        # 检查最近消息中是否有浏览器活动
        recent_messages = self.memory.messages[-3:] if self.memory.messages else []
        browser_in_use = any(
            "browser_use" in msg.content.lower()
            for msg in recent_messages
            if hasattr(msg, "content") and isinstance(msg.content, str)
        )

        if browser_in_use:
            # 临时覆盖为特定于浏览器的提示，以获取浏览器上下文
            self.next_step_prompt = BROWSER_NEXT_STEP_PROMPT

        # 调用父类的思考方法
        result = await super().think()

        # 恢复原始提示
        self.next_step_prompt = original_prompt

        return result
