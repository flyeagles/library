import os
import argparse


def tag_file_with_folder_name(folder, is_surfix, change_folder):
    os.chdir(folder)

    fullpath = os.getcwd()
    _,tail = os.path.split(fullpath)
    print('Will add string "{s}" to file names'.format(s=tail))

    files = os.listdir('.')
    cnt = 0
    for item in files:
        if not change_folder and not os.path.isfile(item):
            # we don't change contents of subfoldeers.
            continue

        new_name = tail + '_' + item
        os.rename(item, new_name)
        cnt += 1

    print("Changed {d} file names.".format(d=cnt))

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Scan specified folder and upload file info to database.')
    argparser.add_argument("-d", dest='targetdir', # metavar='Folder-root',
                           type=str, default='.', required=True,
                           help='The directory path of files.')

    argparser.add_argument("--surfix", dest='at_surfix', # metavar='Folder-root',
                            action='store_true',
                            default=False, required=False,
                            help='whether the folder name is added as surfix.')

    argparser.add_argument("--folder", dest='change_folder', # metavar='Folder-root',
                            action='store_true',
                            default=False, required=False,
                            help='whether to change sub-folder as well.')

    argparser.add_argument("--cleanlog", dest='cleanlog', 
                           default=False, required=False,
                           action='store_true',
                           help='Clean existing log file')

    args = argparser.parse_args()

    print(args)
    tag_file_with_folder_name(args.targetdir, args.at_surfix, args.change_folder)

