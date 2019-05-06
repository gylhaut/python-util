a = [1,2,3]
b=[]
for i in a:
    b.append(i+2)
print(b)

a = [1,2,3]
b = [i+2 for i in a]
print(b)
d = {'today':20,'tomorrow':30}
print(d)

print(d['tomorrow'])
print(dict.fromkeys(['today','tomorrow'],[20,40]))

print(dict([['today',20],['tomorrow',30]]))

a = {1,3,4,4,5}
print(a)

b = set([2,1,3,3,4])
print(b)
s = a| b # 并集
t = a & b # 交集
print(s)
print(t)