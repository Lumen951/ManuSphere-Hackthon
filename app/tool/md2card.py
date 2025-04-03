import re
import requests
import json
import time
import sys
from typing import Optional
import os
import urllib.parse

from app.tool.base import BaseTool, ToolResult


class MD2Card(BaseTool):
    """
    将Markdown内容转换为卡片格式的工具

    使用Coze API将Markdown文本转换为结构化的卡片格式
    """
    name: str = "md2card"
    description: str = """将Markdown内容转换为卡片格式。
    此工具接收Markdown格式的文本，并将其转换为结构化的卡片格式，适合在各种平台上展示。
    可以处理标题、列表、代码块等Markdown元素，并生成美观的卡片布局。
    """
    parameters: dict = {
        "type": "object",
        "properties": {
            "markdown_text": {
                "type": "string",
                "description": "(必填) 需要转换为卡片格式的Markdown文本内容",
            },
            "card_style": {
                "type": "string",
                "description": "(可选) 卡片样式，可选择多种风格",
                "enum": [
                    "apple-notes", "pop-art", "art-deco", "glassmorphism",
                    "warm", "minimal", "dreamy", "nature", "xiaohongshu",
                    "notebook", "darktech", "typewriter", "watercolor",
                    "traditional-chinese", "fairytale", "business",
                    "japanese-magazine", "minimalist", "cyberpunk",
                    "simple", "detailed", "compact"
                ],
                "default": "apple-notes"
            }
        },
        "required": ["markdown_text"],
    }

    # Coze API相关配置
    _personal_access_token: str = "pat_KfHunzX2xz4mJbEhd1iORYjPfyzoMTlsQgHTCja56bqPfEZRAq8YgKeudxX1AWDY"
    _bot_id: str = "7488532057853968424"
    _user_id: str = "7420009541439471650"
    _api_base_url: str = "https://api.coze.cn/v3/chat"

    async def execute(
        self,
        markdown_text: str,
        card_style: Optional[str] = "apple-notes"
    ) -> ToolResult:
        """
        执行Markdown到卡片的转换

        Args:
            markdown_text: 需要转换的Markdown文本
            card_style: 卡片样式，默认为apple-notes

        Returns:
            ToolResult: 包含转换结果或错误信息
        """
        try:
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {self._personal_access_token}",
                "Content-Type": "application/json"
            }

            # 构建消息内容
            message = [
                {
                    "role": "user",
                    "type": "question",
                    "content": f"请将以下Markdown内容转换为{card_style}风格的卡片格式:\n\n{markdown_text}",
                    "content_type": "text"
                }
            ]

            # 构建请求体
            payload = {
                "bot_id": self._bot_id,
                "user_id": self._user_id,
                "stream": True,
                "auto_save_history": False,
                "additional_messages": message
            }

            # 发送请求
            response = requests.post(self._api_base_url, headers=headers, json=payload)

            # 处理响应
            result = ""
            image_urls = []

            for line in response.iter_lines():
                decoded_line = line.decode('utf-8', errors='ignore')

                if decoded_line.startswith("data:"):
                    try:
                        event_data = json.loads(decoded_line[5:])
                        if "content" in event_data:
                            result += event_data["content"]

                            # 尝试从内容中提取图片URL
                            urls = self._extract_image_urls(event_data["content"])
                            if urls:
                                image_urls.extend(urls)
                    except json.JSONDecodeError:
                        continue

            # 下载图片
            saved_images = []
            for url in image_urls:
                try:
                    saved_path = self._download_image(url)
                    saved_images.append(saved_path)
                except Exception as e:
                    result += f"\n下载图片失败 ({url}): {str(e)}"

            # 添加下载信息到结果
            if saved_images:
                result += f"\n\n已保存 {len(saved_images)} 张图片到当前文件夹:"
                for path in saved_images:
                    result += f"\n- {path}"

            return ToolResult(output=result)

        except Exception as e:
            return ToolResult(error=f"转换Markdown到卡片格式失败: {str(e)}")

    def _extract_image_urls(self, text):
        """从文本中提取图片URL"""
        # 提取markdown格式的图片链接 ![...](url)
        markdown_pattern = r'!\[.*?\]\((https?://[^\s)]+)\)'
        markdown_urls = re.findall(markdown_pattern, text)

        # 提取HTML格式的图片链接 <img src="url">
        html_pattern = r'<img\s+[^>]*src="(https?://[^"]+)"[^>]*>'
        html_urls = re.findall(html_pattern, text)

        # 提取JSON中的图片URL
        json_pattern = r'"url"\s*:\s*"(https?://[^"]+)"'
        json_urls = re.findall(json_pattern, text)

        # 合并所有找到的URL
        all_urls = markdown_urls + html_urls + json_urls

        # 去重
        return list(set(all_urls))

    def _download_image(self, url):
        """下载图片并保存到当前文件夹"""
        # 从URL中提取文件名
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # 如果文件名为空或无效，生成一个基于时间戳的文件名
        if not filename or len(filename) < 5:
            timestamp = int(time.time() * 1000)
            filename = f"image_{timestamp}.png"

        # 下载图片
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
        else:
            raise Exception(f"下载失败，状态码: {response.status_code}")

    async def cleanup(self):
        """清理资源，确保即使工具失败也能正确关闭相关资源"""
        pass


