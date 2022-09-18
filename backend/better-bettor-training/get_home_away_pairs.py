import csv
import pickle
from dataclasses import dataclass

data = []
with open("./datasets/results_00_19.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)
header = data.pop(0)

data2 = []
with open("./datasets/test20_22.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        data2.append(row)
data2.pop(0)

header_pos_map = {}
for n, i in enumerate(header):
    header_pos_map[i] = n

training_list = data + data2

input_data = {}
count = 0
for i in training_list:
    if (i[2], i[3]) not in input_data:
        count += 1
        input_data[(i[2],i[3])] = []
    input_data[(i[2],i[3])].append(
        {
            "DateTime": i[1],
            #'FTR': i[header_pos_map['FTR']],
            'HS': i[header_pos_map['HS']],
            'AS': i[header_pos_map['AS']],
            'HST': i[header_pos_map['HST']],
            'AST': i[header_pos_map['AST']],
            'HF': i[header_pos_map['HF']],
            'AF': i[header_pos_map['AF']],
            'HC': i[header_pos_map['HC']],
            'AC': i[header_pos_map['AC']],
            'HY': i[header_pos_map['HY']],
            'AY': i[header_pos_map['AY']],
            'HR': i[header_pos_map['HR']],
            'AR': i[header_pos_map['AR']]
        }
    )
print("홈팀-어웨이팀 총 짝 수:", len(input_data))

with open("match_data.pickle", "wb") as f:
    pickle.dump(input_data, f)
print("match_data.pickle로 경기 결과가 저장되었습니다.")