
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import time
import threading


"""import sys
sys.path.append("C:\\Users\\Ran\\Desktop\\飞书api第二版")"""
import sys
from pathlib import Path
def add_project_root_to_sys_path():
    # 获取当前文件的绝对路径  
    current_file_path = Path(__file__).resolve()

    # 获取当前文件的父目录的父目录（即项目根目录）
    project_root = current_file_path.parent

    # 将项目根目录添加到 sys.path
    sys.path.append(str(project_root))
add_project_root_to_sys_path()

from autom_tbl_inp import standardize_table_format

class ExampleBeeWareApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        
        # Set up T1 (single-line text input)
        self.input_t1 = toga.TextInput(placeholder='Enter text here')

        # Set up T2 (multi-line text input)
        self.input_t2 = toga.MultilineTextInput()

        # Set up T3 (multi-line text input)
        self.input_t3 = toga.MultilineTextInput()

        # Set up T4 (multi-line text input, but will act as a console)
        self.console_t4 = toga.MultilineTextInput(readonly=False)

        # Set up B1 button and its callback
        button_b1 = toga.Button('B1', on_press=self.enclose_text)

        # Set up B2 button and its callback
        button_b2 = toga.Button('B2', on_press=self.dummy_callback)

        # Set up B3 button and its callback
        button_b3 = toga.Button('B3', on_press=self.dummy_callback)

        # Arrange widgets
        box = toga.Box(
            children=[
                toga.Box(children=[self.input_t1, button_b1], style=Pack(direction=ROW)),
                self.input_t2,
                button_b2,
                self.input_t3,
                button_b3,
                self.console_t4,
            ],
            style=Pack(direction=COLUMN)
        )

        # Add the content on the main window
        self.main_window.content = box
        self.main_window.show()
        self.print_running_message()


    def enclose_text(self, widget):
        # Enclose T1's text in brackets and put it in T2
        self.input_t2.value = f'[{self.input_t1.value}[]{self.input_t1.value}]' #步骤一
        self.console_t4.value = f'({self.input_t1.value})\n' + self.console_t4.value #步骤二
        # standardize_table_format() #步骤三
        thread = threading.Thread(target=self.standardize_table_format_thread)
        thread.start()
        
        """# 定义一个不接受参数的包装函数
        def background_task_wrapper(*args, **kwargs):
            standardize_table_format()

        # 将包装函数作为后台任务添加
        self.add_background_task(background_task_wrapper) #步骤三：当仅注释这行代码即self.add_background_task(standardize_table_format())运行时，步骤一、二会正常先运行，然后再运行步骤三，standardize_table_format()运行时整个界面会阻塞
        # self.add_background_task(standardize_table_format()) #步骤三：当仅注释这行代码即self.add_background_task(background_task_wrapper)运行时，步骤一、二会在standardize_table_format()函数运行完成后再执行，standardize_table_format()运行时整个界面会阻塞

"""

    def standardize_table_format_thread(self):
        # 这里执行耗时的操作
        standardize_table_format()
        # 如果需要在操作完成后更新 GUI，确保使用线程安全的方法


    def dummy_callback(self, widget):
        # Placeholder for a callback function
        pass

    def print_running_message(self):
        # Print a running message in the console
        self.console_t4.value = '程序运行中\n' + self.console_t4.value


def main():
    return ExampleBeeWareApp('Example BeeWare App', 'org.beeware.widgets')

if __name__ == '__main__':
    main().main_loop()
