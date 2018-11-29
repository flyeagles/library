import os

for item in os.listdir('.'):
    if os.path.isfile(item):
        continue

    os.chdir(item)
    for subi in os.listdir('.'):
        os.system('move {i} ..'.format(i=subi))

    os.chdir('..')
