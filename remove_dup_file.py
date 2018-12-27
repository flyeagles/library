import os
from stat import S_IREAD
import datetime
import subprocess

import book_tree_view
import sharevars

cwd = os.getcwd()

def pretty_print(list_tuple):
    print("Keep", list_tuple[0])
    for item in list_tuple[1:]:
        print(item)
    return os.path.join(cwd, dup_list[0][1], dup_list[0][0]), \
        os.path.join(cwd, dup_list[-1][1], dup_list[-1][0])

if __name__ == "__main__":
    start_time = datetime.datetime.now()

    a_df = book_tree_view.AllBookTreeView.get_gen_book_index_dataframe(sharevars.lib_index_file, sharevars.target_folder)
    dup_df = a_df.groupby(['size']).filter(lambda x: len(x) > 1)
    #print(dup_df['title'].apply(lambda x: len(x)))
    dup_df['title_len'] = dup_df['title'].apply(lambda x: len(x))

    sorted_df = dup_df.sort_values(by=['size', 'title_len'],ascending=False)

    prev_size = sorted_df['size'].max()
    print('============', prev_size)
    count = 0
    dup_list = []
    for item in sorted_df.iterrows():
        it = item[1]
        title = it[2]
        folder = it[1]
        size = it[5]
        if size != prev_size:
            # handle dup_list.
            keep_file, del_file = pretty_print(dup_list)
            print(str(keep_file))

            subprocess.Popen(r'explorer /select,"{p}"'.format(p=str(keep_file)))
            subprocess.Popen(r'explorer /select,"{p}"'.format(p=str(del_file)))

            ans = input("Do you want to delete the dup files?(yes/no):")
            if ans == 'n':
                break
            
            print("delete", str(del_file))
            
            dup_list = [(title, folder)]
            print('============', size)
        else:
            # add item to dup_list
            dup_list.append((title, folder))

        prev_size = size
        #print(title, folder)

        count += 1
        if count > 100:
            break



    time_in_sec = datetime.datetime.now() - start_time
    print("Processed {c} files in {t} seconds.".format(c=len(dup_df.index),t=time_in_sec))
