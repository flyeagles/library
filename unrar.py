import os

for item in os.listdir('.'):
    pos = item.rindex('[')
    name = item[:pos-1]
    print(name)
    cmd = '7z x -o{f} {i}'.format(f=name, i=item)
    print(cmd)
    os.system(cmd)