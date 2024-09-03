import json

# 读取原始文件喵~(●'◡'●)
input_file = './datasets/html-understanding/data/html_understanding_button.jsonl'
output_file = './datasets/html-understanding/data/html_understanding_button_top10.jsonl'

# 准备一个可爱的列表来存放前十个数据(≧▽≦)
top_10_data = []

# 开始读取文件啦，喵呜~(^･ｪ･^)
with open(input_file, 'r', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i < 10:
            top_10_data.append(json.loads(line.strip()))
        else:
            break  # 喵喵只要前10个哦~(ﾉ≧∀≦)ﾉ

# 把可爱的数据写入新文件里(｡･ω･｡)ﾉ♡
with open(output_file, 'w', encoding='utf-8') as file:
    for item in top_10_data:
        json.dump(item, file, ensure_ascii=False)
        file.write('\n')

print(f"喵呜~✧*。前10个数据已经被可爱地保存到 {output_file} 啦！(≧▽≦)/ ")