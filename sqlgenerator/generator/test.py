import re

str='[UpdateTime] update_time bigint NULL ,'



result=re.match('.*(bigint).*',str)

print(result[0])
