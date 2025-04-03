"""工具选择指南提示词。"""

TOOL_SELECTION_GUIDE = """
# OpenManus 工具选择指南

请根据用户的请求类型选择最合适的工具：

## 搜索和信息获取类任务
- 使用 `web_search` 工具直接进行网络搜索
  - 示例: web_search(query="最新AI技术发展")
  - 适用场景: 查找事实信息、新闻、最新发展等

## 网页浏览和交互
- 使用 `browser_use` 工具进行网页浏览和交互
  - 示例: browser_use(action="go_to_url", url="https://example.com")
  - 适用场景: 访问网站、点击按钮、填写表单、提取网页内容

## 文件和代码操作
- 使用 `python_execute` 工具执行Python代码
  - 示例: python_execute(code="import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())")
  - 适用场景: 数据处理、文件操作、编程任务

## 数学计算
- 使用 `calculator` 工具进行复杂数学计算
  - 示例: calculator(expression="(2 + 3) * 4 / 2")
  - 适用场景: 需要精确计算结果的场合

## 卡片生成
- 使用 `md2card` 工具生成卡片
  - 示例: md2card(content="你好，世界！")
  - 适用场景: 需要生成美观的卡片，如名片、日历、待办事项等

## 日历查询
- 使用 `calendar` 工具查询日历信息
  - 示例: calendar(query="2024年1月1日是星期几")
  - 适用场景: 需要查询特定日期或农历信息

## 天气查询
- 使用 `weather` 工具查询天气信息
  - 示例: weather(city_code="101010100")
  - 适用场景: 需要查询特定城市或地区的天气信息

## 任务完成
- 完成全部任务后使用 `terminate` 工具结束流程
  - 示例: terminate(reason="Task completed successfully")

关键原则:
1. 始终选择一个工具而不是仅仅描述计划
2. 选择最直接解决问题的工具，避免不必要的规划
3. 复杂任务分解为多个简单步骤，每步使用最合适的工具
4. 搜索相关任务必须立即使用搜索工具，不要过度规划
"""

def get_tool_selection_prompt(message: str) -> str:
    """
    基于用户消息生成工具选择提示。

    Args:
        message: 用户的消息内容

    Returns:
        工具选择提示字符串
    """
    # 分析消息中的关键词来确定可能的工具
    search_keywords = ["搜索", "查找", "了解", "信息", "寻找", "search", "find", "look up"]
    browser_keywords = ["网站", "网页", "浏览", "访问", "网址", "url", "website", "browser"]
    code_keywords = ["代码", "编程", "运行", "执行", "计算", "code", "program", "execute", "calculate"]
    file_keywords = ["文件", "保存", "读取", "表格", "file", "save", "read", "excel"]
    card_keywords = ["卡片", "生成", "创建", "card", "generate", "create","md2card","图片","图片生成","风格"]
    time_keywords = ["时间", "日期", "年份", "月份", "日历", "农历", "黄历", "calendar", "time", "date", "year", "month", "day"]
    weather_keywords = ["天气", "温度", "湿度", "风力", "风向", "天气预报", "weather", "temperature", "humidity", "wind", "wind direction", "weather forecast"]
    place_keywords = ["地点", "位置", "地址", "地点", "位置", "地址", "place", "location", "address"]

    suggested_tools = []

    if any(kw in message.lower() for kw in search_keywords):
        suggested_tools.append("web_search")

    if any(kw in message.lower() for kw in browser_keywords):
        suggested_tools.append("browser_use")

    if any(kw in message.lower() for kw in code_keywords):
        suggested_tools.append("python_execute")

    if any(kw in message.lower() for kw in file_keywords):
        suggested_tools.append("python_execute")

    if any(kw in message.lower() for kw in card_keywords):
        suggested_tools.append("md2card")

    if any(kw in message.lower() for kw in time_keywords):
        suggested_tools.append("calendar")

    if any(kw in message.lower() for kw in weather_keywords):
        suggested_tools.append("weather")

    if any(kw in message.lower() for kw in place_keywords):
        suggested_tools.append("place")

    # 如果没有明确的工具建议，建议使用web_search作为首选
    if not suggested_tools:
        suggested_tools.append("web_search")

    # 构建特定的工具提示
    tool_prompt = f"""
    基于您的请求: "{message[:100]}{'...' if len(message) > 100 else ''}"

    建议的工具: {', '.join(suggested_tools)}

    请立即使用上述工具之一执行具体操作，而不是继续规划。
    """

    return TOOL_SELECTION_GUIDE + "\n" + tool_prompt
