import os

for item in os.listdir('.'):
    if os.path.isfile(item):
        continue

    os.chdir(item)
    for subi in os.listdir('.'):
        cmd = 'move "{i}" ..'.format(i=subi)
        print(cmd)
        os.system(cmd)

    os.chdir('..')
