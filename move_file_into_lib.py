# by yluo, November 2018

import argparse
import os
import pickle
import shutil
import datetime
import time

MAX_FILES_FOLDER = 500
MOVE_TARGET_LIB_DATA_FILE = 'lib_move_target.pkl'

def add_size_data_to_index(size_index, size, a_file, root):
    if size in size_index:
        size_index[size].append((a_file, root))
    else:
        size_index[size] = [(a_file, root)]

def get_file_surfix(fname):
    try:
        pos = fname.rindex('.')
        return fname[pos+1:].lower()
    except ValueError:
        return ''

def save_target_folder_data(target_folder_data):
    with open(MOVE_TARGET_LIB_DATA_FILE, 'wb') as WFILE:
        pickle.dump(target_folder_data, WFILE)


def get_target_folder_files(to_folder):
    if os.path.exists(MOVE_TARGET_LIB_DATA_FILE):
        with open(MOVE_TARGET_LIB_DATA_FILE, 'rb') as RFILE:
            target_folder_data = pickle.load(RFILE)
    else:
        target_folder_data = get_target_folder_files_from_system(to_folder)
        save_target_folder_data(target_folder_data)

    return target_folder_data


def get_target_folder_files_from_system(to_folder):
    '''
    return (file_data, start_fd, file_count_in_fd, size_index)
    Structure of file_data:
        map: file_name --> (size, path to file)
    Structure of size_index:
        map: size --> (file_name, path)
    '''
    start_time = datetime.datetime.now()
    all_files = os.walk(to_folder)
    file_stats = {}
    size_index = {}  # mapping from file size to a list of names
    folder_file_count = {}
    for root, dirs, files in all_files:
        for a_file in files:
            new_cnt = folder_file_count.get(root, 0) + 1
            folder_file_count[root] = new_cnt
            file_stat = os.stat(os.path.join(root, a_file))
            file_stats[a_file] = (file_stat.st_size, root)

            add_size_data_to_index(size_index, file_stat.st_size, a_file, root)
    
    print("generate index file in ", datetime.datetime.now() - start_time)
    print(folder_file_count)

    if len(folder_file_count) == 0: # empty library folder yet
        folder_file_count['0001'] = 0
    target_subfolders = list(folder_file_count.keys())
    target_subfolders.sort(reverse=True)
    
    print("Will start moving file into folder:", target_subfolders[0])

    _, tail = os.path.split(target_subfolders[0])

    return file_stats, int(tail), folder_file_count[target_subfolders[0]], size_index

def handle_duplicated_files(files_in_lib, a_file, root, identical_files, size_index):
    this_size = os.path.getsize(os.path.join(root, a_file))
    if this_size == 0:
        time.sleep(1)
        this_size = os.path.getsize(os.path.join(root, a_file))   # when accessing Samba file via Windows, the size may be wrong.
    
    if a_file in files_in_lib:
        if this_size == files_in_lib[a_file][0]:
            print("---- Identical file {fn} at {fd} and {lpath}".format(fn=a_file,
                    fd=root, lpath=files_in_lib[a_file][1]))
            identical_files.append(os.path.join(root, a_file))
        else:
            print("Duplicated file {fn} at {fd} and {lpath}".format(fn=a_file,
                    fd=root, lpath=files_in_lib[a_file][1]))
        
        return True, this_size
    else:
        # check whether there is existing file with same exact size.
        if this_size in size_index:
            size_count = len(size_index[this_size])
            if  size_count == 1:
                print("---- Find file \n\t\t{fn} with exact size {sz} from {fd} and to \n\t\t{f2} in {lpath}".format(fn=a_file,
                        sz=this_size,fd=root, f2=size_index[this_size][0][0], lpath=size_index[this_size][0][1]))
            else:
                print("---- Find file \n\t\t{fn} with exact size {sz} from {fd} and to {cnt} existing books:".format(fn=a_file,
                        sz=this_size,fd=root, cnt=size_count))
                for (old_file, old_root) in size_index[this_size]:
                    print("\t\t{fn} in {fd}".format(fn=old_file, fd=old_root))

            ans = input("Do you still want to move this file?([y]es/[n]o)(default:No):")
            if ans == 'y':
                return False, this_size
            else:
                return True, this_size

    return False, this_size

def get_folder_id_count(start_fid, file_count):
    if file_count < MAX_FILES_FOLDER:
        return start_fid, file_count + 1
    else:
        return start_fid + 1, 1

from stat import S_IREAD, S_IWRITE


def move_from_to(from_folder, to_folder, delidentical, movezip, need_recursive):

    files_in_lib, start_fid, file_count, size_index = get_target_folder_files(to_folder)
    folder_name = '{:04d}'.format(start_fid)

    file_move = []
    all_files = os.walk(from_folder)    
    identical_files = []
    moved_count = 0
    zipped = False
    try:
        for root, dirs, files in all_files:

            for a_file in files:
                    
                surfix = get_file_surfix(a_file)
                if surfix == '7z' or ( (surfix == 'rar' or surfix == 'zip') and not movezip):
                    print('Skip zipped file:', a_file)
                    zipped = True
                    continue

                #print(root, a_file)
                duplicated, this_size = handle_duplicated_files(files_in_lib, a_file, root, identical_files, size_index)
                if duplicated:
                    continue
                
                # need move.
                start_fid, file_count = get_folder_id_count(start_fid, file_count)
                folder_name = '{:04d}'.format(start_fid)
                new_file_path = os.path.join(to_folder, folder_name, a_file)
                if os.path.exists(new_file_path):
                    print("====Found targt file existing! {f}".format(f=new_file_path))
                else:
                    # os.renames(os.path.join(root, a_file), new_file_path)
                    try:
                        old_file_path = os.path.join(root, a_file)
                        os.chmod(old_file_path, S_IWRITE)   # always make old file writable to enable move
                        shutil.move(old_file_path, new_file_path) # this support cross-disk move.
                        os.chmod(new_file_path, S_IREAD)
                    except FileNotFoundError as e:
                        head, _ = os.path.split(new_file_path)
                        os.mkdir(head)
                        shutil.move(old_file_path, new_file_path) # this support cross-disk move.
                        os.chmod(new_file_path, S_IREAD)

                    # update files_in_lib map
                    new_file_path = str(os.path.join(to_folder, folder_name))
                    files_in_lib[a_file] = (this_size, new_file_path)
        
                    add_size_data_to_index(size_index, this_size, a_file, new_file_path)

                    moved_count += 1
                    if moved_count % 100 == 0:
                        print("Has moved {d} files...".format(d=moved_count))

            if not need_recursive:
                break

    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)
    except OSError as e:
        print(e)

    print("Moved total {d} files.".format(d=moved_count))
    print('Folder', folder_name, 'has', file_count, 'files.')

    save_target_folder_data((files_in_lib, start_fid, file_count, size_index))

    if zipped:
        print("You can use '--movezip' command option to force move .zip files.")

    if delidentical and len(identical_files) > 0:
        print("========Deleting following {d} identical files!".format(d=len(identical_files)))
        print(identical_files)
        for id_file in identical_files:
            os.chmod(id_file, S_IWRITE)   # always make old file writable to enable move
            os.unlink(id_file)


def check_path_validity(dirstr):
    thelen = len(dirstr)
    if thelen >= 2 and dirstr[1] == ':':  # e.g., "E:"
        if thelen < 3 or dirstr[2] != '\\':  # e.g., "E:.\"
            print("Cannot use relative path on different drive.")
            exit(1)


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Move files from source folder to target folder. Skip files with duplicated files in target.')
    argparser.add_argument("--from", dest='fromdir', # metavar='Folder-root',
                           type=str, default='.', required=True,
                           help='The directory path of source files. Cannot be relative path if on different drive.')
    argparser.add_argument("--to", dest='targetdir', # metavar='Folder-root',
                           type=str, default='.', required=True,
                           help='The library directory to copy into. Cannot be relative if on different drive.')

    argparser.add_argument("--rec", dest='recursive', 
                           default=False, required=False,
                           action='store_true',
                           help='Scan recursively in source folder. Default is false.')

    argparser.add_argument("--del", dest='delidentical', 
                           default=False, required=False,
                           action='store_true',
                           help='Delete identical files. Default is false.')

    argparser.add_argument("--movezip", dest='movezip', 
                           default=False, required=False,
                           action='store_true',
                           help='Force move zip files. Default is false.')

    argparser.add_argument("--cleanlog", dest='cleanlog', 
                           default=False, required=False,
                           action='store_true',
                           help='Clean existing log file')

    args = argparser.parse_args()

    print(args)

    check_path_validity(args.fromdir)
    check_path_validity(args.targetdir)

    print("WARNING: IF you want to preserve the folder structure from your source, DON'T USE THIS PROGRAM!!")
    answer = input("Do you want to continue? (yes/no)")
    if answer != 'Y' and answer != 'y':
        exit(0)

    move_from_to(args.fromdir, args.targetdir, args.delidentical, args.movezip, args.recursive)