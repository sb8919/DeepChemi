import pandas as pd
from itertools import combinations_with_replacement,product
from collections import Counter 
import copy
import numpy as np

# 최 외각 전자의 옥텟 규칙 정리 1족~7족
ot = {1:["H","Na","K"], 
      2:["Be","Ca"],
      3:["B"],
      4:["C"],
      5:["N", "P"],
      6:["O", "S"],
      7:["F", "Cl"]
     }

ot_name = {'H':'수소', 'Na':'나트륨', 'K':'포타슘', 
           'Be':'베릴륨', 'Ca':'칼슘',
           'B':'붕소',
           'C':'탄소',
           'N':'질소','P':'인',
           'O':'산소','S':'황',
           'F':'플루오르','Cl':'염소'}

data = pd.read_excel('결합길이 정리 파일.xlsx',index_col = 0)
angle_data = pd.read_excel('화합물 결합 각도 정리 파일.xlsx',index_col = 0)
data = data.replace('x',0)

idx,combination_no,p = [],[],0
# idx: 엑셀파일에 있는 결합할 수 없는 원소들의 2차원 위치를 뽑기 위함
# combination_no : 결합할 수 없는 원소들의 순서쌍
# p : 2차원의 data가 전치행렬이기때문에 중복을 피하기 제어 변수로 씀
ndarr_data = data.values
for r,v1 in enumerate(ndarr_data):
    for c in range(p,len(v1)):
        if ndarr_data[r][c]==0:idx.append((r,c))
    p+=1

for r,c in idx:
    combination_no.append((data.index[r],data.columns[c]))


def bond_angle(input_element,element_num=2):
    '''분자 리스트에서 원소들간에 결합 각도를 반환해줍니다.
    ex){'H2S': {'H-S-H': 93}, 'CH2O': {'H-C=O': 122, 'H-C-H': 117.0},'CH2S': {},}
    엑셀파일에 없는 결합 조합은 빈 딕셔너리로...
'''
    
    # element_num=2 : 기본값 2 (원소개수 제한 없음)
    # element_num=1 : 원소개수 4개만
    
    input0 = input_element # input 예시 H O F S
    ot_key = []
    for i in input0:
        for k,v_list in ot.items():
            if i in v_list:
                ot_key.append(k);break

    dic = {v:k for k,v in zip(ot_key,input0)}

    # 하나의 원소로는 8을 만들수 없으므로 2개,3개,4개의 원소로 이루어진 중복조합의 경우의 수를 구함
    all_case,s=[],0
    for i in range(int(element_num),5):
        for j in combinations_with_replacement(list(map(list,dic.items())),i):
            lst = list(j)
            # print(lst)
            if sum(j[k][1] for k in range(i)) == 8:
                all_case.append(lst)
                continue
                
            for k in range(i):
                lst_tmp = copy.deepcopy(lst)
                if lst_tmp[k][1] > 4:
                    lst_tmp[k][1]=8-j[k][1]
                s+=lst_tmp[k][1]
            if s==8:
                all_case.append(lst_tmp)
            s=0

    combination_proba=[]
    for case in all_case:
        tmp1=[case[i][0] for i,v in enumerate(case)]
        combination_proba.append(tmp1)
    answers=[] 
    
    for c in combination_proba:
        for a,b in  combination_no:
            tmp2=c[:]
            if a in tmp2:
                tmp2.remove(a)
                if b in tmp2:break
        else:
            answers.append(c)

    molecular_formula = [] # 추가
    no_num_molecular_formula = [] # 추가
    
    sub = str.maketrans("123456789", "₁₂₃₄₅₆₇₈₉")
    output = []
    show = []
    for i in answers: # 최종 결과를 아래첨자 분자 표현식으로 가공
        dic_tmp = Counter(i)
        
        no_num_molecular_formula.append(sorted(dic_tmp.keys())) # 추가
        molecular_formula.append([f'{k}{str(v).translate(sub)}'for k,v in dic_tmp.items()]) # 추가
        
        output.append([f'{ot_name[k]} {v}개({k}{str(v).translate(sub)})'for k,v in sorted(dic_tmp.items(), key=lambda x:x[1])])
    
    # 각 리스트를 알파벳 순으로 정렬 
    for idx, i in enumerate(molecular_formula):
        molecular_formula[idx] = sorted(i, key = lambda x : x[0])

    # 1. 화학식의 원소 순서는 원소 기호의 알파벳 순서로 나열
    # 2. 탄소가 화학식에 포함된 경우 탄소를 먼저 쓰고, 그 다음에는 수소 그 다음 원소는 알파벳 순으로 나열
    # 3. 산화물에서는 산소를 맨 마지막에 쓴다.
    # 4. 산은 수소를 맨 앞에 쓴다.
    # 5. 이온 결합물은 알파벳 순서와 상관없이 양이온을 먼저 쓰고 음이온을 쓴다.

    # 5 번을 제외한 힐 시스템 규칙 적용  
    for i in range(len(no_num_molecular_formula)): # 추가
        if 'H' in no_num_molecular_formula[i]:
            no_num_molecular_formula[i].insert(0,no_num_molecular_formula[i].pop(no_num_molecular_formula[i].index('H')))
            molecular_formula[i].insert(0,molecular_formula[i].pop(no_num_molecular_formula[i].index('H')))
            
        if 'C' in no_num_molecular_formula[i]:
            no_num_molecular_formula[i].insert(0,no_num_molecular_formula[i].pop(no_num_molecular_formula[i].index('C')))
            molecular_formula[i].insert(0,molecular_formula[i].pop(no_num_molecular_formula[i].index('C')))
            
        if 'O' in no_num_molecular_formula[i]:
            no_num_molecular_formula[i].append(no_num_molecular_formula[i].pop(no_num_molecular_formula[i].index('O')))
            molecular_formula[i].append(molecular_formula[i].pop(no_num_molecular_formula[i].index('O')))
    

    angle_data = pd.read_excel('화합물 결합 각도 정리 파일.xlsx',index_col = 0)

    table = str.maketrans('₁₂₃₄₅₆₇₈₉', '123456789')

    for i in range(len(molecular_formula)):
        molecular_formula[i] = ("".join(molecular_formula[i]).translate(table)).replace('1', '')

    molecular_formula
    angle_dict = {}

    for i in range(len(molecular_formula)):
        angle_dict[''.join(molecular_formula[i])] = {}

    for i in molecular_formula:
        try:
            for j in range(0,4,2):
                if np.isnan(list(angle_data.loc[i])[j+1]) == False:
                    angle_dict[i][list(angle_data.loc[i])[j]] =  list(angle_data.loc[i])[j+1]
        except:
            pass
    #        print(list(angle_data[i]))
    return angle_dict
bond_angle(['C','O','H','S'])


