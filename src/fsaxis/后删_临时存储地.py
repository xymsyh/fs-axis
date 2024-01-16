import re

# 原始文本
text = "[测试1[测试2[测试3]测试1]测试2]"

# 第一步：非贪婪匹配首个[]中的内容
# 使用正则表达式匹配第一个括号内的内容。这里的.*?表示非贪婪匹配，即尽可能少的匹配字符。
pattern_step1 = r"\[.*?\]"
result_step1 = re.search(pattern_step1, text).group()

# 第二步：贪婪匹配result_step1中的最后一个[之前的所有内容
# 在第一步的结果中，寻找最后一个出现的"["及其后的所有字符。这里的.*表示贪婪匹配，尽可能多的匹配字符。
pattern_step2 = r"\[.*\["
result_step2 = re.search(pattern_step2, result_step1).group()

# 第三步：删除result_step2前后的[
# 从第二步的结果中去除两端的"["，以得到最终结果。
result_final = result_step2.strip('[')

result_final