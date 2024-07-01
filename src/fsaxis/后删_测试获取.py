# app.py

版本说明 = "a2更新为2024-05-31" 

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

import _method
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading
import api_methods
import history_methods
import history_layout
import widget_methods
import json
import feishu_api
api = feishu_api.FeishuOpenAPI()

