import re
str = 'ISNULL(t.RoomNo,'') AS room_no,'
result = re.findall('AS ([a-zA-z]*,)', str, flags=0)
print(result[0])
