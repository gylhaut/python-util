# 三引号让程序员从引号和特殊字符串的泥潭里面解脱出来

import re
case_name = "TTestSSAdvanceRepayRequest"



def analyField(fieldname):
    old_column_name = fieldname
    new_column_name = ''
    if (len(old_column_name) > 2):
        new_column_name = old_column_name[0]
        for i in range(1, len(old_column_name) - 1):
            split_str0 = old_column_name[i - 1]
            split_str1 = old_column_name[i]
            split_str2 = old_column_name[i + 1]
            if ((split_str0 != '_') & split_str1.isupper() & split_str2.islower()):
                new_column_name = new_column_name + '_' + split_str1.lower()
            elif (split_str0.islower() & split_str1.isupper()):
                new_column_name = new_column_name + '_' + split_str1.lower()
            else:
                new_column_name = new_column_name + split_str1
        new_column_name = new_column_name + old_column_name[-1]
    else:
        new_column_name = old_column_name.lower()
    return new_column_name.lower()

str_name = re.sub("[A-Z]", lambda x: "_" + x.group(0).lower() if not x.span() == (0,1) else x.group(0).lower(), case_name)

ss = lower_convert(case_name)
print(ss)
