# 本 api_methods.py 在 01152131 实际上可以理解为 app_methods.py

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

from autom_tbl_inp import output_current_data
from autom_tbl_inp import standardize_table_format
from feishu_api import FeishuOpenAPI
from datetime import datetime


def send_imessage(message, user_id=None):
    if not user_id:
        user_id = "Yao"
    
    api = FeishuOpenAPI()
    api.send_message(user_id, message)

def write_cell_data(cell_data):  
    if not cell_data:
        timestamp = datetime.now().strftime("%m%d%H%M")
        cell_data = "清空" + f" [{timestamp}]"

    raw_cell_data_full = output_current_data()
    rcd_value = raw_cell_data_full['data']['valueRange']['values'][0][0]
    old_cell_data = [[str(rcd_value)]]
    data_range = raw_cell_data_full['data']['valueRange']['range']
    
    api = FeishuOpenAPI()
    def clean_cell_data(cell_data_str):
        # 检查并处理 "[[" 或 "[[\"" 开头
        if cell_data_str.startswith('[["') or cell_data_str.startswith('[[\''):
            cell_data_str = cell_data_str[3:]
        elif cell_data_str.startswith('[['):
            cell_data_str = cell_data_str[2:]

        # 检查并处理 "]]" 或 "]]" 结尾
        if cell_data_str.endswith('"]]') or cell_data_str.endswith('\']]'):
            cell_data_str = cell_data_str[:-3]
        elif cell_data_str.endswith(']]'):
            cell_data_str = cell_data_str[:-2]

        return cell_data_str
    cell_data = clean_cell_data(cell_data)
    cell_data = cell_data.replace("\\n", "\n")
    cell_data = [[cell_data]]
    response = api.write_sheet_data(data_range, cell_data)
    return response, cell_data, old_cell_data

def write_line_data(line_data, keep_5_clock=False):  
    # 01151408 重构 write_line_data 函数代码：删除不必要的代码；删除原来的空值直接返回 (现在的逻辑为空值重新读取cell内容)
    
    # 获取单元格 value 和 range
    raw_cell_data_full = output_current_data(keep_5_clock=keep_5_clock)
    rcd_value = raw_cell_data_full['data']['valueRange']['values'][0][0]
    old_cell_data = [[str(rcd_value)]]
    rcd_range = raw_cell_data_full['data']['valueRange']['range']

    print(f"当前line_data数据：{line_data}")

    if line_data:
        line_data = insert_current_time(line_data) #判断入睡起床
        timestamp = datetime.now().strftime("%m%d%H%M")
        new_cell_data = [[line_data + f" [{timestamp}]" + "\n" + str(rcd_value)]]
    else:
        new_cell_data = [[str(rcd_value)]]

    def handling_two_dimensional_list_data(data):
        # 该函数实际上可以处理形如 [[]] 这样的列表的列表的每一个单元格
        # 允许的单元格范围为：1 ~ 正无穷
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                # 迭代替换 '\n\n' 为 '\n'
                while '\n\n' in cell:
                    cell = cell.replace('\n\n', '\n')
                # 删除开头的 '\n'
                cell = cell.lstrip('\n')
                # 删除结尾的 'None'
                if cell.endswith('None'):
                    cell = cell[:-4]
                # 删除结尾的 '\n'
                cell = cell.rstrip('\n')
                # 返回处理结果
                data[i][j] = cell
        return data
    
    new_cell_data = handling_two_dimensional_list_data(new_cell_data)
    print(f"处理后单元格数据：{new_cell_data}")

    api = FeishuOpenAPI()
    response = api.write_sheet_data(rcd_range, new_cell_data)
    return response, new_cell_data, old_cell_data

def insert_current_time(line_data):
    current_time = datetime.now().strftime("%H:%M")
    
    if line_data == "[起床[]起床]" or line_data == "[入睡[]入睡]":
        line_data = line_data.replace("[]", f"[{current_time}]")
    
    return line_data

if __name__ == "__main__":
    send_imessage("test 222")
