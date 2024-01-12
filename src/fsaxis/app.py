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

        # 图片上传界面的输入框
        self.inp_content2 = toga.TextInput(style=Pack(padding=5, flex=1), placeholder='status')

        # 创建时区与运行状态
        self.time_zone = toga.TextInput(style=Pack(flex=1), placeholder='time_zone')
        self.running_status = toga.TextInput(style=Pack(flex=2), placeholder='status')

        # Creating multi-line input fields 创建多行输入字段
        self.inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=84), placeholder='inp_line')
        # self.inp_line.on_change = self.change_inp_line
        # 需要每个输入框都是焦点时使用on_change才能正常，否则会冲突
        self.inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=180), placeholder='inp_cell')
        self.inp_cell.enabled = False

        # Creating buttons 创建按钮
        button_style = {'width': 85, 'padding_top': 16}
        self.btn_line = toga.Button('✅line', style=Pack(**button_style), on_press=self.clk_btn_line)
        self.btn_cell = toga.Button('cell', style=Pack(**button_style), on_press=self.clk_btn_cell)
        button_style = {'width': 85, 'padding_top': 44}
        self.btn_clear = toga.Button('clear', style=Pack(**button_style), on_press=self.clk_btn_clear)

        # Add your new buttons here 新增按钮
        button_style2 = {'width': 85, 'padding_top': 0}
        self.btn_new1 = toga.Button(text = 'CL仅读', style=Pack(**button_style2), on_press=self.on_btn_new1_press)
        self.btn_new2 = toga.Button('历史', style=Pack(**button_style2), on_press=self.on_btn_new2_press)
        self.btn_new3 = toga.Button('传图', style=Pack(**button_style2), on_press=self.on_btn_new3_press)
        self.btn_new4 = toga.Button('✅line', style=Pack(**button_style2), on_press=self.clk_btn_line)

        # Organizing components into rows and columns 将组件组织成行和列
        col_1 = toga.Box(style=column_style, children=[self.btn_cell, self.btn_clear])
        row_1 = toga.Box(style=row_style, children=[self.time_zone, self.running_status])
        row_2 = toga.Box(style=row_style, children=[self.inp_cell, col_1])
        row_3 = toga.Box(style=row_style, children=[self.inp_line, self.btn_line])
        row_4 = toga.Box(style=row_style, children=[self.inp_keyword, self.inp_content])
        row_5 = toga.Box(style=row_style, children=[self.btn_new1, self.btn_new2, self.btn_new3, self.btn_new4])


        # New row for the new buttons 新按钮的行
        # row6 = toga.Box(style=row_style, children=[self.scroll_container])

        # Adding rows to the main layout box 将行添加到主布局框
        self.main_box.add(row_1)
        self.main_box.add(row_2)
        self.main_box.add(row_3)
        self.main_box.add(row_4)
        self.main_box.add(row_5)
        self.scroll_container.style = Pack(flex=1)

        self.main_box.add(self.scroll_container)
        #endregion

        # Setting up the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        self.inp_content.focus()

        self.original_content = self.main_window.content

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
        # 切换 inp_cell 的 enabled 状态
        self.inp_cell.enabled = not self.inp_cell.enabled

        # 更新按钮文本
        if self.inp_cell.enabled == False:
            self.btn_new1.text = "CL仅读"
        else:
            self.btn_new1.text = "CL可写"
    
    def on_btn_new2_press(self, widget):
        pass

    def on_btn_new3_press(self, widget):
        # 创建并显示图片选择和显示界面
        self.create_photo_view()

    def create_photo_view(self):
        from toga import ImageView, ScrollContainer

        # 创建“选择图片”按钮
        pick_button = toga.Button('选择图片', on_press=self.pick_image, style=Pack(padding=5, flex=1))
        back_button = toga.Button('Back', on_press=self.perform_action, style=Pack(padding=5, flex=1))

        # 创建“执行操作”按钮
        # action_button = toga.Button('Perform Action', on_press=self.perform_action2, style=Pack(padding=5, flex=1))
        action_button = toga.Button('上传图片', on_press=self.perform_action2, style=Pack(padding=5, flex=1))

        # 创建文本输入框
        # self.inp_content2 = toga.TextInput(style=Pack(padding=5, flex=1), placeholder='status')

        # 水平布局的容器，包括动作按钮和文本输入框
        row_1 = toga.Box(style=Pack(direction=ROW, padding=5), children=[action_button, self.inp_content2])
        row_2 = toga.Box(style=Pack(direction=ROW, padding=5), children=[pick_button, back_button])

        # 创建 ImageView，用于显示图片
        self.image_view = ImageView(style=Pack(width=400, height=300))

        # 创建 ScrollView，用于滚动查看 ImageView
        scroll_container = ScrollContainer(content=self.image_view, style=Pack(flex=1))

        # 创建垂直布局的容器，包括所有组件
        box = toga.Box(children=[row_2, scroll_container, row_1], style=Pack(direction=COLUMN, padding=10))

        # 更改当前窗口的内容为新布局
        self.main_window.content = box

        self.main_window.app.add_background_task(self.pick_image_direct)
    
    async def pick_image_direct(self, widget):
        # 直接调用 pick_image 方法
        await self.pick_image(widget)

    async def pick_image(self, widget):
        if sys.platform == 'win32':
            # Windows 环境下的逻辑
            image_folder = 'C:\\Users\\Ran\\Pictures\\Quicker截图'
            image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            latest_image = max(image_files, key=os.path.getmtime)
            
            with open(latest_image, 'rb') as f:
                image_data = f.read()
            # 加载图片
            self.image_view.image = toga.Image(data=image_data)
            
            # 获取图片的原始尺寸
            original_width, original_height = self.image_view.image.size
            
            # 设置 ImageView 的 style 属性，这里假设我们希望图片的最大宽度不超过窗口宽度
            max_width = self.main_window.size[0]
            scale_factor = min(max_width / original_width, 1)  # 确保不放大图片
            
            # 调整 ImageView 的大小以保持图片比例
            self.image_view.style.width = original_width * scale_factor
            self.image_view.style.height = original_height * scale_factor
            self.image_view.refresh()
        else:
            # Android 环境下的代码保持不变
            from android.content import Intent
            from java import jarray, jbyte

            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType("image/*")

            result = await self._impl.intent_result(intent)
            uri = result['resultData'].getData()

            content_resolver = self._impl.native.getContentResolver()
            stream = content_resolver.openInputStream(uri)

            def read_stream(input_stream):
                block = jarray(jbyte)(1024 * 1024)
                blocks = []
                while True:
                    bytes_read = input_stream.read(block)
                    if bytes_read == -1:
                        break
                    blocks.append(bytes(block)[:bytes_read])
                return b''.join(blocks)

            image_data = read_stream(stream)
            stream.close()

            self.image_view.image = toga.Image(data=image_data)
            
            # 获取图片的原始尺寸
            original_width, original_height = self.image_view.image.size
            
            # 设置 ImageView 的 style 属性，这里假设我们希望图片的最大宽度不超过窗口宽度
            max_width = self.main_window.size[0]
            scale_factor = min(max_width / original_width, 1)  # 确保不放大图片
            
            # 调整 ImageView 的大小以保持图片比例
            self.image_view.style.width = original_width * scale_factor
            self.image_view.style.height = original_height * scale_factor
            self.image_view.refresh()
        self.image_data = image_data

    def update_status(self, result):
        self.inp_content2.value = result
        # self.inp_content.value = f"{result} {self.inp_content.value}"

    def perform_action(self, widget):
        self.main_window.content = self.original_content
    
    def perform_action2(self, widget):
        self.main_window.content = self.original_content
        if self.image_view.image:
            from write_image import process_image_data
            import threading

            result = [None]

            def on_complete():
                # 更新UI
                self.main_window.app.add_background_task(lambda *args, **kwargs: self.update_status(result[0]))

            def thread_function():
                result[0] = process_image_data(self.image_data)
                on_complete()

            self.inp_content2.value = '图片写入中...'
            threading.Thread(target=thread_function).start()
        else:
            self.main_window.error_dialog("PhotoApp", "No image has been selected.")

    # 定义main_box回调函数
    def update_ui_with_result(self, response, full_cell):
        """更新界面元素的值。"""
        self.inp_cell.value = full_cell
        if response:
            self.running_status.value = str(response['msg']) + ": " + str(response['data']['updatedRange'])
        else:
            self.running_status.value = "write_data为空"
        
        self.btn_line.enabled = True
        self.btn_cell.enabled = True

        global my_global_variable
        if my_global_variable == self.inp_content.value:
            back_content2 = self.inp_line.value# 保持line的不变
            self.inp_content.value = ''
            self.inp_line.value = back_content2# 保持line的不变

            self.inp_content.focus()

    def worker2(self, inp_cell_value):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell = api_methods.write_cell_data(inp_cell_value)
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(response, full_cell))

    def worker(self, inp_line_value):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell = api_methods.write_line_data(inp_line_value)
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(response, full_cell))

    def change_content(self, widget):
        # 检查 inp_content2 是否存在并且有值
        if hasattr(self, 'inp_content2') and self.inp_content2.value:
            if self.inp_keyword.value:
                formatted_value = f'[{self.inp_keyword.value}[{self.inp_content2.value} {self.inp_content.value}]{self.inp_keyword.value}]'
            else:
                formatted_value = f'{self.inp_content2.value} {self.inp_content.value}'
        else:
            if self.inp_keyword.value:
                formatted_value = f'[{self.inp_keyword.value}[{self.inp_content.value}]{self.inp_keyword.value}]'
            else:
                formatted_value = self.inp_content.value

        self.inp_line.value = formatted_value
        """if "。。" in formatted_value:
            self.inp_line.focus()"""
        
    def change_inp_line(self, widget):
        if not self.inp_keyword.value:
            self.inp_content = self.inp_line.value


    def clk_btn_line(self, widget):
        global my_global_variable
        my_global_variable = self.inp_content.value
        self.btn_line.enabled = False
        self.btn_cell.enabled = False
        """处理按钮点击，启动后台线程。"""
        # formatted_value = f'[{self.inp_keyword.value}[{self.inp_content.value}]{self.inp_keyword.value}]'
        # self.inp_line.value = formatted_value
        formatted_value = self.inp_line.value
        self.running_status.value = "写入中..."
        # self.pick_image()
        threading.Thread(target=self.worker, args=(formatted_value,)).start()

    def clk_btn_cell(self, widget):
        self.btn_line.enabled = False
        self.btn_cell.enabled = False
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
            self.btn_line.enabled = True
            self.btn_cell.enabled = True

        # 创建确认对话框的内容
        confirm_label = toga.Label('确认写入？')
        confirm_button = toga.Button('确认', on_press=on_confirm)
        cancel_button = toga.Button('取消', on_press=on_cancel)
        confirm_box = toga.Box(children=[confirm_label, confirm_button, cancel_button])

        # 显示确认对话框
        self.main_window.content = confirm_box

    def set_controls_enabled(self, enabled):
        # 遍历主布局框中的所有子控件
        for child in self.main_box.children:
            # 检查子控件是否是 Box 类型（可能包含更多控件）
            if isinstance(child, toga.Box):
                for subchild in child.children:
                    # 禁用或启用所有 TextInput 和 Button，除了 self.btn_new3
                    if isinstance(subchild, (toga.TextInput, toga.Button)):
                        if subchild != self.btn_new3:
                            subchild.enabled = enabled
            # 直接禁用或启用 TextInput 和 Button
            elif isinstance(child, (toga.TextInput, toga.Button)):
                if child != self.btn_new3:
                    child.enabled = enabled

    def clk_btn_clear(self, widget):
        """切换到新页面。"""
        # self.main_window.content = self.scroll_container
        back_content = self.inp_line.value
        self.inp_content.focus()
        
        if self.inp_content.value == '': #如果inp_content为空 (意为二次点击)
            self.inp_keyword.value = ''
            self.inp_content.enabled = False
            self.inp_content.enabled = True
            # self.inp_content.focus()
        self.inp_content.value = ''
        self.inp_line.value = back_content #inp_line保持不变

        # 重新设置主界面
        # 禁用再启用输入框来尝试使其失去焦点
        '''self.inp_keyword.enabled = False
        self.inp_content.enabled = False
        self.inp_line.enabled = False
        self.inp_cell.enabled = False

        self.inp_keyword.enabled = True
        self.inp_content.enabled = True
        self.inp_line.enabled = True
        self.inp_cell.enabled = True'''

        # self.set_controls_enabled(False)


def main():
    return fsaxis()
