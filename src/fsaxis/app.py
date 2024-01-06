# app.py 

import sys
from pathlib import Path
def add_project_root_to_sys_path(): # 本行默认收起
    # 获取当前文件的绝对路径  
    current_file_path = Path(__file__).resolve()

    # 获取当前文件的父目录的父目录（即项目根目录）
    project_root = current_file_path.parent

    # 将项目根目录添加到 sys.path
    sys.path.append(str(project_root))
add_project_root_to_sys_path()

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading
import api_methods

import os
print("工作目录 Current working directory:", os.getcwd())

class fsaxis(toga.App):
    def startup(self):
        #region# keywords_box
        self.keywords_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.create_buttons_layout()
        #endregion
        self.scroll_container = toga.ScrollContainer(content=self.keywords_box,style=Pack(height=200))

        #region# main_box
        # Refactored styling for reuse 重构样式以供重用
        row_style = Pack(direction=ROW, padding=5)
        column_style = Pack(direction=COLUMN, padding=0)

        # Creating the main layout box 创建主布局框
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=0))

        # Creating input fields with flex styling 使用 Flex 样式创建输入字段
        self.inp_keyword = toga.TextInput(style=Pack(flex=1), placeholder='keyword')
        self.inp_keyword.on_change = self.change_content
        self.inp_content = toga.TextInput(style=Pack(flex=2), placeholder='content')
        self.inp_content.on_change = self.change_content

        # 创建时区与运行状态
        self.time_zone = toga.TextInput(style=Pack(flex=1), placeholder='time zone')
        self.running_status = toga.TextInput(style=Pack(flex=2), placeholder='status')

        # Creating multi-line input fields 创建多行输入字段
        self.inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=84), placeholder='inp_line')
        self.inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=180), placeholder='inp_cell')

        # Creating buttons 创建按钮
        button_style = {'width': 85, 'padding_top': 20}
        self.btn_line = toga.Button('✅line', style=Pack(**button_style), on_press=self.clk_btn_line)
        self.btn_cell = toga.Button('cell', style=Pack(**button_style), on_press=self.clk_btn_cell)
        button_style = {'width': 85, 'padding_top': 48}
        self.btn_clear = toga.Button('clear', style=Pack(**button_style), on_press=self.clk_btn_clear)

        # Add your new buttons here 新增按钮
        button_style2 = {'width': 85, 'padding_top': 0}
        self.btn_new1 = toga.Button('仅读', style=Pack(**button_style2), on_press=self.on_btn_new1_press)
        self.btn_new2 = toga.Button('历史', style=Pack(**button_style2), on_press=self.on_btn_new1_press)
        self.btn_new3 = toga.Button('B3', style=Pack(**button_style2), on_press=self.on_btn_new1_press)
        self.btn_new4 = toga.Button('B4', style=Pack(**button_style2), on_press=self.on_btn_new1_press)

        # Organizing components into rows and columns 将组件组织成行和列
        row1 = toga.Box(style=row_style, children=[self.inp_keyword, self.inp_content])
        row2 = toga.Box(style=row_style, children=[self.inp_line, self.btn_line])
        col1 = toga.Box(style=column_style, children=[self.btn_cell, self.btn_clear])
        row3 = toga.Box(style=row_style, children=[self.inp_cell, col1])
        row4 = toga.Box(style=row_style, children=[self.time_zone, self.running_status])

        # New row for the new buttons 新按钮的行
        row5 = toga.Box(style=row_style, children=[self.btn_new1, self.btn_new2, self.btn_new3, self.btn_new4])
        # row6 = toga.Box(style=row_style, children=[self.scroll_container])

        # Adding rows to the main layout box 将行添加到主布局框
        self.main_box.add(row4)
        self.main_box.add(row3)
        self.main_box.add(row2)
        self.main_box.add(row1)
        self.main_box.add(row5)
        self.scroll_container.style = Pack(flex=1)

        self.main_box.add(self.scroll_container)
        #endregion

        # Setting up the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    # 定义keywords_box回调函数
    

    def create_buttons_layout(self):
        # 遍历 class_text 字典中的每个类别
        from class_text import class_text
        # 为每个类别的每个按钮创建一个新行
        for category_name, buttons in class_text.items():
            # 创建并添加一个类别标签
            category_label = toga.Label(category_name, style=Pack(padding_bottom=0))
            self.keywords_box.add(category_label)

            # 创建该类别下的所有按钮
            row_box = None
            for i, (button_name, _) in enumerate(buttons):
                # 每四个按钮或在新类别开始时创建一个新行
                if i % 4 == 0 or row_box is None:
                    row_box = toga.Box(style=Pack(direction=ROW, padding=5))
                    self.keywords_box.add(row_box)

                if button_name:  # 确保按钮名称非空
                    button = toga.Button(button_name, style=Pack(width=85), on_press=self.on_button_press)
                    row_box.add(button)

    def on_button_press(self, widget):
        # 更新 inp_keyword 的值为按钮的文本
        self.inp_keyword.value = widget.text
        # self.main_window.content = self.main_box


    def on_btn_new1_press(self, widget):
        # 按钮被按下时激活 inp_keyword 输入框
        self.inp_content.focus()

    # 定义main_box回调函数
    def update_ui_with_result(self, response, full_cell):
        """更新界面元素的值。"""
        self.inp_cell.value = full_cell
        if response:
            self.running_status.value = str(response['msg']) + ": " + str(response['data']['updatedRange'])
        else:
            self.running_status.value = "write_data为空"

    def worker2(self, inp_cell_value):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell = api_methods.write_cell_data(inp_cell_value)
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(response, full_cell))

    def worker(self, inp_line_value):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell = api_methods.write_line_data(inp_line_value)
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(response, full_cell))

    def change_content(self, widget):
        formatted_value = f'[{self.inp_keyword.value}[{self.inp_content.value}]{self.inp_keyword.value}]'
        self.inp_line.value = formatted_value
        if "。。" in formatted_value:
            self.inp_line.focus()

    def clk_btn_line(self, widget):
        """处理按钮点击，启动后台线程。"""
        # formatted_value = f'[{self.inp_keyword.value}[{self.inp_content.value}]{self.inp_keyword.value}]'
        # self.inp_line.value = formatted_value
        formatted_value = self.inp_line.value
        self.running_status.value = "写入中..."
        threading.Thread(target=self.worker, args=(formatted_value,)).start()

    def clk_btn_cell(self, widget):
        formatted_value = self.inp_cell.value

        # 创建确认操作的处理函数
        def on_confirm(widget):
            self.running_status.value = "写入中..."
            threading.Thread(target=self.worker2, args=(formatted_value,)).start()
            self.main_window.content = self.main_box
            

        # 创建取消操作的处理函数
        def on_cancel(widget):
            # self.running_status.value = "操作已取消"
            self.main_window.content = self.main_box

        # 创建确认对话框的内容
        confirm_label = toga.Label('确认写入？')
        confirm_button = toga.Button('确认', on_press=on_confirm)
        cancel_button = toga.Button('取消', on_press=on_cancel)
        confirm_box = toga.Box(children=[confirm_label, confirm_button, cancel_button])

        # 显示确认对话框
        self.main_window.content = confirm_box

    def clk_btn_clear(self, widget):
        """切换到新页面。"""
        # self.main_window.content = self.scroll_container
        self.inp_keyword.value = ''
        self.inp_content.value = ''
        self.inp_line.value = ''

def main():
    return fsaxis()
