# by yluo, November 2018

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


import auxi
import library_data
import sharevars

class BookTreeView:

    def __init__(self, tree_view, count_entry, unique_count_entry, page_size):
        self.tree_view = tree_view  # the tree view to show the book list
        self.df = None    # dataframe contains all books
        self.tree_idds = None     # tree IIDs to manipuate each row

        self.count_entry = count_entry   # total item count display
        self.unique_count_entry = unique_count_entry   # total item count display
        self.page_size = page_size

        self.reset_location()
        self._initialize_tree_iids()
        self.recent_df_time = None

    def reset_location(self):
        self.location = self.page_size

    def set_dataframe(self, a_df):
        self.df = a_df
        self.reset_location()

        self.recent_df_time = datetime.datetime.now()

    def get_dataframe(self):
        return self.df

    def get_book_count(self):
        return len(self.df)

    def filter_df(self, df_filter, tags, columns):
        return self.df.loc[lambda df: df_filter(df, tags)][columns]

    def get_selected_row(self):
        focus_iid = self.tree_view.focus()
        book_title = self.tree_view.item(focus_iid, 'text')
        book_record = self.tree_view.item(focus_iid, 'values')
        return book_title, book_record

    def update_view_with_df(self, a_df):
        self.set_dataframe(a_df)
        if a_df is not None:
            self._fill_tree_view_with_page()
            auxi.set_count_in_entry(self.count_entry, len(self.df))
            auxi.set_count_in_entry(self.unique_count_entry, self.df['title'].nunique())

    def focus_on_row(self, focus_idx):
        # focus on specific line
        new_focus_iid = self.tree_iids[focus_idx]
        self.tree_view.focus(new_focus_iid)
        self.tree_view.see(new_focus_iid)
        self.tree_view.selection_set(new_focus_iid)

    def page_down(self):
        self._cmd_page_updown_generic(BookTreeView._line_count_page_down)

    def page_up(self):
        self._cmd_page_updown_generic(BookTreeView._line_count_page_up)

    def page_before(self):
        self._cmd_prev_next_page(BookTreeView._calc_prev_page_loc)

    def page_next(self):
        self._cmd_prev_next_page(BookTreeView._calc_next_page_loc)


    #############################################
    # private methods

    def _initialize_tree_iids(self):
        self.tree_iids = []
        for _ in range(self.page_size):
            iid = self.tree_view.insert('', 'end', 
                    text='', values=['', ''])
            self.tree_iids.append(iid)

    def _location_capped_at_length(self):
        return min(self.location, len(self.df.index))

    def _fill_tree_view_with_page(self):
        if self.df is None:
            return

        df_index = self.df[self.location-self.page_size : self._location_capped_at_length()].index
        for idx, row in enumerate(df_index):
            self.tree_view.item(self.tree_iids[idx],
                text=self.df.loc[row, 'title'],
                values=[self.df.loc[row, 'surfix'],
                        self.df.loc[row, 'size'],
                        self.df.loc[row, 'folder']
                        ])

        for idx in range(len(df_index), self.page_size):
            self.tree_view.item(self.tree_iids[idx],
                text='',
                values=['', ''])

        self.focus_on_row(0)

    def _cmd_prev_next_page(self, func_calc_loc):
        if self.tree_iids is None:
            # not loaded yet. Just return.
            return

        need_fill_page, self.location = func_calc_loc(self.location, self.df, self.page_size)
        if need_fill_page:
            self._fill_tree_view_with_page()

    def _cmd_page_updown_generic(self, new_idx_func):
        focus_iid = self.tree_view.focus()
        focus_idx = self.tree_view.index(focus_iid)
        focus_idx = new_idx_func(focus_idx, self.page_size)
        self.focus_on_row(focus_idx)

    #############################################
    # static functions to calculate index location.

    @staticmethod
    def _line_count_page_down(focus_idx, page_size):
        focus_idx += int(page_size / 2)
        if focus_idx >= page_size:
            focus_idx = page_size - 1
        return focus_idx

    @staticmethod
    def _line_count_page_up(focus_idx, page_size):
        focus_idx -= int(page_size / 2)
        if focus_idx < 0:
            focus_idx = 0
        return focus_idx

    @staticmethod
    def _calc_prev_page_loc(location, a_df, page_size):
        '''
        return: need_fill_page_flag, new location
        '''
        location -= page_size
        if location <= 0:
            location = page_size
            return False, location
        
        return True, location

    @staticmethod
    def _calc_next_page_loc(location, a_df, page_size):
        '''
        return: need_fill_page_flag, new location
        '''
        if location >= len(a_df):
            return False, location
        
        return True, location + page_size



import datetime
import os
import pandas as pd


class AllBookTreeView(BookTreeView):

    def __init__(self, tree_view, count_entry, unique_count_entry, page_size, lib_index_file, lib_dir):
        super().__init__(tree_view, count_entry, unique_count_entry, page_size)
        self.lib_index_file = lib_index_file

        sharevars.global_lib_data = library_data.LibraryData(lib_dir)

        # need load the data from index file.
        a_df = sharevars.global_lib_data.get_library_df()
        self.update_view_with_df(a_df)

    def shutdown(self):
        # need persist dataframe if changed since loaded frmo index.
        sharevars.global_lib_data.save()

    '''
    def rename_title(self, from_title, surfix, size, folder, to_title):
        '' '
            scan book dataframe, replace title field when matched.
            also need update tag_file_dict
        '' '

        # !!!!! this change based on only on filename without surfix. so it will rush ahead of the real change
        # for the rest of files with same name but different surfix, or in different folders. 
        # THIS MUST BE CHANGED IF file name change feature is modified into based on other characters beyond file title.
        # !!!!!!!!!!!!!!!!!!
        match_indexes = self.df[self.df['title']==from_title].index
        for index in match_indexes:
            self.df.at[index, 'title'] = to_title
            #  df.at[df[df[0]==5].index[0],0] = 15
    '''

    @staticmethod
    def merge_book_index_dataframe(lib_index_file, lib_dir, book_df):
        the_list = library_data.LibraryData.rec_read_folder(lib_dir)
        new_part_book_df = pd.DataFrame(the_list)
        new_part_book_df.columns = ['title', 'folder', 'filename', 
                'surfix', 'authors', 'size', 'mod_date' ]
        #new_part_book_df.sort_values(['filename'], inplace=True, ascending=True)

        old_fname_set = set(book_df['filename'])
        new_fname_set = set(new_part_book_df['filename'])
        true_new_fname_set = new_fname_set - old_fname_set
        func_get_true_new = lambda x: x in true_new_fname_set

        # remove existing items in book_df from new part df
        true_new_part_book_df = new_part_book_df.loc[lambda df: df['filename'].apply(func_get_true_new)]

        # now merge new_part_book_df with book_df
        return pd.concat([book_df, true_new_part_book_df], ignore_index=True)


