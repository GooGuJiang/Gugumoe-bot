import os
cmd = 'python bot3.py'
while True:
    res = os.popen(cmd)
    output_str = res.read()   # 获得输出字符串
    print(output_str)