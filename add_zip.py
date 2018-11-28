import os

for item in os.listdir('.'):
    if os.path.isfile(item):
        continue

    print(item)

    cmd = '7z a -tzip -mx=0 {i}.zip {i}'.format(i=item)

    print(cmd)
    os.system(cmd)