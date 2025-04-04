# 🌟 ManuSphere 的 Hackathon 作品！🌟

<br>

## 👥 队伍介绍

<div style="background-color: #FFD166; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
来自<b>北大</b>，<b>人大高瓴</b>，<b>北理</b>的大一&大二同学共同开发的 <span style="color: #FF6B6B; font-weight: bold;">OpenManus tool</span>

为<span style="color: #06D6A0; font-weight: bold;">开源</span>，为<span style="color: #118AB2; font-weight: bold;">AGI</span>，为<span style="color: #EF476F; font-weight: bold;">共同的极客精神</span>！

</div>

## 🚀 3 天开发成果

### 🎨 卡片生成工具 md2card

<div style="border: 3px solid #FF6B6B; padding: 10px; border-radius: 15px; margin-bottom: 20px;">
<p>测试语句：为我生成一张大奖章基金的波普风格卡片，保存在本地</p>

<p>生成结果：</p>

<img src="./workspace/1743692028342_8321kq.png" alt="大奖章基金波普风格卡片" style="max-width: 100%; border-radius: 10px; border: 2px dashed #06D6A0;"/>

<p>对比过去单纯使用 python_execute 工具生成的卡片：</p>

<img src="./workspace\48738d5447c9cac015145d2d904b2cc.png" alt="不知生成的什么东西" style="max-width: 100%; border-radius: 10px; border: 2px dashed #FF6B6B;"/>

<p>生成全过程，一共调用 8 次便可以生成精美卡片：</p>

<img src="./workspace\OpenManus生成效果演示-卡片生成.mp4" alt="OpenManus生成效果演示" style="max-width: 100%; border-radius: 10px;"/>
</div>

### ✨ 功能特点

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px;">
  <div style="background-color: #FFD166; padding: 15px; border-radius: 10px;">
    <h4 style="color: #073B4C; margin-top: 0;">🎭 多样风格</h4>
    <p>支持十余种种卡片风格：波普风格、苹果备忘录风格、小红书风格</p>
  </div>

  <div style="background-color: #06D6A0; padding: 15px; border-radius: 10px;">
    <h4 style="color: #073B4C; margin-top: 0;">💾 自动保存</h4>
    <p>自动下载并保存生成的图片</p>
  </div>

  <div style="background-color: #118AB2; padding: 15px; border-radius: 10px;">
    <h4 style="color: #FFFFFF; margin-top: 0;">🖥️ 简单易用</h4>
    <p>简单易用的命令行和 Web 界面</p>
  </div>

  <div style="background-color: #EF476F; padding: 15px; border-radius: 10px;">
    <h4 style="color: #FFFFFF; margin-top: 0;">📝 Markdown 支持</h4>
    <p>自动根据初始提示词撰写 Markdown 文档</p>
  </div>
</div>

#### 📋 ToDo

- 🎨 添加更多样式
- 🖼️ 在 Web 前端中允许显示生成卡片

### 🔧 精准调用工具执行优化

<div style="background-color: #F8F9FA; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #FF6B6B;">
<p><b>痛点：</b>生成卡片过程中经常出现调用 Web，试图使用 Canvas 等网站制作卡片的情况</p>

<p><b>解决方案:</b>添加 tool_guide 工具，根据关键词检索调用最符合工具执行任务</p>

```python
search_keywords = ["搜索", "查找", "了解", "信息", "寻找", "search", "find", "look up"]
browser_keywords = ["网站", "网页", "浏览", "访问", "网址", "url", "website", "browser"]
code_keywords = ["代码", "编程", "运行", "执行", "计算", "code", "program", "execute", "calculate"]
file_keywords = ["文件", "保存", "读取", "表格", "file", "save", "read", "excel"]
card_keywords = ["卡片", "生成", "创建", "card", "generate", "create","md2card","图片","图片生成","风格"]
time_keywords = ["时间", "日期", "年份", "月份", "日历", "农历", "黄历", "calendar", "time", "date", "year", "month", "day"]
weather_keywords = ["天气", "温度", "湿度", "风力", "风向", "天气预报", "weather", "temperature", "humidity", "wind", "wind direction", "weather forecast"]

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
```

</div>

### ☀️ 天气&日期工具

<div style="background-color: #F8F9FA; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #06D6A0;">
<p><b>痛点：</b>在使用过程中经常发现调用假日期，假天气，假地点</p>

<p><b>解决方案：</b>接入专门 API，用于提供精确的日期、天气和地点</p>

<p>代码位置：tool 文件夹中的 time, weather, place 工具</p>
</div>

## 💖 感谢

<div style="background-color: #FFD166; padding: 20px; border-radius: 10px; margin-top: 20px;">
<p>感谢 OpenManus 团队组织本次黑客松，是 OpenManus 的开源才有我们得以发挥的空间</p>

<p>感谢我的两名队友，他们在开发过程中提供了宝贵的建议以及不可或缺的帮助</p>

<p>我们深知技术有限，尚有很大提升空间，但依然希望能尽微薄之力帮助完善 OpenManus</p>

<p>未来会继续优化！希望 OpenManus 越做越好，做真正开源的 Manus！</p>
</div>
