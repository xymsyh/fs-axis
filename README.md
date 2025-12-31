# 部署流程

1. 将 fs_api 下载在 D:\R2025\RPA 文件夹下，跳转链接：https://github.com/xymsyh/fs_api_example
2. 将 本文件夹 下载在 D:\R2025\RPA 文件夹下
3. 管理员权限运行 "README.创建符号链接.py" 以创建需要的符号链接
4. 运行 "briefcase dev" 可以直接在开发环境中运行 fsaxis 应用

# 打包

1. 运行 "briefcase create android" 创建安卓项目
2. 运行 "briefcase build android" 构建安卓项目
3. 运行 "briefcase run android" 在安卓模拟器或连接的安卓设备上运行应用（请数据线连接手机并打开USB调试）

# 其他问题

如何拓展行数：在 https://rcentral.feishu.cn/wiki/Gki5wAsavi11OjkFa8YcNS33nzh （替换为你的配置） 
的飞书表格中右键第二行 “向上插入X行” 并同步更新在 json_config.json 中的 a2_date 进行更新定义
当更新了 a2_data 后，必须重新执行打包的三步流程才能在手机端进行更新