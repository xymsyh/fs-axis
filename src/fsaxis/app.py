import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class fsaxis(toga.App):
    def startup(self):
        # Refactored styling for reuse
        row_style = Pack(direction=ROW, padding=5)
        column_style = Pack(direction=COLUMN, padding=0)

        # Creating the main layout box
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=0))

        # Creating input fields with flex styling
        inp_keyword = toga.TextInput(style=Pack(flex=1))
        inp_content = toga.TextInput(style=Pack(flex=2))

        # 创建时区与运行状态
        time_zone = toga.TextInput(style=Pack(flex=1))
        running_status = toga.TextInput(style=Pack(flex=2))

        # Creating multi-line input fields
        inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=85))
        inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=155))

        # Creating buttons
        button_style = {'width': 85, 'padding_top': 20}
        btn_line = toga.Button('✅line', style=Pack(**button_style))
        btn_cell = toga.Button('✅cell', style=Pack(**button_style))
        btn_clear = toga.Button('清空', style=Pack(**button_style))

        # Organizing components into rows and columns
        row1 = toga.Box(style=row_style, children=[inp_keyword, inp_content])
        row2 = toga.Box(style=row_style, children=[inp_line, btn_line])
        col1 = toga.Box(style=column_style, children=[btn_cell, btn_clear])
        row3 = toga.Box(style=row_style, children=[inp_cell, col1])
        row4 = toga.Box(style=row_style, children=[time_zone, running_status])

        # Adding rows to the main layout box
        main_box.add(row1)
        main_box.add(row2)
        main_box.add(row3)
        main_box.add(row4)

        # Setting up the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return fsaxis()
