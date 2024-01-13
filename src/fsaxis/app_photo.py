# 本可后删 (01121742)，目前仅用于参考

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

import os
import sys
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga import ImageView, ScrollContainer

class PhotoApp(toga.App):
    def __init__(self, formal_name, app_id, **kwargs):
            super().__init__(formal_name, app_id, **kwargs)
            self.image_data = None  # 添加这行来初始化 image_data 属性


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

        

    # 执行操作的方法
    def update_status(self, result):
        self.inp_content.value = result

    def perform_action(self, widget):
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

            self.inp_content.value = '写入中...'
            threading.Thread(target=thread_function).start()
        else:
            self.main_window.error_dialog("PhotoApp", "No image has been selected.")

    # 启动应用程序时执行的方法
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.size = (400, 600)

        pick_button = toga.Button('Pick Image', on_press=self.pick_image, style=Pack(padding=5))
        action_button = toga.Button('Perform Action', on_press=self.perform_action, style=Pack(padding=5, flex=1))
        self.inp_content = toga.TextInput(style=Pack(flex=2), placeholder='content')
        row_1 = toga.Box(style=Pack(direction=ROW, padding=5), children=[action_button, self.inp_content])



        self.image_view = ImageView(style=Pack(width=400, height=300))

        scroll_container = ScrollContainer(content=self.image_view, style=Pack(flex=1))

        box = toga.Box(children=[pick_button, scroll_container, row_1],
                       style=Pack(direction=COLUMN, padding=10))

        self.main_window.content = box
        self.main_window.show()

def main():
    return PhotoApp('PhotoApp', 'org.beeware.photoapp')

if __name__ == '__main__':
    app = main()
    app.main_loop()
