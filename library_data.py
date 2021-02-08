import datetime
import pickle
import os
import pandas as pd

import auxi


MOVE_TARGET_LIB_DATA_FILE = 'lib_move_target.pkl'
MAX_FILES_FOLDER = 500

class DataForMoveCheck:

    @staticmethod
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

                DataForMoveCheck._add_size_data_to_index(size_index, file_stat.st_size, a_file, root)

        print("generate index file in ", datetime.datetime.now() - start_time)
        print(folder_file_count)

        if len(folder_file_count) == 0: # empty library folder yet
            folder_file_count['0001'] = 0
        target_subfolders = list(folder_file_count.keys())
        target_subfolders.sort(reverse=True)
        
        print("Will start moving file into folder:", target_subfolders[0])

        _, tail = os.path.split(target_subfolders[0])

        '''
        file_stats: map(file name --> (file size, path))
        tail: last folder name
        count: of items in last folder
        size_index: map(size --> [(file name, path)])  # with the same size
        '''
        '''
        Library dataframe structure:
            [(title without extension, path, file name, extension, "", size, file modify time)]
        '''
        return file_stats, int(tail), folder_file_count[target_subfolders[0]], size_index

    @staticmethod
    def _add_size_data_to_index(size_index, size, a_file, root):
        if size in size_index:
            size_index[size].append((a_file, root))
        else:
            size_index[size] = [(a_file, root)]

    @staticmethod
    def rename_file(files_in_lib, old_file_name, new_file_name, size_index, this_size):
        # Need modify file_stats's key, and size_index's value file name.
        if new_file_name in files_in_lib:
            print("Name conflict for " + new_file_name)
            print("Cannot rename.")
            return False

        files_in_lib[new_file_name] = files_in_lib[old_file_name]
        del files_in_lib[old_file_name]

        # modify index
        size_index[this_size][0] = (new_file_name, size_index[this_size][0][1])

        return True

    @staticmethod
    def get_folder_id_count(start_fid, file_count):
        if file_count < MAX_FILES_FOLDER:
            return start_fid, file_count + 1
        else:
            return start_fid + 1, 1


class LibraryData:
    
    lib_index_file = 'lib_index.pkl'

    def __init__(self, to_folder):
        self.to_folder = to_folder
        self.file_stats, self.fid, self.fcount, self.size_index = \
                LibraryData._get_target_folder_files(self.to_folder)
        self.library_df = LibraryData.get_gen_book_index_dataframe(LibraryData.lib_index_file, self.to_folder)
        self.initial_time = datetime.datetime.now()
        self.last_mod_time = self.initial_time

    def get_target_folder_files(self):
        return self.file_stats, self.fid, self.fcount, self.size_index

    def get_library_df(self):
        return self.library_df

    def get_folder_id_count(self):
        new_fid, new_count = DataForMoveCheck.get_folder_id_count(self.fid, self.fcount)
        self.fid = new_fid
        self.fcount = new_count
        return new_fid, new_count

    def save(self):
        if self.initial_time == self.last_mod_time:
            print("no change in library data.")
            return

        LibraryData._save_target_folder_data((self.file_stats, self.fid, self.fcount, self.size_index))

        print('Save changed books dataframe.')
        self.library_df.to_pickle(LibraryData.lib_index_file)

    @staticmethod
    def _add_file_to_df(book_df, a_file, new_file_path, this_size, file_mod_time):
        # [(title without extension, path, file name, extension, "", size, file modify time)]
        name, surfix = auxi.get_name_surfix(a_file)
        the_list = [(name, new_file_path, a_file, surfix, "", this_size, file_mod_time)]
        new_part_book_df = pd.DataFrame(the_list)
        new_part_book_df.columns = ['title', 'folder', 'filename', 
                'surfix', 'authors', 'size', 'mod_date' ]

        # now merge new_part_book_df with book_df
        return pd.concat([book_df, new_part_book_df], ignore_index=True)


    def add_file_to_lib(self, to_folder, folder_name, this_size, a_file, file_mod_time):
        new_file_path = str(os.path.join(to_folder, folder_name))
        self.file_stats[a_file] = (this_size, new_file_path)

        DataForMoveCheck._add_size_data_to_index(self.size_index, this_size, a_file, new_file_path)

        # add item to data frame
        self.library_df = LibraryData._add_file_to_df(self.library_df, a_file, new_file_path, this_size, file_mod_time)

        self.last_mod_time = datetime.datetime.now()


    @staticmethod
    def _save_target_folder_data(target_folder_data):
        with open(MOVE_TARGET_LIB_DATA_FILE, 'wb') as WFILE:
            pickle.dump(target_folder_data, WFILE)

    @staticmethod
    def _get_target_folder_files(to_folder):
        if os.path.exists(MOVE_TARGET_LIB_DATA_FILE):
            with open(MOVE_TARGET_LIB_DATA_FILE, 'rb') as RFILE:
                target_folder_data = pickle.load(RFILE)
        else:
            target_folder_data = DataForMoveCheck.get_target_folder_files_from_system(to_folder)
            LibraryData._save_target_folder_data(target_folder_data)

        return target_folder_data

    def rename_file_for_move_entry(self, old_file_name, new_file_name, this_size):
        if self.rename_file_for_move_only(old_file_name, new_file_name, this_size):
            bothpath = self.file_stats[new_file_name][1]
            old_full_name = os.path.join(bothpath, old_file_name)
            new_full_name = os.path.join(bothpath, new_file_name)
            self.rename_file_in_df_only(old_full_name, new_full_name)
            return True

        return False


    def rename_file_for_move_only(self, old_file_name, new_file_name, this_size):
        if DataForMoveCheck.rename_file(self.file_stats, old_file_name, new_file_name, self.size_index, this_size):
            # need change dataframe too
            self.last_mod_time = datetime.datetime.now()
            return True

        return False

    def rename_file_in_df_entry(self, old_full_name, new_full_name):
        _, old_file_name = os.path.split(old_full_name)
        _, new_file_name = os.path.split(new_full_name)
        this_size = self.file_stats[old_file_name][0]
        if not self.rename_file_for_move_only(old_file_name, new_file_name, this_size):
            print("Cannot rename title ")
            return False

        self.rename_file_in_df_only(old_full_name, new_full_name)
        return True


    def rename_file_in_df_only(self, old_full_name, new_full_name):
        '''
            scan book dataframe, replace title field when matched.
            also need update tag_file_dict
        '''

        # !!!!! this change based on only on filename without surfix. so it will rush ahead of the real change
        # for the rest of files with same name but different surfix, or in different folders. 
        # THIS MUST BE CHANGED IF file name change feature is modified into based on other characters beyond file title.
        # !!!!!!!!!!!!!!!!!!
        _, old_name = os.path.split(old_full_name)
        _, new_name = os.path.split(new_full_name)
        old_title, _ = auxi.get_name_surfix(old_name)
        new_title, _ = auxi.get_name_surfix(new_name)

        match_indexes = self.library_df[self.library_df['title']==old_title].index
        for index in match_indexes:
            self.library_df.at[index, 'title'] = new_title
            self.library_df.at[index, 'filename'] = new_title + '.' + self.library_df.at[index, 'surfix']
            #  df.at[df[df[0]==5].index[0],0] = 15

        self.recent_df_time = datetime.datetime.now()

    @staticmethod
    def get_gen_book_index_dataframe(lib_index_file, lib_dir):
        if os.path.exists(lib_index_file):
            start = datetime.datetime.now()
            book_df = pd.read_pickle(lib_index_file)
            print('load index time:', datetime.datetime.now() - start)
            print('Index contains books:', len(book_df.index))
        else:
            the_list = LibraryData.rec_read_folder(lib_dir)
            book_df = pd.DataFrame(the_list)
            book_df.to_pickle(lib_index_file)
  
        book_df.columns = ['title', 'folder', 'filename', 
                    'surfix', 'authors', 'size', 'mod_date' ]
        book_df.sort_values(['filename'], inplace=True, ascending=True)

        '''
        # print(book_df['folder'])
        # print(book_df['folder'] == '.\\library\\0110')
        in_folder_df = book_df[book_df['folder'] == '.\\library\\0110']
        file_list = in_folder_df['filename'].to_list()
        for idx, file in enumerate(file_list):
            print(file)
        '''
        
        return book_df


    @staticmethod
    def rec_read_folder(folder):
        all_file_info = []
        start = datetime.datetime.now()
        
        print("Walk in folder", folder)
        res = os.walk(folder)
        for root, dirs, files in res:
            for filename in files:
                fstat = os.stat(os.path.join(root, filename))
                name, surfix = auxi.get_name_surfix(filename)
                all_file_info.append((name, root, filename, surfix, "", fstat.st_size, auxi.get_date(fstat.st_mtime)))
        dur = datetime.datetime.now() - start
        print("Folder scan time:", dur)

        '''
        [(title without extension, path, file name, extension, "", size, file modify time)]
        '''
        return all_file_info
