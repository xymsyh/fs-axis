# api_methods.py

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

from autom_tbl_inp import standardize_table_format
from feishu_api import FeishuOpenAPI


def locate_now():
    data_full = standardize_table_format()
    data_value = data_full['data']['valueRange']['values'][0][0]
    data_range = data_full['data']['valueRange']['range']
    print (data_full)
    print (f'data_range: {data_range}')
    return data_value

def write_cell_data(cell_data):  
    if not cell_data:
        return None, cell_data
    
    raw_data_full = standardize_table_format()
    data_range = raw_data_full['data']['valueRange']['range']
    
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
    cell_data = [[cell_data]]
    response = api.write_sheet_data(data_range, cell_data)
    return response, cell_data

def write_line_data(line_data):  
    # 检查cell_data是否为空
    if not line_data:
        # response = {'msg': 'line_data为空', 'data': None}
        return None, line_data
      
    raw_data_full = standardize_table_format()
    raw_data_value = raw_data_full['data']['valueRange']['values'][0][0]
    data_range = raw_data_full['data']['valueRange']['range']

    from datetime import datetime
    timestamp = datetime.now().strftime("%m%d%H%M")
    cell_data = [[line_data + f" [{timestamp}]" + "\n" + str(raw_data_value)]]

    def process_data(data):
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
    
    cell_data = process_data(cell_data)
    print(f"处理后数据：{cell_data}")

    api = FeishuOpenAPI()
    response = api.write_sheet_data(data_range, cell_data)
    return response, cell_data
