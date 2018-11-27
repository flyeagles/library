# by yluo, November 2018

import os
import datetime
import time
import pandas as pd

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


import re
import sharevars
import pyperclip
import time

import threading

import auxi


def escape_slash(a_str):
    return a_str.replace('\\', '\\\\')

class WatchClip(threading.Thread):
    def __init__(self, search_string_entry, search_func):
        threading.Thread.__init__(self)
        self.string_entry = search_string_entry
        self.search_func = search_func

    def run(self):
        old_clip = "dummy"
        print("Ready to watch clip change.")
        while sharevars.not_quit:
            clip_text = escape_slash(pyperclip.paste())
            if clip_text != old_clip and clip_text.strip() != '':
                old_clip = clip_text
                self.string_entry.delete(0, tk.END)
                self.string_entry.insert(tk.END, clip_text)
                self.search_func()

            time.sleep(0.3)

 
isascii = lambda s: len(s) == len(s.encode())

syms = r' |\(|\)|\[|\]|\.|_|-|\+|\?|\'|（|）|\:|：|，|、|《|》|·|“|”|？|【|】'
def split_to_words(str_val):
    return re.split(syms, str_val)

def get_two_letter_words(str_val):
    str_list = split_to_words(str_val)
    words = []
    for short_str in str_list:
        if len(short_str) == 0:
            continue

        if isascii(short_str):
            words.append(short_str)
        else:
            for idx in range(len(short_str)-1):
                words.append(short_str[idx:idx+2])
            
            for idx in range(len(short_str)-2):
                words.append(short_str[idx:idx+3])

    return words


def series_and(ser1, ser2):
    return ser1 & ser2

def series_or(ser1, ser2):
    return ser1 | ser2

def df_filter_func(df, tags, series_func):
    result_series = df['title'].str.contains(next(iter(tags)), flags = re.IGNORECASE)
    for tag in tags:
        result_series = series_func(result_series, df['title'].str.contains(tag, flags = re.IGNORECASE))
    return result_series

def df_filter_and_or(df, set_of_set_tags):
    set_iter = iter(set_of_set_tags)
    result_series = df_filter_func(df, next(set_iter), series_or)
    for _ in range(len(set_of_set_tags) - 1):
        # first level is union, so use "series_or"
        # second level is join, so use "sereies_and"
        result_series = series_and(result_series, df_filter_func(df, next(set_iter), series_or))
    
    return result_series

def df_filter_and(df, tags):
    return df_filter_func(df, tags, series_and)

def df_filter_or(df, tags):
    return df_filter_func(df, tags, series_or)

def set_intersection(set1, set2):
    return set1.intersection(set2)

def set_union(set1, set2):
    return set1.union(set2)

def search_books_with_terms_func(tags, set_func, df_filter):
    '''
    First search title in tag_file_dict,
    then use string matching.
    '''
    result_file_set = set()
    initial = True
    for tag in tags:
        file_set = sharevars.tag_file_dict.get(tag, set())
        if initial:
            result_file_set = file_set
            initial = False
        else:
            result_file_set = set_func(result_file_set, file_set) 
            if len(result_file_set) == 0:
                # no match already. Break out of loop now.
                break

    columns = ['title','surfix','size','folder']
    tag_df = pd.DataFrame(list(result_file_set), columns=columns)
    return pd.concat([tag_df[columns],
            sharevars.all_book_tree_view.filter_df(df_filter, tags, columns)],
            ignore_index=True)


def get_tag_mapped_files_or(set_tags):
    set_iter = iter(set_tags)
    result_file_set = sharevars.tag_file_dict.get(next(set_iter), set())
    for _ in range(len(set_tags)-1):
        file_set = sharevars.tag_file_dict.get(next(set_iter), set())
        result_file_set = result_file_set.union(file_set) 

    return result_file_set

def search_books_with_terms_and_or(set_of_set_tags):
    '''
    First search title in tag_file_dict,
    then use string matching.
    '''
    set_set_iter = iter(set_of_set_tags)
    result_file_set = get_tag_mapped_files_or(next(set_set_iter))
    for _ in range(len(set_of_set_tags)-1):
        file_set = get_tag_mapped_files_or(next(set_set_iter))
        result_file_set = result_file_set.intersection(file_set)
        if len(result_file_set) == 0:
            # no match already. Break out of loop now.
            break

    columns = ['title','surfix','size','folder']
    tag_df = pd.DataFrame(list(result_file_set), columns=columns)
    return pd.concat([tag_df[columns],
            sharevars.all_book_tree_view.filter_df(df_filter_and_or, set_of_set_tags, columns)],
            ignore_index=True)

def search_books_with_terms_and(tags):
    return search_books_with_terms_func(tags, set_intersection, df_filter_and)

def change_tile_in_tag_dict(from_title, surfix, size, folder, to_title):
    print('=====================')
    print(sharevars.tag_file_dict)
    # folder = escape_slash(folder)
    size = str(size)
    print('>>>>', (from_title, surfix, size, folder))
    for tag in sharevars.tag_file_dict.keys():
        print(sharevars.tag_file_dict[tag])
        if (from_title, surfix, size, folder) in sharevars.tag_file_dict[tag]:
            sharevars.tag_file_dict[tag].remove((from_title, surfix, size, folder))
            sharevars.tag_file_dict[tag].add((to_title, surfix, size, folder))
            print('Updated tag for ', (to_title, surfix, size, folder))


#===========================================================
# Monitor library folder change, and update tag_file_dict
#===========================================================

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog.events

class LibFileSystemEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self):
        pass

    def deleteitem(self, file_path):
        head, tail = os.path.split(file_path)
        print(tail, 'is deleted.')
        

    def modifyitem(self, src_path, dst_path):
        try:
            size = os.path.getsize(dst_path)
        except FileNotFoundError as err:
            print(err)
            print("Skip missing file: {fn}".format(fn=path))
            return

        _, old_fname = os.path.split(src_path)
        old_title, _ = auxi.get_name_surfix(old_fname)

        folder, new_fname = os.path.split(dst_path)
        new_title, surfix = auxi.get_name_surfix(new_fname)

        sharevars.all_book_tree_view.rename_title(old_title, surfix, size, folder, new_title)
        change_tile_in_tag_dict(old_title, surfix, size, folder, new_title)
        
        print("Title change: ", (old_title, surfix, size, folder, new_title))
        
    def on_moved(self, event):
        ''' 
        deal with event of file moved between folders or just renamed.
        '''
        print("moved " + str(event))
        if event.is_directory:
            return

        self.modifyitem(event.src_path, event.dest_path)

    '''
    def on_created(self, event):
        print("created " + str(event))
        print(event.src_path)
        pass # just ignore
        
    def on_deleted(self, event):
        return
        print("deleted " + str(event))
        print(event.src_path)
        if event.is_directory:
            return
        
        self.deleteitem(event.src_path)

    def on_modified(self, event):
        '' '
        File name change in a folder will trigger Modified_event for the folder itself.
        '' '
        return
        print("modified " + str(event))
        print(event.src_path)

        # we can ignore modification event.
        pass
    '''

class LibraryMonitor:
    def __init__(self, monitor_folders):
        self.monitor_folders = monitor_folders
        self.event_handler = LibFileSystemEventHandler()
        self.observer = Observer()

    def start(self):
        for path in self.monitor_folders:
            print("Observing {fd}".format(fd=path))
            self.observer.schedule(self.event_handler, path, recursive=True)

        self.observer.start()
        #    observer_list.append(observer)

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()



if __name__ == '__main__':
    lib_monitor = LibraryMonitor(['.'])
    lib_monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        lib_monitor.stop()

    lib_monitor.join()
