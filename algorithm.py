import pandas as pd
from itertools import combinations_with_replacement,product
from collections import Counter 
import copy


#인풋값
input_element = ['H','O', 'C']

def start(input_element):
    ot_name = {'H':'수소', 'Na':'나트륨', 'K':'포타슘', 
           'Be':'베릴륨', 'Ca':'칼슘',
           'B':'붕소',
           'C':'탄소',
           'N':'질소','P':'인',
           'O':'산소','S':'황',
           'F':'플루오르','Cl':'염소'}

    all_mole = list(pd.read_excel("화합물 결합 각도 정리 파일.xlsx")['분자'])[:28]
    all_atom = ["H","Na","K","Be","Ca","B","C","N", "P","O", "S","F", "Cl"]


    for i in range(len(all_mole)-1,-1,-1):
        tmp = True
        for j in list(set(all_atom) - set(input_element)):
            if j  in all_mole[i]:
                tmp = False
        if tmp == False:
            del all_mole[i]

    answers = []
    answers = list(all_mole)
    for i in range(len(answers)):
        answers[i] = list(filter(bool,answers[i].replace('1','1+').replace('2','2+').replace('3','3+').replace('4','4+').split('+') ))

    atom = []
    num = []
    for i in answers:
        tmp_atom = []
        tmp_num = [] 
        for j in i:
            tmp_atom.append(j[:-1])
            tmp_num.append(j[-1])
        atom.append(tmp_atom)
        num.append(tmp_num)


    output= []
    for i in range(len(answers)):
        tmp = []
        for j in range(len(answers[i])):
            tmp.append(f'{ot_name[answers[i][j][0]]} {answers[i][j][1]}개({answers[i][j]})')
        output.append(tmp)
        
        
        
        #####
    for i in range(len(answers)):
        for j in range(len(answers[i])):
            answers[i][j] = answers[i][j].replace('1', '')

    show=[]
    if output:
        for i in range(len(output)):
            show.append(('와 '.join(output[i]),'분자식 : '+''.join(answers[i])))
            
            
    #bond_angle 분자 각도        
    df = pd.read_excel("./화합물 결합 각도 정리 파일.xlsx", index_col=0)
    bond_angle = []     
    for i in all_mole:
        bond_angle.append(list(df.loc[i]))  
    for i in range(len(bond_angle)):
        bond_angle[i] = [x for x in bond_angle[i] if pd.isnull(x) == False]
            
            

    string = ''
    for i in bond_angle:
        string += str(i) + '<br>'
    string = string.replace('[', '').replace(']', '')
            
           
    return show#, string


def bondInfo(mole):
    tmp = pd.read_excel("./화합물 결합 각도 정리 파일.xlsx", index_col=0)
    solve = [x for x in list(tmp.loc[mole]) if pd.isnull(x) == False]

    return str(solve).replace(']', '').replace('[', '')
    