import os

for item in os.listdir('.'):
    new_name = item.replace('&','.').replace(' ', '.').replace('..', '.')
    os.rename(item, new_name)

for item in os.listdir('.'):
    new_name = item.replace('..', '.')
    os.rename(item, new_name)
