def format_line(keyword_left, formatted_value, keyword_right):
    # 检测是否包含"支出"
    if "支出" in keyword_left:
        # 检测是否符合「数字+文本」格式
        if formatted_value[0].isdigit():
            # 分离数字和文本
            digit_part = ''.join(filter(str.isdigit, formatted_value))
            text_part = ''.join(filter(lambda x: not x.isdigit(), formatted_value))
            # 重新组合字符串
            return f'{keyword_left}{digit_part}{keyword_right}{text_part}'
    # 如果不包含"支出"或不符合格式，保持原样
    return f'{keyword_left}{formatted_value}{keyword_right}'

# 示例
keyword_left = "[支出类别["
formatted_value = "11文本"
keyword_right = "]支出类别]"

result = format_line(keyword_left, formatted_value, keyword_right)
print(result)