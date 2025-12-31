import os
import sys

def create_symbolic_links():
    """
    批量创建符号链接
    源文件来自 D:\R2025\RPA\fs_api\
    目标链接创建在 D:\R2025\RPA\fsaxis\src\fsaxis\
    """
    
    # 源目录和目标目录
    source_dir = r"D:\R2025\RPA\fs_api"
    target_dir = r"D:\R2025\RPA\fsaxis\src\fsaxis"
    
    # 需要创建链接的文件列表
    files_to_link = [
        "feishu_api.py",
        "autom_tbl_inp.py", 
        "json_cached.json",
        "json_config.json",
        "json_keywords.json",
        "write_image.py"
    ]
    
    print("🚀 开始批量创建符号链接...")
    print(f"源目录: {source_dir}")
    print(f"目标目录: {target_dir}")
    print("-" * 50)
    
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    for filename in files_to_link:
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        try:
            # 检查源文件是否存在
            if not os.path.exists(source_path):
                print(f"❌ 错误: 源文件不存在 - {source_path}")
                error_count += 1
                continue
            
            # 如果目标链接已存在，先删除
            if os.path.exists(target_path) or os.path.islink(target_path):
                try:
                    os.remove(target_path)
                    print(f"📝 已删除现有文件: {filename}")
                except Exception as e:
                    print(f"⚠️  无法删除现有文件 {filename}: {e}")
                    error_count += 1
                    continue
            
            # 创建符号链接
            os.symlink(source_path, target_path)
            print(f"✅ 成功创建: {filename}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 创建 {filename} 失败: {e}")
            error_count += 1
    
    print("-" * 50)
    print(f"📊 完成统计:")
    print(f"   成功: {success_count} 个")
    print(f"   失败: {error_count} 个")
    
    if error_count == 0:
        print("🎉 所有符号链接创建成功！")
    else:
        print("⚠️  部分链接创建失败，请检查错误信息。")

if __name__ == "__main__":
    # 检查操作系统（Windows需要管理员权限）
    if sys.platform == "win32":
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("⚠️  在Windows上创建符号链接可能需要管理员权限。")
            print("   请以管理员身份运行此脚本。")
    
    create_symbolic_links()