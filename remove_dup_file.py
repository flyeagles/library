import os
import stat
import datetime
import subprocess
import argparse
import pickle

import send2trash

import book_tree_view
import sharevars

cwd = os.getcwd()

def pretty_print(dup_list):
    print("Keep", dup_list[0])
    print("Del ", dup_list[-1])
    return os.path.join(cwd, dup_list[0][1], dup_list[0][0]), \
        os.path.join(cwd, dup_list[-1][1], dup_list[-1][0])


def remove_dup_files(noopenfile, skip_size_set):
    start_time = datetime.datetime.now()

    a_df = book_tree_view.AllBookTreeView.get_gen_book_index_dataframe(sharevars.lib_index_file, sharevars.target_folder)

    dup_df = a_df.groupby(['size']).filter(lambda x: len(x) > 1)
    #print(dup_df['title'].apply(lambda x: len(x)))
    dup_df['title_len'] = dup_df['title'].apply(lambda x: len(x))

    sorted_df = dup_df.sort_values(by=['size', 'title_len'],ascending=False)

    prev_size = sorted_df['size'].max()
    print('============', prev_size)
    dup_list = []
    deleted = False
    for item in sorted_df.iterrows():
        it = item[1]
        filename = it[2]
        folder = it[1]
        size = it[5]


        if size != prev_size:
            # handle dup_list.
            keep_file, del_file = pretty_print(dup_list)

            if prev_size in skip_size_set:
                # ignore file sizes in skip-set
                print("Skip these files.")
            else:
                if not noopenfile:
                    subprocess.Popen(r'explorer /select,"{p}"'.format(p=str(keep_file)))
                    subprocess.Popen(r'explorer /select,"{p}"'.format(p=str(del_file)))

                to_delete = False
                ans = input("Do you want to delete the dup files?(yes/no/skip/reverse):")
                if ans == 'n':
                    break
                elif ans == 's':
                    skip_size_set.add(prev_size)
                elif ans == 'r':
                    # reverse the selection of keep and delete.
                    del_file = keep_file
                    del_idx = 0
                    to_delete = True
                else:
                    del_idx = -1
                    to_delete = True

                if to_delete:
                    # delete
                    print("delete", str(del_file))

                    a_df = a_df[ (a_df.filename!=dup_list[del_idx][0]) | (a_df.folder!=dup_list[del_idx][1])]
                    
                    #deleted = True
                    #break

                    os.chmod(del_file, stat.S_IWRITE)
                    send2trash.send2trash(os.path.abspath(str(del_file)))  # os.path.abspath() is necessary to send file to recycle bin.

                    deleted = True

            dup_list = [(filename, folder)]
            print('============', size)
        else:
            # add item to dup_list
            dup_list.append((filename, folder))

        prev_size = size
        #print(title, folder)

    if deleted:
        a_df.to_pickle(sharevars.lib_index_file)    

    time_in_sec = datetime.datetime.now() - start_time
    print("Processed {c} files in {t} seconds.".format(c=len(dup_df.index),t=time_in_sec))

SKIP_SIZE_FILE = 'skip_size_check.pkl'

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Remove duplicated files based on file size.')

    argparser.add_argument("--noopenfile", dest='noopenfile', 
                           default=False, required=False,
                           action='store_true',
                           help='Opne file in folder for verification.')

    args = argparser.parse_args()

    if os.path.exists(SKIP_SIZE_FILE):
        with open(SKIP_SIZE_FILE, 'br') as read_file:
            skip_size_set = pickle.load(read_file)
    else:
        skip_size_set = set()

    remove_dup_files(args.noopenfile, skip_size_set)

    with open(SKIP_SIZE_FILE, 'bw') as write_file:
        pickle.dump(skip_size_set, write_file)