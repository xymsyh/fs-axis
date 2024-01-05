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

class fsaxis(toga.App):
    def startup(self):
        # 创建一个新页面
        self.new_page = toga.Box(style=Pack(direction=COLUMN, padding=5))
        new_label = toga.Label('这是一个新的页面')
        self.new_page.add(new_label)

        # Refactored styling for reuse
        row_style = Pack(direction=ROW, padding=5)
        column_style = Pack(direction=COLUMN, padding=0)

        # Creating the main layout box
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=0))

        # Creating input fields with flex styling
        self.inp_keyword = toga.TextInput(style=Pack(flex=1))
        self.inp_content = toga.TextInput(style=Pack(flex=2))

        # 创建时区与运行状态
        self.time_zone = toga.TextInput(style=Pack(flex=1), placeholder='time zone')
        self.running_status = toga.TextInput(style=Pack(flex=2))

        # Creating multi-line input fields
        self.inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=85))
        self.inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=155))

        # Creating buttons
        button_style = {'width': 85, 'padding_top': 20}
        self.btn_line = toga.Button('✅line', style=Pack(**button_style), on_press=self.clk_btn_line)
        self.btn_cell = toga.Button('✅cell', style=Pack(**button_style), on_press=self.clk_btn_cell)
        self.btn_clear = toga.Button('清空', style=Pack(**button_style), on_press=self.clk_btn_clear)

        # region Organizing components into rows and columns
        row1 = toga.Box(style=row_style, children=[self.inp_keyword, self.inp_content])
        row2 = toga.Box(style=row_style, children=[self.inp_line, self.btn_line])
        col1 = toga.Box(style=column_style, children=[self.btn_cell, self.btn_clear])
        row3 = toga.Box(style=row_style, children=[self.inp_cell, col1])
        row4 = toga.Box(style=row_style, children=[self.time_zone, self.running_status])
        # endregion

        # Adding rows to the main layout box
        main_box.add(row1)
        main_box.add(row2)
        main_box.add(row3)
        main_box.add(row4)

        # Setting up the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # 定义回调函数
    def update_ui_with_result(self, result):
        """更新界面元素的值。"""
        self.inp_cell.value = result

    def worker(self, inp_line_value):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        result = api_methods.write_line_data(inp_line_value)
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(result))

    def clk_btn_line(self, widget):
        """处理按钮点击，启动后台线程。"""
        formatted_value = f'[{self.inp_keyword.value}[{self.inp_content.value}]{self.inp_keyword.value}]'
        self.inp_line.value = formatted_value
        threading.Thread(target=self.worker, args=(formatted_value,)).start()

    def clk_btn_cell(self, widget):
        """处理第二个按钮的点击（如果有实际功能，需要实现）。"""
        pass

    def clk_btn_clear(self, widget):
        """切换到新页面。"""
        self.main_window.content = self.new_page

def main():
    return fsaxis()
