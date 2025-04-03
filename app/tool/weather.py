import requests
from typing import Dict, Optional, Any
from app.tool.base import BaseTool, ToolResult

class WeatherTool(BaseTool):
    """天气工具
    
    提供获取当地天气信息的工具方法
    """
    
    name:str = "weather"
    description: str= "获取当地天气信息的工具"
    parameters:Dict[str, Any] = {
        "type": "object",
        "properties": {
            "city_code": {
                "type": "string", 
                "description": "城市代码,如101010100代表北京",
                "default": "101010100",
                "required": True
            }
        }
    }

    # 天气API配置
    
    async def execute(self, **kwargs) -> ToolResult:
        """执行天气信息获取
        
        Args:
            city_code: 城市代码,默认为北京(101010100)
            
        Returns:
            ToolResult: 包含天气信息的结果
        """
        try:
            # 获取城市代码参数
            API_URL:str = "http://t.weather.sojson.com/api/weather/city/{}"

            city_code = kwargs.get("city_code", "101010100")
            
            # 调用天气API
            url:str = API_URL.format(city_code)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            
            if weather_data['status'] != 200:
                raise Exception(weather_data['message'])
                
            # 解析天气数据
            data = weather_data['data']
            forecast = data['forecast'][0]  # 获取今日天气预报
            
            # 构造返回结果
            result:Dict[str, Any] = {
                "current": {
                    "temperature": data['wendu'],  # 当前温度
                    "humidity": data['shidu'],  # 湿度
                    "air_quality": data['quality'],  # 空气质量
                    "pm25": data['pm25'],  # PM2.5
                    "pm10": data['pm10']  # PM10
                },
                "forecast": {
                    "date": forecast['ymd'],  # 日期
                    "week": forecast['week'],  # 星期
                    "type": forecast['type'],  # 天气类型
                    "high": forecast['high'],  # 最高温
                    "low": forecast['low'],  # 最低温
                    "wind_direction": forecast['fx'],  # 风向
                    "wind_level": forecast['fl'],  # 风级
                    "notice": forecast['notice']  # 天气提示
                },
            }
            
            return ToolResult(output=str(result))
            
        except Exception as e:
            return ToolResult(error=f"获取天气信息失败: {str(e)}")

if __name__ == "__main__":
    import asyncio
    
    async def test():
        tool = WeatherTool()
        result = await tool.execute(city_code="101020100")  # 上海的城市代码
        print(result.output)
        
    asyncio.run(test())
