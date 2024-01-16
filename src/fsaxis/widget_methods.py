def on_lose_focus(self):
    # self.
    pass

def on_change(self, widget=None):
    def handle_url(content):
        # 使用更高效的方式来检查 URL
        if any(substring in content for substring in ['http://', 'https://', 'www.']):
            return content + ' '
        return content

    def auto_complete_keyword_logic():
        
        content_value = handle_url(self.inp_content.value) #提取content值
        
        # 简单判断
        if not self.inp_keyword.value and any(keyword in content_value for keyword in ['维生素', '眼药水', 'eds', 'EDS', '甲硝唑凝胶', '甲硝']):
            self.inp_keyword.value = '日常药品'
        if not self.inp_keyword.value and any(keyword in content_value for keyword in ['瑜伽', '眼保健操', '瑜伽', '瑜伽', '瑜伽', '瑜伽']):
            self.inp_keyword.value = '室内运动'
        if not self.inp_keyword.value and any(keyword in content_value for keyword in ['跑步', '跑步', '跑步', '跑步', '跑步', '跑步']):
            self.inp_keyword.value = '户外运动'
        
        # 简单判断 + 时间判断
        food_keywords = ['鸡腿', '汉堡', '汉堡包', '米饭', '韭菜面', '溜溜梅', '吉香居酸豆角', '旺仔牛奶', '鸭掌', '火鸡面', 
                    '牛肉串', '天地一号', '柚子', '小辣条', '可乐', '鸡蛋葱面', '八宝粥', '橙子', '肯德基全鸡', 
                    '团购券', '鸡米花', '面包', '卡士酸奶', '乌江榨菜']

        if not self.inp_keyword.value and any(keyword in content_value for keyword in food_keywords):
            from datetime import datetime
            current_hour = datetime.now().hour
            if 6 <= current_hour < 11:
                self.inp_keyword.value = '早餐'
            elif 11 <= current_hour < 15:
                self.inp_keyword.value = '中餐'
            elif 15 <= current_hour <= 23:
                self.inp_keyword.value = '晚餐'
            elif 0 <= current_hour < 6:
                self.inp_keyword.value = '夜餐'

        return content_value

    content_value = auto_complete_keyword_logic()
    # picture_status_value = getattr(self, 'picture_status', None)
    picture_status_value = self.picture_status.value

    if self.inp_keyword.value:
        keyword_value = self.inp_keyword.value
        if keyword_value in ["v", "hy", "kg", "ab"]: # 转大写
            keyword_value = keyword_value.upper()

        keyword_left = f'[{keyword_value}['
        keyword_left = keyword_left.replace("，", "[").replace("。", "[").replace("]", "[")

        keyword_right = f']{keyword_value}]'
        keyword_right = keyword_right.replace("，", "]").replace("。", "]").replace("[", "]")
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