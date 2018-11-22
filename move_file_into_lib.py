import argparse
import os

MAX_FILES_FOLDER = 500

def get_target_folder_files(to_folder):
    all_files = os.walk(to_folder)
    file_stats = {}
    folder_file_count = {}
    for root, dirs, files in all_files:
        for a_file in files:
            new_cnt = folder_file_count.get(root, 0) + 1
            folder_file_count[root] = new_cnt
            file_stat = os.stat(os.path.join(root, a_file))
            file_stats[a_file] = (file_stat.st_size, root)
    
    print(file_stats)
    print(folder_file_count)

    if len(folder_file_count) == 0: # empty library folder yet
        folder_file_count['0001'] = 0
    target_subfolders = list(folder_file_count.keys())
    target_subfolders.sort(reverse=True)
    print(target_subfolders[0])
    head, tail = os.path.split(target_subfolders[0])

    return file_stats, int(tail), folder_file_count[target_subfolders[0]]

def handle_duplicated_files(files_in_lib, a_file, root, identical_files):
    if a_file in files_in_lib:
        file_stat = os.stat(os.path.join(root, a_file))
        if file_stat.st_size == files_in_lib[a_file][0]:
            print("---- Identical file {fn} at {fd}".format(fn=a_file,
                    fd=root))
            identical_files.append(os.path.join(root, a_file))
        else:
            print("Duplicated file {fn} at {fd}".format(fn=a_file,
                    fd=root))
        
        return True
    return False

def get_folder_id_count(start_fid, file_count):
    if file_count < MAX_FILES_FOLDER:
        return start_fid, file_count + 1
    else:
        return start_fid + 1, 1

def move_from_to(from_folder, to_folder, delidentical):

    files_in_lib, start_fid, file_count = get_target_folder_files(to_folder)
    folder_name = '{:04d}'.format(start_fid)

    file_move = []
    all_files = os.walk(from_folder)
    identical_files = []
    for root, dirs, files in all_files:
        for a_file in files:
            #print(root, a_file)
            duplicated = handle_duplicated_files(files_in_lib, a_file, root, identical_files)
            if duplicated:
                continue
            
            # need move.
            start_fid, file_count = get_folder_id_count(start_fid, file_count)
            folder_name = '{:04d}'.format(start_fid)
            new_file_path = os.path.join(to_folder, folder_name, a_file)
            if os.path.exists(new_file_path):
                print("====Found targt file existing! {f}".format(f=new_file_path))
            else:
                os.renames(os.path.join(root, a_file), new_file_path)

    print('Folder', folder_name, 'has', file_count, 'files.')

    if delidentical and len(identical_files) > 0:
        print("========Deleting following identical files!")
        print(identical_files)
        for id_file in identical_files:
            os.unlink(id_file)
           

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Move files from source folder to target folder. Skip files with duplicated files in target.')
    argparser.add_argument("--from", dest='fromdir', # metavar='Folder-root',
                           type=str, default='.', required=True,
                           help='The directory path of source files.')
    argparser.add_argument("--to", dest='targetdir', # metavar='Folder-root',
                           type=str, default='.', required=True,
                           help='The library directory to copy into.')

    argparser.add_argument("--norec", dest='recursive', 
                           default=False, required=False,
                           action='store_true',
                           help='Don\'t scan recursively in source folder. Default is false.')

    argparser.add_argument("--del", dest='delidentical', 
                           default=False, required=False,
                           action='store_true',
                           help='Delete identical files. Default is false.')

    argparser.add_argument("--cleanlog", dest='cleanlog', 
                           default=False, required=False,
                           action='store_true',
                           help='Clean existing log file')

    args = argparser.parse_args()

    print(args)

    move_from_to(args.fromdir, args.targetdir, args.delidentical)