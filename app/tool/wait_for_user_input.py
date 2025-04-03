import asyncio
from typing import Optional

from pydantic import Field

from app.tool.base import BaseTool, ToolResult


_WAIT_FOR_USER_INPUT_DESCRIPTION = """暂停当前执行并等待用户输入。
当您需要在执行过程中获取用户的额外信息或确认时使用此工具。
工具会暂停执行，显示一条消息给用户，然后等待用户输入后继续执行。
"""


class WaitForUserInput(BaseTool):
    """等待用户输入的工具，用于在执行过程中与用户交互。"""

    name: str = "wait_for_user_input"
    description: str = _WAIT_FOR_USER_INPUT_DESCRIPTION
    parameters: dict = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "(可选) 展示给用户的提示消息。清晰说明您需要用户提供什么信息。",
            },
            "default": {
                "type": "string",
                "description": "(可选) 当用户不提供输入时的默认值。",
            },
        },
        "required": [],
    }

    async def execute(
        self, message: Optional[str] = None, default: Optional[str] = None
    ) -> ToolResult:
        """
        暂停执行并等待用户输入。

        Args:
            message (Optional[str]): 显示给用户的提示消息
            default (Optional[str]): 用户未提供输入时的默认值

        Returns:
            ToolResult: 包含用户输入的结果对象
        """
        prompt = message or "等待用户输入..."

        try:
            # 此处实际等待用户输入的逻辑会由应用框架处理
            # 工具只需返回特定结构的结果通知系统需要等待输入

            # 如果提供了默认值，则在提示中显示
            if default:
                prompt += f" (默认: {default})"

            return ToolResult(
                output="",  # 输出为空字符串
                system=f"waiting_for_user_input:{prompt}",  # 使用system字段传递控制信息
                default=default,  # 存储默认值供系统使用
            )
        except Exception as e:
            return ToolResult(error=f"等待用户输入时发生错误: {str(e)}")
