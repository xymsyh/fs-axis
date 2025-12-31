import os
import shutil

def create_symbolic_links(source_dir, target_dir, file_pairs):
    """
    批量创建符号链接
    
    Args:
        source_dir (str): 源文件目录
        target_dir (str): 目标链接目录
        file_pairs (list): 文件名配对列表，格式为[(target_name, source_name), ...]
    """
    for target_name, source_name in file_pairs:
        target_path = os.path.join(target_dir, target_name)
        source_path = os.path.join(source_dir, source_name)
        
        # 检查源文件是否存在
        if not os.path.exists(source_path):
            print(f"源文件不存在: {source_path}")
            continue
            
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 如果目标文件已存在，先删除
        if os.path.exists(target_path):
            try:
                if os.path.islink(target_path):
                    os.remove(target_path)
                else:
                    os.unlink(target_path)
            except OSError as e:
                print(f"删除现有文件失败: {target_path} - {e}")
                continue
        
        # 创建符号链接
        try:
            os.symlink(source_path, target_path)
            print(f"成功创建链接: {target_path} -> {source_path}")
        except OSError as e:
            print(f"创建链接失败: {target_path} -> {source_path} - {e}")

# 定义文件配对关系
file_pairs = [
    ('feishu_api.py', 'feishu_api.py'),
    ('autom_tbl_inp.py', 'autom_tbl_inp.pyw'),
    ('json_cached.json', 'json_cached.json'),
    ('json_config.json', 'json_config.json'),
    ('json_keywords.json', 'anal/json_keywords.json'),
    ('write_image.py', 'write_image.py')
]

# 设置源目录和目标目录
source_directory = r'D:\R2025\RPA\fs_api'
target_directory = r'D:\R2025\RPA\fsaxis\src\fsaxis'

# 执行创建
create_symbolic_links(source_directory, target_directory, file_pairs)