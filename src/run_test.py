import argparse
import subprocess
import shutil
import os
from datetime import datetime

def main(app_name):
    # 设置工作目录
    work_dir = f"C:\\Users\\Ran\\Desktop\\{app_name}"
    os.chdir(work_dir)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 执行 briefcase package android -p debug-apk
    subprocess.run(["briefcase", "package", "android", "-p", "debug-apk"], check=True)

    # 复制 APK 文件
    apk_source = work_dir + f"\\dist\\{app_name}-0.0.1.debug.apk"

    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 创建包含日期的新文件夹路径
    new_folder_path = os.path.join("C:\\Users\\Ran\\Desktop\\测试apk留档", current_date)

    # 如果文件夹不存在，则创建它
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # 更新apk_dest以包含新的文件夹路径
    apk_dest = os.path.join(new_folder_path, f"{app_name}_{timestamp}.apk")
    # apk_dest = f"C:\\Users\\Ran\\Desktop\\测试apk留档\\{app_name}-0.0.1.debug_" + timestamp + ".apk" #请修改这部分的逻辑。在测试apk留档下面，新建一个名为当前日期的文件夹，然后再进行后续操作
    shutil.copy(apk_source, apk_dest)

    # 执行 briefcase package android -p apk -u
    subprocess.run(["briefcase", "package", "android", "-p", "apk", "-u"], check=True)

    # 运行 briefcase run android --log 并自动选择设备
    process = subprocess.Popen(["briefcase", "run", "android", "--log"], stdin=subprocess.PIPE, text=True)
    output, error = process.communicate("1\n")

    # 检查输出以确定是否选择了正确的设备
    if "V2324A" in output:
        print("Device V2324A selected.")
    else:
        print("Manual selection required.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('app_name', type=str, help='Name of the app')

    args = parser.parse_args()
    main(args.app_name)
