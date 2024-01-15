import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW

def build(app):
    # 创建一个垂直排列的盒子来放置所有控件
    main_box = toga.Box(style=Pack(direction=COLUMN))

    # 添加顶部按钮
    top_buttons_box = toga.Box(style=Pack(direction=ROW, padding=5))
    for i in range(4):
        button = toga.Button(f'顶部按钮 {i+1}', on_press=lambda widget: print(f"顶部按钮 {i+1} 被点击"))
        top_buttons_box.add(button)
    main_box.add(top_buttons_box)

    # 日志数据
    log_data = [
        '2024-01-15 22:02:00: 测试\n',
        '2024-01-15 22:03:19: 测试\n',
        '2024-01-15 22:03:24: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:30: 测试\n',
        '2024-01-15 22:07:33: 测试\n',
        '2024-01-15 22:07:36: 测试\n',
        '2024-01-15 22:07:39: 测试\n',
        '2024-01-15 22:07:40: 测试'
    ]

    # 创建一个滚动容器
    scroll_box = toga.ScrollContainer(content=main_box, style=Pack(flex=1))

    # 为每条日志创建一个输入框和按钮
    for log in log_data:
        row_box = toga.Box(style=Pack(direction=ROW, padding=5))
        text_input = toga.TextInput(style=Pack(flex=1), readonly=False, value=log.strip())
        button = toga.Button('按钮', on_press=lambda widget: print("按钮被点击"))
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
