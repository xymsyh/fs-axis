import json

# 函数用于记录单元格的历史修改记录
def record_history_cell(cell_id, modification):
    history = {'Cell ID': cell_id, 'Modification': modification}
    with open('history_cell.json', 'a') as file:
        json.dump(history, file)
        file.write('\n')

# 函数用于读取历史记录
def read_history_cell():
    history = []
    with open('history_cell.json', 'r') as file:
        for line in file:
            entry = json.loads(line)
            history.append(entry)
    return history

# 示例用法
if __name__ == '__main__':
    cell_id = 1  # 单元格的唯一标识符
    modification = '修改内容：添加新数据'
    
    record_history_cell(cell_id, modification)
    
    # 读取历史记录
    history = read_history_cell()
    for entry in history:
        print(f'Cell ID: {entry["Cell ID"]}, Modification: {entry["Modification"]}')
