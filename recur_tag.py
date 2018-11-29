import os

import tag_file_with_folder_name

for item in os.listdir('.'):
    if os.path.isfile(item):
        continue

    tag_file_with_folder_name.tag_file_with_folder_name(item, False, False)
    