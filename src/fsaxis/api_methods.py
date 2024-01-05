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

def write_line_data(cell_data):    
    data_full = standardize_table_format()
    data_value = data_full['data']['valueRange']['values'][0][0]
    data_range = data_full['data']['valueRange']['range']

    cell_data = [[cell_data + "\n" + str(data_value)]]

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
                data[i][j] = cell
                # 删除结尾的 '\n'
                cell = cell.rstrip('\n')

        return data
    
    cell_data = process_data(cell_data)

    api = FeishuOpenAPI()
    response = api.write_sheet_data(data_range, cell_data)
    return response, cell_data
