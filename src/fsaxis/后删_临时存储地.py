def change_content(self, widget):
    # 定义一个帮助函数来检查并处理 URL
    def handle_url(content):
        if 'http://' in content or 'https://' in content or 'www.' in content:
            return content + ' '
        return content

    # 检查 inp_content 是否存在并且有值
    if hasattr(self, 'inp_content') and self.inp_content.value:
        content_value = handle_url(self.inp_content.value)

        # 检查关键字是否为空，并检查内容中是否包含特定的医药关键字
        if not self.inp_keyword.value:
            if any(keyword in content_value for keyword in ['维生素', '眼药水', 'eds', 'EDS', '甲硝唑凝胶', '甲硝']):
                self.inp_keyword.value = '日常药品'

        # 根据是否存在 inp_keyword 和 picture_status 来格式化 inp_line 的值
        if hasattr(self, 'picture_status') and self.picture_status.value:
            if self.inp_keyword.value:
                formatted_value = f'[{self.inp_keyword.value}[{self.picture_status.value} {content_value}]{self.inp_keyword.value}]'
            else:
                formatted_value = f'{self.picture_status.value} {content_value}'
        else:
            if self.inp_keyword.value:
                formatted_value = f'[{self.inp_keyword.value}[{content_value}]{self.inp_keyword.value}]'
    else:
        formatted_value = content_value

self.inp_line.value = formatted_value
