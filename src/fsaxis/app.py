# app.py

版本说明 = "inp_content为空不继续" 

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
import history_methods
import history_layout
import widget_methods
import json
import feishu_api
api = feishu_api.FeishuOpenAPI()

from datetime import datetime, timedelta
import queue

import os
print("工作目录 Current working directory:", os.getcwd())

import widget_text as wt

class fsaxis(toga.App):
    def startup(self):
        self.line读取 = '🚀读取'
        self.line写入 = '✅写入'
        self.line读取icon = '🚀'
        self.line写入icon = '✅'

        #region# keywords_box
        self.keywords_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 5, 0, 5)))
        
        #endregion
        self.scroll_container = toga.ScrollContainer(content=self.keywords_box,style=Pack(height=200))

        #region# main_box
        # Refactored styling for reuse 重构样式以供重用
        row_style = Pack(direction=ROW, padding=(0, 5, 0, 5))
        column_style = Pack(direction=COLUMN, padding=0)

        # Creating the main layout box 创建主布局框
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=0))

        # Creating input fields with flex styling 使用 Flex 样式创建输入字段
        self.inp_keyword = toga.TextInput(style=Pack(flex=1), placeholder='keyword')
        self.inp_keyword.on_change = lambda widget: widget_methods.on_change(self, widget)
        self.inp_keyword.on_lose_focus = lambda widget: widget_methods.on_lose_focus.inp_keyword(self, widget)

        self.inp_content = toga.TextInput(style=Pack(flex=2), placeholder='content', on_confirm=self.clk_btn_line)
        self.inp_content.on_change = lambda widget: widget_methods.on_change(self, widget)
        # self.inp_content.on_lose_focus = lambda widget: widget_methods.on_lose_focus.inp_content(self, widget)
        self.inp_content.on_gain_focus = lambda widget: widget_methods.on_lose_focus.inp_content(self, widget)
        self.inp_keyword.on_gain_focus = lambda widget: widget_methods.on_lose_focus.inp_content(self, widget)

        # 图片上传界面的输入框
        self.picture_status = toga.TextInput(style=Pack(padding=5, flex=1), placeholder='status')
        self.picture_status.on_change = lambda widget: widget_methods.on_change(self, widget)

        # 创建时区与运行状态
        self.time_zone = toga.TextInput(style=Pack(flex=1), placeholder='time_zone')
        self.time_zone.on_change = self.change_btnLine_status_byTZ
        self.running_status = toga.TextInput(style=Pack(flex=2), placeholder='status')

        # Creating multi-line input fields 创建多行输入字段
        self.inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=95), placeholder='inp_line')
        # self.inp_line.on_change = lambda widget: widget_methods.on_lose_focus.inp_line(self, widget)
        
        self.inp_line.on_change = self.change_btnLine_status
        # 需要每个输入框都是焦点时使用on_change才能正常，否则会冲突
        self.inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=150), placeholder='inp_cell')
        self.inp_cell.readonly = True

        # 标准按钮

        ## 靠顶风格
        button_style = {'width': 85, 'padding_top': 12} 
        self.btn_std1 = toga.Button('📜老滚', style=Pack(**button_style), on_press=self.clk_btn_cell)
        self.btn_std3 = toga.Button('🔀童锁', style=Pack(**button_style), on_press=self.toggle_child_lock)
        
        ## 第二风格
        button_style = {'width': 85, 'padding_top': 25} 
        self.btn_std2 = toga.Button('🖼️绘图', style=Pack(**button_style), on_press = self.on_btn_new3_press)
        
        # 新按钮
        button_style_用于开头 = {'width': 85, 'padding': (0, 0, 0, 5)}
        button_style_用于后跟 = {'width': 85, 'padding': (0, 0, 0, 0)}

        self.标准配置 = {
            'btn_new1': {
                'text': '👀仅读', 
                'style': button_style_用于开头, 
                'callback': self.on_btn_new1_press
            },

            'btn_new2': {
                'text': '🎨待定',  
                'style': button_style_用于后跟, 
                'callback': None
            },
            'btn_new3': {
                'text': '🗑️清关', 
                'style': button_style_用于后跟, 
                'callback': lambda widget: widget_methods.on_press.clear_keyword(self, widget)
            },

            'btn_new4': {
                'text': "🗑️清内",  # 使用 self.lineButton_state_read 直接作为文本值
                'style': button_style_用于后跟, 
                'callback': lambda widget: widget_methods.on_press.clear(self, widget)
            },
            'btn_new5': {
                'text': '🕰️往事', 
                'style': button_style_用于开头, 
                'callback': self.on_btn_new2_press
            },
            'btn_new6': {
                'text': '📜回滚', 
                'style': button_style_用于后跟, 
                'callback': self.clk_btn_cell
            },

            'btn_new7': {
                'text': '🖼️传图', 
                'style': button_style_用于后跟, 
                'callback': self.on_btn_new3_press
            },

            'btn_new8': {
                'text': "🤫写隐", 
                'style': button_style_用于后跟, 
                'callback': None
            },
        }

        self.童锁配置 = {
            'btn_new1': {
                'text': '🌙昨天', 
                'style': button_style_用于开头, 
                'callback': None, 
                'enabled': False
            },

            'btn_new2': {
                'text': '☀️今天',  
                'style': button_style_用于后跟, 
                'callback': None, 
                'enabled': False
            },
            'btn_new3': {
                'text': '💫明天', 
                'style': button_style_用于后跟, 
                'callback': None, 
                'enabled': False
            },

            'btn_new4': {
                'text': "🌌深空",  
                'style': button_style_用于后跟, 
                'callback': lambda widget: widget_methods.on_press.clear(self, widget)
            },
            'btn_new5': {
                'text': '🌙昨天', 
                'style': button_style_用于开头, 
                'callback': None, 
                'enabled': False
            },
            'btn_new6': {
                'text': '☀️今天', 
                'style': button_style_用于后跟, 
                'callback': None, 
                'enabled': False
            },

            'btn_new7': {
                'text': '💫明天', 
                'style': button_style_用于后跟, 
                'callback': None, 
                'enabled': False
            },

            'btn_new8': {
                'text': self.line读取, 
                'style': button_style_用于后跟, 
                'callback': self.clk_btn_line
            },
        }


        # 创建按钮
        for key, config in self.童锁配置.items():
            setattr(
                self, 
                key, 
                toga.Button(
                    config['text'], 
                    style=Pack(**config['style']), 
                    on_press=config['callback'], 
                    # 同样使用 get 方法设置按钮的初始启用状态，如果 'enabled' 字段不存在，则默认为 True
                    enabled=config.get('enabled', True)
                )
            )

        # Organizing components into rows and columns 将组件组织成行和列
        col_1 = toga.Box(style=column_style, children=[self.btn_std1, self.btn_std2]) 
        row_1 = toga.Box(style=row_style, children=[self.time_zone, self.running_status])
        row_2 = toga.Box(style=row_style, children=[self.inp_cell, col_1])
        row_3 = toga.Box(style=row_style, children=[self.inp_line, self.btn_std3]) 
        row_4 = toga.Box(style=row_style, children=[self.inp_keyword, self.inp_content])
        row_5 = toga.Box(style=row_style, children=[self.btn_new1, self.btn_new2, self.btn_new3, self.btn_new4])
        row_6 = toga.Box(style=row_style, children=[self.btn_new5, self.btn_new6, self.btn_new7, self.btn_new8])


        # New row for the new buttons 新按钮的行
        # row6 = toga.Box(style=row_style, children=[self.scroll_container])

        # Adding rows to the main layout box 将行添加到主布局框
        self.main_box.add(row_1)
        self.main_box.add(row_2)
        self.main_box.add(row_3)
        self.main_box.add(row_4)
        self.main_box.add(row_5)
        self.main_box.add(row_6)
        self.scroll_container.style = Pack(flex=1)

        self.main_box.add(self.scroll_container)
        #endregion

        # Setting up the main window
        self.main_window = toga.MainWindow(title=self.formal_name, size=(550, 750))
        self.main_window.content = self.main_box
        self.main_window.show()
        self.inp_content.focus()

        self.original_content = self.main_window.content

        self.my_global_variable = None
        self.history_layout_box = None
        self.used_data_json = None
        self.clock_icons = {
            0: '🕛', 0.5: '🕧', 1: '🕐', 1.5: '🕜',
            2: '🕑', 2.5: '🕝', 3: '🕒', 3.5: '🕞',
            4: '🕓', 4.5: '🕟', 5: '🕔', 5.5: '🕠',
            6: '🕕', 6.5: '🕡', 7: '🕖', 7.5: '🕢',
            8: '🕗', 8.5: '🕣', 9: '🕘', 9.5: '🕤',
            10: '🕙', 10.5: '🕥', 11: '🕚', 11.5: '🕦',
        }

        threading.Thread(target=self.compare_keyword_data).start()

        # self.image_upload_completed = threading.Event()
        self.upload_result_queue = queue.Queue()

    # 定义相关回调函数
    def toggle_child_lock(self, widget):
        # 定义一个属性来跟踪童锁是否被激活
        if hasattr(self, 'child_lock_active'):
            self.child_lock_active = not self.child_lock_active
        else:
            self.child_lock_active = False

        # 选择正确的配置字典
        config_to_use = self.童锁配置 if self.child_lock_active else self.标准配置

        # 根据童锁状态切换按钮的启用状态和文本
        for btn_name, btn_config in config_to_use.items():
            btn = getattr(self, btn_name, None)
            if btn:
                btn.text = btn_config['text']  # 更新按钮文本
                btn.on_press = btn_config['callback']  # 更新按钮回调函数
                # btn.style = btn_config['style']  # 更新按钮样式，如果需要
                # 使用 get 方法获取 'enabled' 字段的值，如果不存在则默认为 True
                btn.enabled = btn_config.get('enabled', True)

        # 根据童锁的激活状态更新童锁按钮的文本
        if self.child_lock_active:
            # self.btn_std3.text = '⭐恒星'
            self.btn_std3.text = '🔀童锁'
        else:
            self.btn_std3.text = '🌠流星'

    # @staticmethod
    def get_clock_icon(self, hour, minute):
        # 根据小时和分钟确定图标
        
        # 计算对应的键值
        key = hour % 12 + (0.5 if minute >= 30 else 0)
        # 返回对应的图标
        return self.clock_icons.get(key, '❓')

    @staticmethod
    def format_text(hour):
        # 格式化文本为"01点"、"02点"……"23点"
        # return f'{hour:02d}点'
        return f'{hour:02d}'

    def update_lineButton_state(self, enabled, text=None):
        # 这里用于更改on_change时, 发送按钮的更新逻辑
        # for btn in [self.btn_std1, self.btn_new4, self.btn_new8]:
        for btn in [self.btn_new8]:
            btn.enabled = enabled
            if text:
                btn.text = text

    def change_btnLine_status_byTZ(self, widget):

        if self.time_zone.value == "":
            self.update_lineButton_state(True)
            self.change_btnLine_status(widget)
        elif self.time_zone.value == "-":
            self.update_lineButton_state(False)
        else:
            try:
                time_zone_offset = int(self.time_zone.value)
                current_utc_time = datetime.now()
                adjusted_time = current_utc_time + timedelta(hours=time_zone_offset)
                icon = self.get_clock_icon(adjusted_time.hour, adjusted_time.minute)
                text = self.format_text(adjusted_time.hour)
                if self.inp_line.value:
                    self.update_lineButton_state(True, f'{self.line写入icon}{icon}{text}')
                else:
                    self.update_lineButton_state(True, f'{self.line读取icon}{icon}{text}')
            except ValueError:
                self.update_lineButton_state(False, '❓❓')

    def compare_keyword_data(self):
        # 从 API 获取数据
        api = feishu_api.FeishuOpenAPI()
        self.sheet_data_json = api.get_sheet_data('70fPAj!B1:B2')['data']['valueRange']['values'][0][0]  # 假设 api_methods 是您用来调用 API 的模块

        self.sheet_data_json = json.loads(self.sheet_data_json)
        toga.App.app.add_background_task(self.create_buttons_layout)

    # 定义keywords_box回调函数
    

    def create_buttons_layout(self, *args, **kwargs):
        if self.used_data_json == self.sheet_data_json:
            return

        # 首先清除 keywords_box 中的所有现有子元素
        for child in list(self.keywords_box.children):
            self.keywords_box.remove(child)

        # 接着使用最新的数据重新创建按钮
        self.used_data_json = self.sheet_data_json
        for category_name, category_items in self.used_data_json.items():
            # 创建并添加一个类别标签
            category_label = toga.Label(category_name, style=Pack(padding_bottom=0))
            self.keywords_box.add(category_label)

            # 创建该类别下的所有按钮
            row_box = None
            for i, item in enumerate(category_items):
                button_name = item["keyword"]
                if i % 4 == 0 or row_box is None:
                    row_box = toga.Box(style=Pack(direction=ROW, padding=(0, 5, 0, 5)))
                    self.keywords_box.add(row_box)

                if button_name:  # 确保按钮名称非空
                    button = toga.Button(button_name, style=Pack(width=85), on_press=self.on_button_press)
                    row_box.add(button)

    def on_button_press(self, widget):
        # 更新 inp_keyword 的值为按钮的文本
        self.inp_keyword.value = widget.text
        # self.main_window.content = self.main_box


    def rewrite_keywords_json(self, widget):
        threading.Thread(target=self.compare_keyword_data).start()

    def on_btn_new1_press(self, widget):
        # 切换 inp_cell 输入框的只读状态
        self.inp_cell.readonly = not self.inp_cell.readonly

        # 更新按钮文本以反映当前状态
        if self.inp_cell.readonly:
            self.btn_new1.text = '👀仅读'
        else:
            self.btn_new1.text = '✍️可写'
    
    

    def on_btn_new2_press(self, widget = None, assistive_calling = False):

        print('on_btn_new2_press 被调用')

        if assistive_calling == True or self.history_layout_box is None:
            log_data = history_methods.read("line")
            log_data = history_methods.time_formatting(log_data)
            log_data = log_data[-20:][::-1]
            self.history_layout_box = history_layout.build(None, log_data, fsaxis_instance = self)
            print('on_btn_new2_press 被调用222')

        if assistive_calling == False:

            # self.original_content = self.main_window.content
            self.main_window.content = self.history_layout_box
            
            print('on_btn_new2_press 被调用333')

        

    def on_btn_new3_press(self, widget):
        # 创建并显示图片选择和显示界面
        self.create_photo_view()

    def create_photo_view(self):
        # 01151718 开始重构create_photo_view函数
        from toga import ImageView, ScrollContainer

        # 创建上传、选择、返回按钮
        action_button = toga.Button('上传所选图片', on_press=self.perform_action2, style=Pack(padding=0, flex=3))
        # pick_button = toga.Button('重选', on_press=self.pick_image, style=Pack(padding=0, flex=1))
        back_button = toga.Button('取消', on_press=self.perform_action, style=Pack(padding=0, flex=1))

        action_button2 = toga.Button('上传所选图片', on_press=self.perform_action2, style=Pack(padding=0, flex=3))
        # pick_button2 = toga.Button('重选', on_press=self.pick_image, style=Pack(padding=0, flex=1))
        back_button2 = toga.Button('取消', on_press=self.perform_action, style=Pack(padding=0, flex=1))

        # 水平布局的容器，包括动作按钮和文本输入框
        row_1 = toga.Box(style=Pack(direction=ROW, padding=5), children=[action_button, back_button])
        row_2 = toga.Box(style=Pack(direction=ROW, padding=5), children=[action_button2, back_button2])

        # 创建 ImageView，用于显示图片
        self.image_view = ImageView(style=Pack(width=400, height=300))

        # 创建 ScrollView，用于滚动查看 ImageView
        scroll_container = ScrollContainer(content=self.image_view, style=Pack(flex=1))

        # 创建垂直布局的容器，包括所有组件
        self.photo_view_box = toga.Box(children=[row_1, scroll_container, row_2], style=Pack(direction=COLUMN, padding=10))

        # 更改当前窗口的内容为新布局
        

        self.main_window.app.add_background_task(self.pick_image_direct)

        
    
    async def pick_image_direct(self, widget):
        # 直接调用 pick_image 方法
        await self.pick_image(widget)
        self.main_window.content = self.photo_view_box

        # 注释以下段可取消安卓选中后自动执行 (取消自动执行后，需要手动点击上传按钮)
        if sys.platform != 'win32': # != 'win32' 即安卓
            self.perform_action2(widget) 
            self.inp_content.focus()
            # self.scroll_container.clear()
            self.scroll_container.content = self.image_view

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
            from android.content import Intent # type: ignore
            from java import jarray, jbyte # type: ignore

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
        self.picture_status.value = result
        """# 图片上传逻辑...
        self.image_upload_completed.clear()  # 确保事件处于未设置状态
        # 进行图片上传...
        self.image_upload_completed.set()  # 图片上传完成后设置事件"""
        self.upload_result_queue.put(result)
        # self.inp_content.value = f"{result} {self.inp_content.value}"

    def perform_action(self, widget):
        self.main_window.content = self.original_content
    
    def perform_action2(self, widget):
        self.main_window.content = self.original_content
        if self.image_view.image:
            from write_image import process_image_data
            import threading

            result = [None]  # 使用列表存储结果，以便在线程中修改

            def on_complete():
                # 使用 result[0] 获取结果，并更新UI
                self.main_window.app.add_background_task(lambda *args, **kwargs: self.update_status(result[0]))

            def thread_function():
                # 清空队列以确保获取的是最新结果
                while not self.upload_result_queue.empty():
                    try:
                        self.upload_result_queue.get_nowait()
                    except queue.Empty:
                        break
                # 将处理结果存储在 result[0] 中
                result[0] = process_image_data(self.image_data)
                on_complete()

            self.picture_status.value = wt.图片写入中
            threading.Thread(target=thread_function).start()
        else:
            self.main_window.error_dialog("PhotoApp", "No image has been selected.")


    # 定义main_box回调函数
    def update_ui_with_result(self, response, full_cell, no_write_history = False, old_cell_data=None):
        """更新界面元素的值。"""
        self.inp_cell.value = full_cell

        if no_write_history == False:
            history_methods.write("cell", old_cell_data)
            history_methods.write("cell", full_cell)

        if response:
            self.running_status.value = str(response['msg']) + ": " + str(response['data']['updatedRange'])
            # 检查self.btn_line.text是否包含任意一个时钟图标
            if any(icon in self.btn_std1.text for icon in self.clock_icons.values()):
                # 如果包含，执行某些操作
                # if '-' in self.time_zone.value 
                    self.time_zone.value = ''
        else:
            self.running_status.value = "write_data为空"
        
        self.btn_std1.enabled = True
        self.btn_std2.enabled = True

        # --- 用于保持 inp_line 不变的方法 --- ↓
        # 注：下述7行方法于 01131540 进行了重构，未进行测试而直接发布了，后续出现相关问题可关注此
        # global my_global_variable
        if self.my_global_variable == self.inp_content.value: #判断用户在写入期间是否操作inp_content值
            back_content2 = self.inp_line.value #记录inp_line值
            self.inp_content.value = '' #由于on_change函数的存在，会导致inp_line值变化
            self.inp_line.value = back_content2 #还原inp_line值
        
        self.picture_status.value = ""
        # self.inp_content.focus() # 该会导致在电脑上窗口激活，而我不希望激活

        # if sys.platform == 'win32':
        if 1 == 1:
            threading.Thread(target=self.worker3, args=()).start()
            pass
            
        threading.Thread(target=self.worker4, args=(full_cell,)).start()

        # threading.Thread(target=self.on_btn_new2_press, args=(True,)).start()

        # threading.Thread(target=self.on_btn_new2_press, kwargs={'assistive_calling': True}).start()

        self.on_btn_new2_press(assistive_calling=True)

        self.scroll_container.content = self.keywords_box

    def worker4(self, message):
        print("message 01172159 01172159 01172159")
        print(message)
        response = api_methods.send_imessage(str(message))

        # self.on_btn_new2_press(assistive_calling=True)
    def worker3(self):
        response = api_methods.standardize_table_format()

    def worker2(self, inp_cell_value, no_write_history = False):
        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell, old_cell_data = api_methods.write_cell_data(inp_cell_value)

        if no_write_history == True:
            toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(
                response, full_cell, no_write_history == True, old_cell_data = old_cell_data))

        else:
            toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(
                response, full_cell, old_cell_data = old_cell_data))

    def worker(self, inp_line_value, time_zone):
        """# 等待图片上传完成
        self.image_upload_completed.wait()"""

        if wt.图片写入中 in inp_line_value:
            result = self.upload_result_queue.get()
            inp_line_value = inp_line_value.replace(wt.图片写入中, result)

        """在后台线程中执行耗时操作，并在完成后更新UI。"""
        response, full_cell, old_cell_data = api_methods.write_line_data(inp_line_value, time_zone=time_zone)  
        toga.App.app.add_background_task(lambda interface: self.update_ui_with_result(
            response, full_cell, old_cell_data = old_cell_data))

        
    def change_btnLine_status(self, widget):
        '''if not self.inp_keyword.value:
            self.inp_content = self.inp_line.value''' # 于02010935注释
        
        if self.time_zone.value == "":
            if self.inp_line.value == "":
                self.update_lineButton_state(True, self.line读取)
            if self.inp_line.value != "":
                self.update_lineButton_state(True, self.line写入)
        else:
            self.change_btnLine_status_byTZ(widget)


    def clk_btn_line(self, widget): #line回调

        # 首先检查inp_content.value是否为空, 若为空则更新状态栏并返回
        if self.inp_content.value == "" and self.inp_keyword.value != "": 
            self.running_status.value = "inp_content为空 无法继续"
            return  # 停止执行后续代码

        # widget_methods.on_lose_focus.inp_keyword(self, widget) #使用失去焦点方法。用于更新关键词框中的内容
        if self.inp_content.value == "" and self.inp_keyword.value != "" and self.inp_line.value == "":
            widget_methods.on_change(self, widget)
            
        # 01152032：优化clk_btn_line函数
        # global my_global_variable
        self.my_global_variable = self.inp_content.value # 用于后续判断用户是否更改inp_content值

        self.btn_std1.enabled = False
        self.btn_std2.enabled = False
        
        self.running_status.value = "执行中..."
        history_methods.write("line", self.inp_line.value)

        def parse_time_zone_string(time_zone_str):
            # 如果字符串为空，返回默认值0
            if not time_zone_str:
                return 0

            # 验证字符串是否只包含数字、加号和减号
            if all(c in '0123456789+-' for c in time_zone_str):
                try:
                    # 计算表达式的值
                    time_zone_value = eval(time_zone_str)
                    return time_zone_value
                except Exception as e:
                    # 如果表达式无效或计算过程中发生错误
                    print(f"无法解析时区字符串: {time_zone_str}. 错误: {e}")
                    return None
            else:
                print(f"时区字符串包含无效字符: {time_zone_str}")
                return None
        time_zone = parse_time_zone_string(self.time_zone.value) #待修改完毕
        # time_zone = int(self.time_zone.value)

        # 添加上次提交的内容保存到变量，以确保不会不必要的获取焦点以更新内容
        self.last_inp_line_value = self.inp_line.value

        threading.Thread(target=self.worker, args=(self.inp_line.value, time_zone,)).start()

    def clk_btn_cell(self, widget):
        """self.btn_std1.enabled = False
        self.btn_std2.enabled = False"""
        self.btn_new8.enabled = False #这部分内容的目的是为了确保不会重复触发回调函数, 以免出现错误

        self.inp_cell.readonly = True
        cell_history_data = history_methods.read("cell")

        # 创建确认操作的处理函数
        def on_confirm(widget):
            self.running_status.value = "回退中..."
            
            # [-2] 为上次提交内容
            # .split(": ", 1)[1] 为剔除前面的时间
            rollback_content = cell_history_data[-2].split(": ", 1)[1]
            history_methods.delete_last_lines("cell", 1)

            no_write_history = True

            threading.Thread(target=self.worker2, args=(rollback_content, no_write_history, )).start()
            self.main_window.content = self.main_box
            

        # 创建取消操作的处理函数
        def on_cancel(widget):
            # self.running_status.value = "操作已取消"
            self.main_window.content = self.main_box
            """self.btn_std1.enabled = True
            self.btn_std2.enabled = True"""
            self.btn_new8.enabled = True

        # 创建确认对话框的内容
        confirm_label = toga.Label('确认回退至以下版本？')
        confirm_button = toga.Button('确认', on_press=on_confirm)
        cancel_button = toga.Button('取消', on_press=on_cancel)
        confirm_box = toga.Box(children=[confirm_label, confirm_button, cancel_button])

        # 创建cell历史记录显示框
        cell_history_show = toga.MultilineTextInput(style=Pack(flex=1))
        cell_history_show2 = toga.MultilineTextInput(style=Pack(flex=1))

        # 定义原始文本 ---------------------------------------------------
        latest_1 = cell_history_data[-1]
        latest_2 = cell_history_data[-2]

        # 提取时间戳
        latest_1_time = latest_1[:19]  # 时间戳的格式为 "YYYY-MM-DD HH:MM:SS"
        latest_2_time = latest_2[:19]

        # 计算开始和结束切片的位置
        start_slice = len("2024-01-18 18:02:XX: [['")
        end_slice = len("']]")

        # 处理两个文本
        processed_text1 = latest_1[start_slice:-end_slice]
        processed_text2 = latest_2[start_slice:-end_slice]

        # 寻找不同部分
        difference = processed_text1.replace(processed_text2, '').strip()

        # 打印时间戳和差异部分
        # latest_1_time, latest_2_time, difference, latest_2
        # 定义原始文本 ---------------------------------------------------

        def time_ago(time_str):
            from datetime import datetime
            current_time = datetime.now()
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            diff = current_time - time
            seconds = diff.total_seconds()

            if seconds < 60:
                return f"{int(seconds)}秒前"
            elif seconds < 3600:
                return f"{int(seconds // 60)}分钟前"
            elif seconds < 86400:
                return f"{int(seconds // 3600)}小时前"
            else:
                return f"{int(seconds // 86400)}天前"

        latest_1_time = time_ago(latest_1_time)
        latest_2_time = time_ago(latest_2_time)

        cell_history_show.value = "【即将移除 (" + latest_1_time + ")：】\n" + difference.replace('\\n', '\n')
        cell_history_show2.value = "【结果预览 (" + latest_2_time + ")：】\n" + processed_text2.replace('\\n', '\n')

        # 新box
        confirm_box_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        confirm_box_box.add(confirm_box)
        confirm_box_box.add(cell_history_show)
        confirm_box_box.add(cell_history_show2)

        # 显示确认对话框
        self.main_window.content = confirm_box_box

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




def main():
    return fsaxis(f"飞书轴线_{版本说明}")
