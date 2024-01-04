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

def write_line_data(line_data):    
    data_full = standardize_table_format()
    data_value = data_full['data']['valueRange']['values'][0][0]
    data_range = data_full['data']['valueRange']['range']

    line_data = line_data + "\n" + str(data_value)
    line_data = [[line_data]]
    print (f'data_range 01042240: {data_range}')
    print (f'line_data 01042240: {line_data}')

    api = FeishuOpenAPI()
    test_data = api.get_sheet_data("9ba2f5!C28:C28")['data']['valueRange']['values']
    print (f'test_data 01042257: {test_data}')

    result = api.write_sheet_data(data_range, line_data)
    # result = api.write_sheet_data("9ba2f5!C29:C29", test_data)
    return result
    # return data_value