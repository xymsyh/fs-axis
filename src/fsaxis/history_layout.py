# 此版本完全等价于在LocNow中测试的app.py代码，并且可以单独运行，这很棒！
import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW
import re

def keyword_extraction(text):
    try:
        # 第一步：非贪婪匹配首个[]中的内容 
        # 使用正则表达式匹配第一个括号内的内容。这里的.*?表示非贪婪匹配，即尽可能少的匹配字符。
        pattern_step1 = r"\[.*?\]"
        result_step1 = re.search(pattern_step1, text).group()

        # 第二步：贪婪匹配result_step1中的最后一个[之前的所有内容 
        # 在第一步的结果中，寻找最后一个出现的"["及其后的所有字符。这里的.*表示贪婪匹配，尽可能多的匹配字符。
        pattern_step2 = r"\[.*\["
        result_step2 = re.search(pattern_step2, result_step1).group()

        # 第三步：删除result_step2前后的[ 
        # 从第二步的结果中去除两端的"["，以得到最终结果。
        result_final = result_step2.strip('[')

        return result_final
    except AttributeError:
        # 如果匹配失败，返回空字符串
        return ""

def build(app, log_data=None, fsaxis_instance=None):
    # 创建一个垂直排列的盒子来放置所有控件
    main_box = toga.Box(style=Pack(direction=COLUMN))

    #状态输入栏：配合on_change回调函数实现功能的调用
    inp_status = toga.TextInput(style=Pack(flex=1), placeholder='inp_status')

    # 添加顶部按钮
    top_buttons_box = toga.Box(style=Pack(direction=ROW, padding=5))
    for i in range(4):
        button = toga.Button(f'顶部按钮 {i+1}', on_press=lambda widget: print(f"顶部按钮 {i+1} 被点击"))
        top_buttons_box.add(button)
    main_box.add(top_buttons_box)

    # 日志数据
    if log_data == None:
        log_data = [
            '2024-01-15 22:02:00: 测试\n',
            '2024-01-15 22:03:19: 测试\n',
            '2024-01-15 22:03:24: 测试\n',
            '2024-01-15 22:07:30: 测试\n',
        ]

    # 创建一个滚动容器
    scroll_box = toga.ScrollContainer(content=main_box, style=Pack(flex=1))

    # 为每条日志创建一个输入框和按钮
    for log in log_data:
        row_box = toga.Box(style=Pack(direction=ROW, padding=5))
        text_input = toga.TextInput(style=Pack(flex=1), readonly=False, value=log.strip())

        def on_button_press(widget, text_input=text_input, fsaxis_instance=fsaxis_instance):
            if fsaxis_instance and hasattr(fsaxis_instance, 'inp_keyword'):
                keyword_content = keyword_extraction(text_input.value)
                fsaxis_instance.inp_keyword.value = keyword_content

                fsaxis_instance.inp_line.value = text_input.value.split(": ", 1)[1]

                fsaxis_instance.perform_action(None)
            print("按钮被点击，输入框内容已赋值")
            print(fsaxis_instance.inp_keyword.value)

        button = toga.Button('按钮', on_press=on_button_press)
        row_box.add(text_input)
        row_box.add(button)
        main_box.add(row_box)


    # 添加底部按钮
    bottom_buttons_box = toga.Box(style=Pack(direction=ROW, padding=5))
    for i in range(4):
        button = toga.Button(f'底部按钮 {i+1}', on_press=lambda widget: print(f"底部按钮 {i+1} 被点击"))
        bottom_buttons_box.add(button)
    main_box.add(bottom_buttons_box)

    return scroll_box

def main():
    # 创建 Toga 应用
    return toga.App('日志应用', 'org.beeware.helloworld', startup=build)

if __name__ == '__main__':
    main().main_loop()
