import os

for item in os.listdir('.'):
    if os.path.isdir(item):
        continue
        
    pos = item.rindex('.')
    name = item[:pos]
    print(name)
    cmd = '7z x -o"{f}" "{i}"'.format(f=name, i=item)
    print(cmd)
    os.system(cmd)