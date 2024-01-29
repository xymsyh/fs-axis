import re

def format_value(keyword_left, formatted_value, keyword_right):
    # 检查keyword_left是否包含"支出"
    if "支出" in keyword_left:
        # 使用正则表达式提取数字和文本部分
        match = re.match(r"(\d+)(.*)", formatted_value)
        if match:
            # 将数字和文本部分分别提取出来
            numbers = match.group(1)
            text = match.group(2)
            # 按新格式组合
            return f"{keyword_left}{numbers}{keyword_right}{text}"
    # 如果不包含"支出"或者没有匹配到格式，返回原始格式
    return f"{keyword_left}{formatted_value}{keyword_right}"

# 示例
keyword_left = "[支出类别["
formatted_value = "11222 文本99"
keyword_right = "]支出类别]"

result = format_value(keyword_left, formatted_value, keyword_right)
print(result)