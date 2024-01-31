def parse_time_zone_string(time_zone_str):
            # 如果字符串为空，返回默认值0
            if not time_zone_str:
                return 0

            # 验证字符串是否只包含数字、加号和减号
            if all(c in '0123456789+-' for c in time_zone_str):
                try:
                    # 计算表达式的值
                    time_zone_value = eval(time_zone_str)
                    return time_zone_value
                except Exception as e:
                    # 如果表达式无效或计算过程中发生错误
                    print(f"无法解析时区字符串: {time_zone_str}. 错误: {e}")
                    return None
            else:
                print(f"时区字符串包含无效字符: {time_zone_str}")
                return None

time_zone = parse_time_zone_string("-3+3") #待修改完毕
print(time_zone)

# 测试git钩子