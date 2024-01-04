import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class fsaxis(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        # Input fields
        inp_keyword = toga.TextInput(style=Pack(flex=1))
        inp_content = toga.TextInput(style=Pack(flex=2))
        
        # Multi-line input fields
        inp_line = toga.MultilineTextInput(style=Pack(flex=1, height=100))
        inp_cell = toga.MultilineTextInput(style=Pack(flex=1, height=200))
        
        # Buttons
        b1 = toga.Button('B1', style=Pack(width=100, padding_left=20))
        b2 = toga.Button('B2', style=Pack(width=100))
        b3 = toga.Button('B3', style=Pack(width=100))
        
        # Row containers
        row1 = toga.Box(style=Pack(direction=ROW, padding=5))
        row2 = toga.Box(style=Pack(direction=ROW, padding=5))
        row3 = toga.Box(style=Pack(direction=ROW, padding=5))
        column_buttons = toga.Box(style=Pack(direction=COLUMN, padding=5))  # Container for B2 and B3
        
        # Add input fields and buttons to the rows
        row1.add(inp_keyword)
        row1.add(inp_content)
        row2.add(inp_line)
        row2.add(b1)
        
        # Add buttons to the column container and the column container to the row
        column_buttons.add(b2)
        column_buttons.add(b3)
        row3.add(inp_cell)
        row3.add(column_buttons)  # Include the column container in the same row as inp_cell

        # Add the rows to the main box
        main_box.add(row1)
        main_box.add(row2)
        main_box.add(row3)

        # Main window configuration
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return fsaxis()
