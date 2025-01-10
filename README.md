# comicReader
可按元数据分类并搜索本地漫画，避免本地漫画一大堆不知道该看啥
# 漫画标签分类器

## 项目描述
这是一个用于漫画压缩包分类的应用程序。它从压缩包中的 XML 文件中提取标签，按分类显示并提供搜索功能。每个漫画的封面将显示为压缩包中的第一张图片。

## 功能特性
- 从漫画压缩包中的 XML 文件中提取标签。
- 按标签分类显示漫画，并提供搜索功能。
- 显示每个漫画的封面图。
- 支持选择漫画文件夹并自动加载其中的压缩包。

## 技术栈
- Python 3.x
- tkinter (用于图形界面)
- zipfile (用于解压缩文件)
- Pillow (用于图像处理)
- xml.etree.ElementTree (用于解析 XML 文件)

## 安装与运行

1. 克隆或下载项目代码：
   ```bash
   git clone https://github.com/your-username/project-name.git

2. 创建并激活虚拟环境：
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .\.venv\Scripts\activate   # Windows

3. 安装项目依赖：
    pip install -r requirements.txt

4. 运行应用：
    python app.py

5. 选择包含漫画压缩包的文件夹，程序会自动加载其中的文件。