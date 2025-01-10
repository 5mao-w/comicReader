import os
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
import io

class ComicClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("漫画标签分类器")
        self.root.geometry("800x600")

        # 存储压缩包及其标签的字典
        self.comics = {}

        # 创建搜索框
        self.search_label = tk.Label(root, text="搜索标签:")
        self.search_label.pack(pady=5)
        
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(root, text="搜索", command=self.search_comics)
        self.search_button.pack(pady=5)

        # 创建标签列表框
        self.tag_list_label = tk.Label(root, text="标签分类:")
        self.tag_list_label.pack(pady=5)

        self.tag_listbox = tk.Listbox(root, height=10, width=50)
        self.tag_listbox.pack(pady=10)
        self.tag_listbox.bind("<<ListboxSelect>>", self.show_comics_by_tag)

        # 创建展示区
        self.result_frame = ttk.Frame(root)
        self.result_frame.pack(pady=10)

    def load_comics_from_folder(self, folder_path):
        """加载文件夹中的所有压缩包及其标签信息"""
        for filename in os.listdir(folder_path):
            if filename.endswith('.zip'):
                zip_path = os.path.join(folder_path, filename)
                self.process_zip_file(zip_path)

    def process_zip_file(self, zip_path):
        """处理压缩包，提取xml标签和封面图片"""
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # 找到xml文件
            xml_files = [f for f in zip_file.namelist() if f.endswith('.xml')]
            if xml_files:
                xml_file = xml_files[0]
                with zip_file.open(xml_file) as xml_f:
                    # 解析xml文件，获取标签
                    tree = ET.parse(xml_f)
                    root = tree.getroot()
                    tags = self.parse_tags_from_xml(root)

                    # 获取漫画封面（假设第一张图片是封面）
                    cover_image = self.get_comic_cover(zip_file)

                    # 保存数据
                    self.comics[zip_path] = {'tags': tags, 'cover_image': cover_image}

                    # 更新标签列表框
                    for tag in tags:
                        if tag not in self.tag_listbox.get(0, tk.END):
                            self.tag_listbox.insert(tk.END, tag)

    def parse_tags_from_xml(self, xml_root):
        """解析xml文件中的标签"""
        tags = []
        for category in xml_root.findall('.//Category'):
            for tag in category.findall('Tag'):
                tags.append(tag.text)
        return tags

    def get_comic_cover(self, zip_file):
        """获取压缩包中的封面图片"""
        image_files = [f for f in zip_file.namelist() if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        if image_files:
            image_file = image_files[0]
            with zip_file.open(image_file) as img_f:
                img_data = img_f.read()
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((100, 100))  # 设置封面图像的大小
                return ImageTk.PhotoImage(img)
        return None

    def search_comics(self):
        """根据输入框中的标签搜索漫画"""
        search_term = self.search_entry.get().lower()
        search_results = []

        for zip_path, comic_data in self.comics.items():
            matched_tags = [tag for tag in comic_data['tags'] if search_term in tag.lower()]
            if matched_tags:
                search_results.append((zip_path, comic_data))

        self.display_comics(search_results)

    def show_comics_by_tag(self, event):
        """根据选择的标签显示漫画"""
        selected_tag = self.tag_listbox.get(tk.ACTIVE)
        filtered_comics = []

        for zip_path, comic_data in self.comics.items():
            if selected_tag in comic_data['tags']:
                filtered_comics.append((zip_path, comic_data))

        self.display_comics(filtered_comics)

    def display_comics(self, comics):
        """根据漫画信息显示网格"""
        # 清空旧的结果显示
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for i, (zip_path, comic_data) in enumerate(comics):
            frame = ttk.Frame(self.result_frame)
            frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            # 显示封面图
            if comic_data['cover_image']:
                cover_label = tk.Label(frame, image=comic_data['cover_image'])
                cover_label.image = comic_data['cover_image']  # 保持对图像的引用
                cover_label.grid(row=0, column=0)

            # 显示漫画文件名
            comic_name = os.path.basename(zip_path)
            comic_name_label = tk.Label(frame, text=comic_name, wraplength=100)
            comic_name_label.grid(row=1, column=0)

# 主程序
def main():
    root = tk.Tk()

    # 创建应用实例
    app = ComicClassifierApp(root)

    # 选择漫画文件夹并加载内容
    folder_path = filedialog.askdirectory(title="选择漫画压缩包文件夹")
    if folder_path:
        app.load_comics_from_folder(folder_path)

    root.mainloop()

if __name__ == "__main__":
    main()
