# _*_ coding:utf-8 _*_
import re

if __name__ == "__main__":
    filename = 'data.txt'
    with open(filename,'r',encoding='UTF-8') as file_to_read:
        while True:
            lines = file_to_read.readline()
            sub_lines = lines[6:]
            has = sub_lines.find("(")
            if has ==-1:
                print(sub_lines.strip())
            else:
                p1 = re.compile(r'(.*?)[(]')  # 最小匹配
                freezer_kind = re.findall(p1, sub_lines)
                print(freezer_kind[0])
            if not lines:
                break

