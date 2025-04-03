import time
import datetime
from typing import Optional, Dict, Any
from zhdate import ZhDate  # 用于处理农历日期

from app.tool.base import BaseTool, ToolResult
from pydantic import Field

class CalendarTool(BaseTool):
    """日历工具
    
    提供获取系统时间和农历时间的工具方法
    """
    name: str = Field(default="calendar")  # 修复 Pydantic 的字段覆盖问题
    description: str = "获取系统时间和农历时间的工具"
    parameters: Dict[str, Any] = {
        "type": "object", 
        "properties": {
            "format": {
                "type": "string",
                "description": "时间格式,如 %Y-%m-%d %H:%M:%S",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        }
    }

    async def execute(self, **kwargs: Any) -> ToolResult:
        """执行日历时间获取
        
        Args:
            kwargs: 传入的参数字典，包含 `format` 参数
            
        Returns:
            ToolResult: 包含公历和农历时间信息的结果
        """
        try:
            time_format: str = kwargs.get("format", "%Y-%m-%d %H:%M:%S")
            now: datetime.datetime = datetime.datetime.now()
            lunar: ZhDate = ZhDate.from_datetime(now)
            
            result: Dict[str, Any] = {
                "gregorian": {  # 公历信息
                    "timestamp": time.time(),
                    "formatted": now.strftime(time_format),
                    "datetime": str(now),
                    "date": {"year": now.year, "month": now.month, "day": now.day},
                    "time": {"hour": now.hour, "minute": now.minute, "second": now.second}
                },
                "lunar": {  # 农历信息
                    "year": lunar.lunar_year,
                    "month": lunar.lunar_month,
                    "day": lunar.lunar_day,
                    "formatted": lunar.chinese()  # 中文格式化
                }
            }

            
            return ToolResult(output=str(result))
        
        except Exception as e:
            print(e)
            return ToolResult(error=f"获取日历时间失败: {str(e)}")

if __name__ == "__main__":
    import asyncio
    
    async def test() -> None:
        tool: CalendarTool = CalendarTool()
        result: ToolResult = await tool.execute(format="%Y年%m月%d日 %H:%M:%S")
        print(result.output)
        
    asyncio.run(test())
