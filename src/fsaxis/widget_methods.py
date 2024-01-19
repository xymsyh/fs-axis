
import json
from datetime import datetime
import os

import json
import os
from datetime import datetime

def on_change(self, widget=None):
    

    def auto_complete_keyword_logic():
        content_value = self.inp_content.value

        # 从JSON文件中读取关键词
        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'json_keywords.json')
        with open(config_path, 'r', encoding='utf-8') as file:
            keywords_data = json.load(file)

        # 遍历所有类别
        for category in keywords_data.values():
            for item in category:
                # 检查普通关键词，确保'inp_content'键存在
                if 'inp_content' in item and not self.inp_keyword.value:
                    if any(keyword in content_value for keyword in item["inp_content"]):
                        # self.inp_keyword.value = item["keyword"]
                        self_inp_keyword_value = item["keyword"]
                        break
       
            
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
        if keyword_value in ["v", "hy", "kg", "ab"]: # 转大写
            keyword_value = keyword_value.upper()

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
    self.inp_line.value = f'{keyword_left}{formatted_value}{keyword_right}'


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

class on_lose_focus:
    @staticmethod
    def inp_keyword(self, widget=None):
        if self.inp_keyword.value != '':
            self.inp_keyword.value = self.inp_keyword.value.replace("，", "/").replace("。", "/").replace("[", "/")

    @staticmethod
    def inp_content(self, widgett=None):
        if (self.inp_keyword.value == ''
                and self.inp_content.value == ''
                and "图片写入中..." not in self.inp_line.value):
            self.inp_content.value = self.inp_line.value
            
