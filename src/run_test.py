import subprocess
import shutil
import os
from datetime import datetime #本及前未测试，若有问题回退前前版即可

def get_latest_git_commit_message():
    """ 获取最新的 Git 提交描述 """
    try:
        commit_message = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], text=True).strip()
        return commit_message
    except subprocess.CalledProcessError as e:
        print(f"获取 Git 提交描述失败: {e}")
        return None

def main():
    # 设置工作目录
    work_dir = "C:\\Users\\Ran\\Desktop\\fsaxis"
    os.chdir(work_dir)

    # 获取最新的 Git 提交描述
    commit_message = get_latest_git_commit_message()
    if not commit_message:
        print("无法获取 Git 提交描述，将继续使用时间戳作为文件名的一部分。")
        commit_message = "NoCommitMessage"

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 执行 briefcase package android -p debug-apk
    subprocess.run(["briefcase", "package", "android", "-p", "debug-apk"], check=True)

    # 复制 APK 文件
    apk_source = work_dir + "\\dist\\fsaxis-0.0.1.debug.apk"
    apk_dest = f"C:\\Users\\Ran\\Desktop\\测试apk留档\\fsaxis-0.0.1.debug_{timestamp}_{commit_message}.apk"
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
    main()
