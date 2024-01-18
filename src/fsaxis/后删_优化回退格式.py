# 定义原始文本
latest_1 = "2024-01-18 18:02:10: [['测试333 [01181802]\n测试222 [01181802]']]"
latest_2 = "2024-01-18 18:02:09: [['测试222 [01181802]']]"

# 去除开始和结尾的特定部分
# 假设时间戳和格式固定，我们可以直接通过字符数来切片
start_slice = len("2024-01-18 18:02:XX: [['")
end_slice = len("']]")

# 处理两个文本
processed_text1 = latest_1[start_slice:-end_slice]
processed_text2 = latest_2[start_slice:-end_slice]

# 寻找不同部分
difference = processed_text1.replace(processed_text2, '').strip()

print(difference)

