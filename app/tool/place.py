import requests
from app.tool.base import BaseTool, ToolResult
from typing import Optional, Dict, Any

class PlaceTool(BaseTool):
    """地点工具
    
    提供获取用户所在地信息的工具方法
    """
    
    name: str = "place"
    description: str = "获取用户所在地信息的工具"
    parameters:Dict[str, Any ] = {
        "type": "object",
        "properties": {
            "ip": {
                "type": "string",
                "description": "IP地址,默认使用当前IP",
                "default": None 
            }
        }
    }

    # IP定位API配置 
    API_URL:str = "https://ipapi.co/{}/json/"

    async def execute(self, **kwargs: Any) -> ToolResult:
        """执行地点信息获取
        
        Args:
            ip: IP地址,默认使用当前IP
            
        Returns:
            ToolResult: 包含地点信息的结果
        """
        try:
            # 获取IP参数
            # 优先使用传入的IP参数,如果没有则获取当前IP
            ip: str = kwargs.get("ip")
            if not ip:
                try:
                    # 通过900cha获取当前IP
                    import re
                    # 向网站发送请求获取公网IP
                    response = requests.get('http://myip.ipip.net', timeout=5)
                    public_ip = response.text# 使用正则表达式提取IP地址
                    public_ip = re.search(r'(\d{1,3}\.){3}\d{1,3}', public_ip).group()
                    # 返回的是纯文本格式的IP地址
                    ip:str= public_ip
                except:
                    raise Exception("无法获取当前IP地址")
                    
            if not ip:
                raise Exception("无法获取当前IP地址")
            # return ToolResult(output=str(ip))
            # 调用IP定位API
            # 构造API请求URL
            url: str = self.API_URL.format(ip)
            # 发送GET请求获取位置信息
            headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
            ,'Referer':'https://ipapi.co/36.112.3.49/json/'}
            response = requests.get(url, timeout=10,headers=headers)
            # 检查响应状态
            response.raise_for_status()
            # 解析JSON响应数据
            location_data = response.json()
            
            # 构造返回结果
            result:Dict[str,Any] = {
                "ip": location_data["ip"],
                "location": {
                    "country": location_data["country_name"],  # 国家
                    "region": location_data["region"],  # 地区/省份
                    "city": location_data["city"],  # 城市
                    "latitude": location_data["latitude"],  # 纬度
                    "longitude": location_data["longitude"]  # 经度
                },
                "network": {
                    "asn": location_data["asn"],  # ASN编号
                    "org": location_data["org"],  # 运营商
                },
                "timezone": location_data["timezone"],  # 时区
                "currency": location_data["currency"]  # 货币
            }
            
            return ToolResult(output=str(result))
            
        except Exception as e:
            print(e)
            return ToolResult(error=f"获取地点信息失败: {str(e)}")

if __name__ == "__main__":
    import asyncio
    
    async def test():
        tool = PlaceTool()
        result = await tool.execute()
        print(result.output)
        
    asyncio.run(test())
