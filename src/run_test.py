import subprocess
import shutil
import os
from datetime import datetime

# 设置工作目录
work_dir = "C:\\Users\\Ran\\Desktop\\fsaxis"
os.chdir(work_dir)

# 生成时间戳
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 执行 briefcase package android -p debug-apk
subprocess.run(["briefcase", "package", "android", "-p", "debug-apk"], check=True)

# 复制 APK 文件
apk_source = work_dir + "\\dist\\fsaxis-0.0.1.debug.apk"
apk_dest = "C:\\Users\\Ran\\Desktop\\测试apk留档\\fsaxis-0.0.1.debug_" + timestamp + ".apk"
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
