
import json
from datetime import datetime
import os
import re

import json
import os
from datetime import datetime

import requests

def on_change(self, widget=None):
    

    def auto_complete_keyword_logic():
        self_inp_keyword_value = None  # 在这里初始化变量
        content_value = self.inp_content.value

        keywords_data = self.sheet_data_json

        # 遍历所有类别
        for category in keywords_data.values():
            for item in category:
                # 检查普通关键词，确保'inp_content'键存在
                if 'inp_content' in item and not self.inp_keyword.value:
                    if any(keyword in content_value for keyword in item["inp_content"]):
                        # self.inp_keyword.value = item["keyword"]
                        self_inp_keyword_value = item["keyword"]
                        break
       
            
        if self_inp_keyword_value:
            if self_inp_keyword_value == "就餐记录":
            
                current_hour = datetime.now().hour
                if 6 <= current_hour < 11:
                    self_inp_keyword_value = '早餐'
                elif 11 <= current_hour < 15:
                    self_inp_keyword_value = '中餐'
                elif 15 <= current_hour <= 23:
                    self_inp_keyword_value = '晚餐'
                elif 0 <= current_hour < 6:
                    self_inp_keyword_value = '夜餐'
                    
            self.inp_keyword.value = self_inp_keyword_value
    auto_complete_keyword_logic()

    def handle_url(content):
        # 查找 URL
        start_pos = -1
        for substring in ['http://', 'https://', 'www.']:
            start_pos = content.find(substring)
            if start_pos != -1:
                break

        if start_pos == -1:
            return content  # 没有找到网址，返回原文本

        # 提取 URL
        end_pos = len(content)
        # 定义一个用于检测网址结束的字符集合，包括空格和中文全角标点符号
        stop_chars = [' ', '，', '。', '！', '？', '；', '：', '“', '”', '（', '）', '、', '《', '》', '—']
        for i in range(start_pos, len(content)):
            if content[i] in stop_chars or '\u4e00' <= content[i] <= '\u9fff':  # 检查是否是中文字符
                end_pos = i
                break

        url = content[start_pos:end_pos]

        # 设置请求头部，模仿常见浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Origin': 'https://www.google.com'
        }

        # 获取网址标题
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                start = response.text.find('<title>') + 7
                end = response.text.find('</title>', start)
                title = response.text[start:end].strip()
            else:
                title = f'无法获取标题，状态码：{response.status_code}'
        except Exception as e:
            title = f'获取标题时出错：{e}'

        # 返回格式化的字符串
        return f"{content}：{title}"

    
    content_value = handle_url(self.inp_content.value)
    # picture_status_value = getattr(self, 'picture_status', None)
    picture_status_value = self.picture_status.value

    if self.inp_keyword.value:
        keyword_value = self.inp_keyword.value
        # if keyword_value in ["v", "hy", "kg", "ab"]: # 转大写
            # keyword_value = keyword_value.upper()

        keyword_left = f'[{keyword_value}['
        keyword_left = keyword_left.replace("，", "[").replace("。", "[").replace("、", "[").replace("]", "[").replace("/", "[")

        keyword_right = f']{keyword_value}]'
        keyword_right = keyword_right.replace("，", "]").replace("。", "]").replace("、", "]").replace("[", "]").replace("/", "]")
    else:
        keyword_left = ''
        keyword_right = ''

    # 检查规划冒号逻辑
    if "规划" in keyword_left:
        if "：：" in content_value:
            pass
        else:
            content_value = content_value.replace("：", "：：", 1)

    if "规划" in keyword_left:
        # 本逻辑为: 防止中括号和大括号出现在内容中, 以免影响可分析性
        picture_status_value = picture_status_value.replace('[', '(').replace('{', '(').replace(']', ')').replace('}', ')')
        content_value = content_value.replace('[', '(').replace('{', '(').replace(']', ')').replace('}', ')')

    # 检查图片标识逻辑
    if "支出" in keyword_left or "规划" in keyword_left:
        formatted_value = f'{content_value} {picture_status_value}' if picture_status_value else content_value
    else:
        formatted_value = f'{picture_status_value} {content_value}' if picture_status_value else content_value

    # 组合最终的格式化值
    def format_value(keyword_left, formatted_value, keyword_right):

        # ↓↓↓检查支出逻辑↓↓↓
        # 检查keyword_left是否包含"支出" [支出]
        if "支出" in keyword_left:
            # 使用正则表达式提取数字和文本部分
            match = re.match(r"(\d+(\.\d+)?)(.*)", formatted_value)
            if match:
                # 将数字和文本部分分别提取出来
                numbers = match.group(1)
                text = match.group(3)
                # 按新格式组合
                return f"{keyword_left}{numbers}{keyword_right}{text}"
        # 如果不包含"支出"或者没有匹配到格式，返回原始格式
        return f"{keyword_left}{formatted_value}{keyword_right}"
        # ↑↑↑检查支出逻辑↑↑↑
    
    result = format_value(keyword_left, formatted_value, keyword_right)
    if '[规划[' in result:
        result = r'{}' + result

    self.inp_line.value = result


    # 检测文本判断执行
    """if "。。" in formatted_value:
        self.inp_line.focus()"""

class on_press:

    @staticmethod
    def clear(self, widget):
        # 01162244 修改clear按钮为：Clear改为简单的清空keyword中的内容，不执行焦点转移操作

        back_content = self.inp_line.value #保持inp_line不变
        
        #如果inp_keywordh和inp_content为空 (意为三次点击)：将inp_line内容清空
        if self.inp_keyword.value == '' and self.inp_content.value == '':
            self.inp_line.value = ''
            back_content = ''

        """#如果inp_keyword为空 (意为二次点击)：将inp_content内容清空
        if self.inp_keyword.value == '':
            self.inp_content.value = ''

        #如果什么都不判定 (意为首次点击)：将inp_keyword内容清空
        self.inp_keyword.value = ''"""

        #如果inp_content为空 (意为二次点击)：将inp_keyword内容清空
        if self.inp_content.value == '':
            self.inp_keyword.value = ''

        #如果什么都不判定 (意为首次点击)：将inp_content内容清空
        self.inp_content.value = ''

        self.inp_line.value = back_content #保持inp_line不变
    
    @staticmethod
    def clear_keyword(self, widget):
        # 01162244 修改clear按钮为：Clear改为简单的清空keyword中的内容，不执行焦点转移操作

        back_content = self.inp_line.value #保持inp_line不变
        
        #如果inp_keywordh和inp_content为空 (意为三次点击)：将inp_line内容清空
        if self.inp_keyword.value == '' and self.inp_content.value == '':
            self.inp_line.value = ''
            back_content = ''

        """#如果inp_keyword为空 (意为二次点击)：将inp_content内容清空
        if self.inp_keyword.value == '':
            self.inp_content.value = ''

        #如果什么都不判定 (意为首次点击)：将inp_keyword内容清空
        self.inp_keyword.value = ''"""

        #如果inp_content为空 (意为二次点击)：将inp_keyword内容清空
        if self.inp_keyword.value == '':
            self.inp_content.value = ''

        #如果什么都不判定 (意为首次点击)：将inp_content内容清空
        self.inp_keyword.value = ''

        self.inp_line.value = back_content #保持inp_line不变

class on_lose_focus:
    @staticmethod
    def inp_keyword(self, widget=None):
        if self.inp_keyword.value != '':
            self.inp_keyword.value = self.inp_keyword.value.replace("，", "/").replace("。", "/").replace("、", "/").replace("[", "/")

        def auto_complete_keyword_logic():
            self_inp_keyword_value = None  # 在这里初始化变量
            keyword_value = self.inp_keyword.value

            keywords_data = self.sheet_data_json

            # 遍历所有类别
            for category in keywords_data.values():
                for item in category:
                    # 检查普通关键词，确保'inp_content'键存在
                    if 'inp_keyword' in item:
                    # if 'inp_keyword' in item and not self.inp_keyword.value:
                        if any(keyword == keyword_value for keyword in item["inp_keyword"]):
                            # self.inp_keyword.value = item["keyword"]
                            self_inp_keyword_value = item["keyword"]
                            break
        
                
            
            if self_inp_keyword_value:
                self.inp_keyword.value = self_inp_keyword_value
        auto_complete_keyword_logic()


    @staticmethod
    def inp_content(self, widget=None):
        if (self.inp_keyword.value == ''
                and self.inp_content.value == ''
                and "图片写入中..." not in self.inp_line.value):
            
            if self.inp_line.value != self.last_inp_line_value:
                self.inp_content.value = self.inp_line.value
        
        if widget == self.inp_keyword:
            self.rewrite_keywords_json(widget)
            
