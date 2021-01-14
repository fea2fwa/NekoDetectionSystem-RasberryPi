# -*- coding: utf-8 -*-
path = '/home/pi/.bashrc'

virtualenv_lines = ['# virtualenv and virtualenvwrapper\n', 
                    'export WORKON_HOME=$HOME/.virtualenvs\n',
                    'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3\n',
                    'source /usr/local/bin/virtualenvwrapper.sh\n']

lines = ''
try:
    with open(path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line in virtualenv_lines:
                continue
            else:
                lines += line
except Exception as e:
    print(path,'を新規に作成します。')

if lines[-2:] != '\n\n':
    lines += '\n'
lines += ''.join(virtualenv_lines)


with open(path, mode='w') as f:
    f.write(lines)

print(path,'に設定を追加しました。')