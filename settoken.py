# -*- coding: utf-8 -*-
path = '/home/pi/.netrc'
token_section = '\nmachine notify-api\n\tpassword '

token = input('トークン: ')
token_section += token
token_section += '\n'

lines = ''
try:
    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if 'machine notify-api' in line:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    else:
                        if 'machine' in line:
                            break
            lines += line
except Exception as e:
    print(path,'を新規に作成します。')

lines += token_section

with open(path, mode='w') as f:
    f.write(lines)

print(path,'に設定を追加しました。')