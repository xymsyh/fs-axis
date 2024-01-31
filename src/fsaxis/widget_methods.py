
import json
from datetime import datetime
import os
import re


import json
import os
from datetime import datetime

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
        # 使用更高效的方式来检查 URL
        if any(substring in content for substring in ['http://', 'https://', 'www.']):
            return content + ' '
        return content
    
    content_value = handle_url(self.inp_content.value)
    # picture_status_value = getattr(self, 'picture_status', None)
    picture_status_value = self.picture_status.value

    if self.inp_keyword.value:
        keyword_value = self.inp_keyword.value
        # if keyword_value in ["v", "hy", "kg", "ab"]: # 转大写
            # keyword_value = keyword_value.upper()

        keyword_left = f'[{keyword_value}['
        keyword_left = keyword_left.replace("，", "[").replace("。", "[").replace("]", "[").replace("/", "[")

        keyword_right = f']{keyword_value}]'
        keyword_right = keyword_right.replace("，", "]").replace("。", "]").replace("[", "]").replace("/", "]")
    else:
        keyword_left = ''
        keyword_right = ''

    # 简化条件逻辑
    formatted_value = f'{picture_status_value} {content_value}' if picture_status_value else content_value

    # 组合最终的格式化值
    def format_value(keyword_left, formatted_value, keyword_right):
        # 检查keyword_left是否包含"支出"
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
    
    result = format_value(keyword_left, formatted_value, keyword_right)
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
            self.inp_keyword.value = self.inp_keyword.value.replace("，", "/").replace("。", "/").replace("[", "/")

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
    def inp_content(self, widgett=None):
        if (self.inp_keyword.value == ''
                and self.inp_content.value == ''
                and "图片写入中..." not in self.inp_line.value):
            self.inp_content.value = self.inp_line.value
            
