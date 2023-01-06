import argparse
import ast

# import os
#print (os.getcwd())

def file2str(file_n):
    # python-file to string
    
    parsed = ast.parse(open(file_n,encoding="utf-8").read())
    for node in ast.walk(parsed):
        # let's work only on functions & classes definitions
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            continue
        if not len(node.body):
            continue
        if not isinstance(node.body[0], ast.Expr):
            continue
        if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
            continue
        node.body = node.body[1:]
    
    s = ast.dump(parsed).replace('\n', '')
    return s 

# https://habr.com/ru/post/676858/
# вычисляем само расстояние между двумя строками (возвращает к-во требуемых вставок/удалений/замен)
def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]
# нормировка: можно разделить редакционное расстояние на длину текста

#check out #1
#str1 = file2str('files/arima.py')
#str2 = file2str('files/autoarima.py')
#str2 = file2str('plagiat1/arima.py')
#out = levenstein(str1,str2)/max(len(str1),len(str2))
#print (round(out,3))


## MAIN


parser = argparse.ArgumentParser()
parser.add_argument('input',  type=str)
parser.add_argument('output', type=str)

args = parser.parse_args()

file1 = open(str(args.input), "r")
lines = file1.readlines()
for line in lines:
    # split
    str_1, str_2 = line.split(' ')
    print(str_1+' vs '+str_2)
    # code
    str1 = file2str(str_1.replace('\n',''))
    str2 = file2str(str_2.replace('\n',''))
    out = levenstein(str1,str2)/max(len(str1),len(str2))
    # дозапись скора в файл
    with open(str(args.output), 'a') as f_in:
        f_in.write(str(round(out,4))+'\n')
    
file1.close
