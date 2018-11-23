#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.18
#  in conjunction with Tcl version 8.6
#    Nov 13, 2018 10:59:20 PM CST  platform: Windows NT
#    Nov 13, 2018 11:46:36 PM CST  platform: Windows NT
#    Nov 13, 2018 11:54:32 PM CST  platform: Windows NT
#    Nov 14, 2018 08:22:55 PM CST  platform: Windows NT
#    Nov 14, 2018 08:46:43 PM CST  platform: Windows NT
#    Nov 14, 2018 08:59:41 PM CST  platform: Windows NT
#    Nov 14, 2018 09:02:24 PM CST  platform: Windows NT
#    Nov 14, 2018 10:21:53 PM CST  platform: Windows NT
#    Nov 15, 2018 08:31:15 PM CST  platform: Windows NT
#    Nov 15, 2018 08:44:45 PM CST  platform: Windows NT
#    Nov 15, 2018 08:57:49 PM CST  platform: Windows NT
#    Nov 15, 2018 09:53:05 PM CST  platform: Windows NT
#    Nov 17, 2018 10:08:07 PM CST  platform: Windows NT
#    Nov 17, 2018 10:47:10 PM CST  platform: Windows NT
#    Nov 17, 2018 10:50:54 PM CST  platform: Windows NT
#    Nov 18, 2018 10:27:36 PM CST  platform: Windows NT
#    Nov 18, 2018 10:30:08 PM CST  platform: Windows NT
#    Nov 18, 2018 11:17:39 PM CST  platform: Windows NT
#    Nov 19, 2018 02:55:57 PM CST  platform: Windows NT
#    Nov 19, 2018 05:23:57 PM CST  platform: Windows NT
#    Nov 19, 2018 05:59:57 PM CST  platform: Windows NT
#    Nov 19, 2018 10:34:04 PM CST  platform: Windows NT
#    Nov 19, 2018 11:34:22 PM CST  platform: Windows NT
#    Nov 20, 2018 06:24:40 PM CST  platform: Windows NT
#    Nov 20, 2018 08:57:48 PM CST  platform: Windows NT
#    Nov 20, 2018 11:21:31 PM CST  platform: Windows NT
#    Nov 21, 2018 02:16:44 PM CST  platform: Windows NT
#    Nov 21, 2018 04:38:51 PM CST  platform: Windows NT
#    Nov 21, 2018 05:12:11 PM CST  platform: Windows NT
#    Nov 21, 2018 10:03:40 PM CST  platform: Windows NT
#    Nov 22, 2018 02:00:52 PM CST  platform: Windows NT
#    Nov 22, 2018 03:49:54 PM CST  platform: Windows NT

import sys
import pandas as pd
import re
import os
import subprocess
import pickle

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    py3 = True
    import tkinter.ttk as ttk

# own code

import sharevars
import features
import book_tree_view
import category_tree_view

def search_from_text_entry(p1):
    print('library_support.search_from_text_entry')
    search_file_name()
    sys.stdout.flush()

def search_tags():
    print('library_support.search_tags')
    show_search_result_from_listbox()
    sys.stdout.flush()

def add_cat_relation():
    print('library_support.add_cat_relation')
    global check_cat_contains
    print(check_cat_contains.get())

    is_contain_rel = (check_cat_contains.get() == '1')
    sub_cat = w.sub_cat_entry.get()
    obj_cat = w.obj_cat_entry.get()

    sharevars.category_tree_view.add_cat_relation(sub_cat, obj_cat, is_contain_rel)

    sys.stdout.flush()

def set_tag_as_obj():
    print('library_support.set_tag_as_obj')
    w.obj_cat_entry.delete(0, tk.END)
    w.obj_cat_entry.insert(tk.END, sharevars.category_tree_view.get_selected_cat())

    sys.stdout.flush()

def set_tag_as_sub():
    print('library_support.set_tag_as_sub')
    w.sub_cat_entry.delete(0, tk.END)
    w.sub_cat_entry.insert(tk.END, sharevars.category_tree_view.get_selected_cat())
    sys.stdout.flush()

def swap_tags():
    print('library_support.swap_tags')
    temp_tag = w.obj_cat_entry.get()
    w.obj_cat_entry.delete(0, tk.END)
    w.obj_cat_entry.insert(tk.END, w.sub_cat_entry.get())

    w.sub_cat_entry.delete(0, tk.END)
    w.sub_cat_entry.insert(tk.END, temp_tag)

    sys.stdout.flush()

def record_title(p1):
    print('library_support.record_title')
    print('p1 = {0}'.format(p1))
    sharevars.title_in_focus = sharevars.all_book_tree_view.get_selected_row()[0]
    sys.stdout.flush()

def add_tag_e(p1):
    print('library_support.add_tag_e')
    print('p1 = {0}'.format(p1))
    add_tag()
    sys.stdout.flush()

import filename_change

def remove_file_tag(p1):
    print('library_support.remove_file_tag')
    print('p1 = {0}'.format(p1))

    focus_tuple = w.file_tags_scrolledlistbox.curselection()
    tag = w.file_tags_scrolledlistbox.get(focus_tuple[0])
    print(tag)
    
    title, record = sharevars.all_book_tree_view.get_selected_row()
    new_tag_tuple = flaten_tuple(title, record)
    sharevars.tag_file_dict[tag].remove(new_tag_tuple)

    w.file_tags_scrolledlistbox.delete(focus_tuple[0])

    sys.stdout.flush()

def flaten_tuple(title, record):
    return (title, record[0], record[1], record[2])

def add_tag():
    print('library_support.add_tag')
    tag_text = w.manual_tag_entry.get()
    print(tag_text)
    if len(tag_text) == 0:
        return

    # get current selected full file name of book tree view
    title, record = sharevars.all_book_tree_view.get_selected_row()
    new_tag_tuple = flaten_tuple(title, record)

    file_set = sharevars.tag_file_dict.get(tag_text, set())
    if new_tag_tuple not in file_set:
        file_set.add(new_tag_tuple)
        sharevars.tag_file_dict[tag_text] = file_set

    sharevars.category_tree_view.add_category(tag_text)

    print(sharevars.tag_file_dict)

    sys.stdout.flush()

def pick_searched_item(p1):
    print('library_support.pick_searched_item')
    print('p1 = {0}'.format(p1))
    show_searched_file_detail()
    sharevars.title_in_focus = sharevars.search_book_tree_view.get_selected_row()[0]
    sys.stdout.flush()

def search_books_with_descendents():
    tag_descend_list_set = []
    for chosen_tag in sharevars.chosen_tags_set:
        # we can add the descendents of selected tag for union--search as well.
        desc_set = sharevars.category_tree_view.get_all_descendents_rec(chosen_tag)
        desc_set.add(chosen_tag)
        tag_descend_list_set.append(desc_set)

    tag_df = features.search_books_with_terms_and_or(tag_descend_list_set)

    sharevars.search_book_tree_view.update_view_with_df(tag_df)

def show_search_result_from_listbox():
    if check_explicit_tag.get() == '1':
        # should just search the terms, without considerig their children.
        search_books_and(sharevars.chosen_tags_set)
    else:
        search_books_with_descendents()

def search_books_and(str_list):
    tag_df = features.search_books_with_terms_and(str_list)
    sharevars.search_book_tree_view.update_view_with_df(tag_df)

def search_file_name():
    print('library_support.search_file_name')

    search_string = w.search_string_entry.get().strip()
    if search_string == '':
        return

    str_list = features.split_to_words(search_string)
    search_books_and(str_list)

    sys.stdout.flush()

def rescan_folder():
    '''
    Called from "Rescan library" button.
    '''
    print('library_support.rescan_folder')
    new_lib_df = book_tree_view.AllBookTreeView.merge_book_index_dataframe(
            sharevars.lib_index_file,
            sharevars.target_folder,
            sharevars.all_book_tree_view.get_dataframe()
            )
    print(len(new_lib_df.index))
    sharevars.all_book_tree_view.update_view_with_df(new_lib_df)
    sys.stdout.flush()


def open_filename_change(p1):
    print('library_support.open_filename_change')
    print('p1 = {0}'.format(p1))
    change_file_name()
    sys.stdout.flush()

def change_file_name():
    print('library_support.change_file_name')
    
    # !!!!!!  must use create_TopLevel1() to launch child window. Otherwise its event system will malfunction.
    filename_change.create_Toplevel1(root)

    sys.stdout.flush()

def remove_tag_4_search(p1):
    print('library_support.remove_tag_4_search')
    print('p1 = {0}'.format(p1))
    focus_tuple = w.chosen_tag_scrolledlistbox.curselection()
    cat_name = w.chosen_tag_scrolledlistbox.get(focus_tuple[0])
    print(cat_name)

    if (cat_name not in sharevars.chosen_tags_set) or len(sharevars.chosen_tags_set) == 1:
        # we don't allow remove tag at last item
        return

    w.chosen_tag_scrolledlistbox.delete(focus_tuple[0])
    sharevars.chosen_tags_set.remove(cat_name)

    show_search_result_from_listbox()

    sys.stdout.flush()

def search_book_view_control(p1):
    print('p1 = {0}'.format(p1))

    if p1.keycode == 13: # ENTER
        book_title, book_record = sharevars.search_book_tree_view.get_selected_row()
        open_file_in_explorer(book_record, book_title)

    if p1.keycode == 39: # right arrow. next page
        sharevars.search_book_tree_view.page_next()
    elif p1.keycode == 37: # left arrow. previous page
        sharevars.search_book_tree_view.page_before()
    elif p1.keycode == 34: # page down.
        sharevars.search_book_tree_view.page_down()
    elif p1.keycode == 33: # page up.
        sharevars.search_book_tree_view.page_up()

    sharevars.title_in_focus = sharevars.search_book_tree_view.get_selected_row()[0]

    show_searched_file_detail()

    sys.stdout.flush()

def show_searched_file_detail():
    # show current selected file's details.
    w.file_detail_entry.delete(0, tk.END)
    values = w.search_books_scrolledtreeview.item(
            w.search_books_scrolledtreeview.focus(), 'values')
    if values[1] == '':
        return

    print(values)

    w.file_detail_entry.insert(tk.END, 
        '{}, {:,d} bytes'.format(values[0], int(values[1])))

def search_book_in_category(p1):
    print('library_support.search_book_in_category')
    print('p1 = {0}'.format(p1))
    cat_name = sharevars.category_tree_view.get_selected_cat()
    print(cat_name)

    if cat_name in sharevars.chosen_tags_set:
        return

    w.chosen_tag_scrolledlistbox.insert(tk.END, cat_name)
    sharevars.chosen_tags_set.add(cat_name)

    show_search_result_from_listbox()

    sys.stdout.flush()

def add_tag_2_cat(p1):
    print('library_support.add_tag_2_cat')
    print('p1 = {0}'.format(p1))
    sys.stdout.flush()

    selected_idx = w.tag_candidate_scrolledlistbox.curselection()[0]
    item = w.tag_candidate_scrolledlistbox.get(selected_idx)
    print(item)
    sharevars.category_tree_view.add_category(item)

def open_file_in_explorer(book_record, book_title):
    full_file_path = os.path.join(os.getcwd(), book_record[2],
                            book_title +'.'+book_record[0])
    #full_file_path = full_file_path.replace('(', '^(')
    print('"'+full_file_path+'"')
    #os.system('"'+full_file_path+'"')
    subprocess.Popen(r'explorer /select,"{p}"'.format(p=full_file_path))

def fill_tag_candidates(book_title):
    sharevars.tag_candidates = features.get_two_letter_words(book_title)
    w.tag_candidate_scrolledlistbox.delete(0, tk.END)
    for term in sharevars.tag_candidates:
        w.tag_candidate_scrolledlistbox.insert(tk.END, term)

def fill_existing_tags(book_title, book_record):
    file_tags = []
    book_tuple = flaten_tuple(book_title, book_record)
    for tag in sharevars.tag_file_dict.keys():
        if book_tuple in sharevars.tag_file_dict[tag]:
            file_tags.append(tag)
    
    w.file_tags_scrolledlistbox.delete(0, tk.END)
    for term in file_tags:
        w.file_tags_scrolledlistbox.insert(tk.END, term)

def all_book_view_control(p1):
    if p1.keycode == 13: # ENTER
        book_title, book_record = sharevars.all_book_tree_view.get_selected_row()
        print(book_title)

        fill_tag_candidates(book_title)
        fill_existing_tags(book_title, book_record)

        w.filename_entry.delete(0, tk.END)
        w.filename_entry.insert(tk.END, book_title)

        open_file_in_explorer(book_record, book_title)

    elif p1.keycode == 39: # right arrow. next page
        sharevars.all_book_tree_view.page_next()
    elif p1.keycode == 37: # left arrow. previous page
        sharevars.all_book_tree_view.page_before()
    elif p1.keycode == 34: # page down.
        sharevars.all_book_tree_view.page_down()
    elif p1.keycode == 33: # page up.
        sharevars.all_book_tree_view.page_up()

    sharevars.title_in_focus = sharevars.all_book_tree_view.get_selected_row()[0]

    sys.stdout.flush()

def cmd_save_category():
    sharevars.category_tree_view.shutdown()

def save_tag_file_dict():
    with open(sharevars.TAG_FILE_NAME, 'wb') as AFILE:
        pickle.dump(sharevars.tag_file_dict, AFILE)

def quit_app(p1):
    print('library_support.quit_app')
    print('p1 = {0}'.format(p1))

    sys.stdout.flush()
    destroy_window()

def set_Tk_var():
    global var_book_list
    var_book_list = tk.StringVar()
    global check_cat_contains
    check_cat_contains = tk.StringVar()
    global check_explicit_tag
    check_explicit_tag = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

    print('=====00000000')

    if sharevars.all_book_tree_view is None:
        sharevars.all_book_tree_view = book_tree_view.AllBookTreeView(
                    w.books_scrolledtreeview,
                    w.all_book_count_entry,
                    sharevars.page_size,
                    sharevars.lib_index_file,
                    sharevars.target_folder
                    )

    if sharevars.search_book_tree_view is None:
        sharevars.search_book_tree_view = book_tree_view.BookTreeView(
                    w.search_books_scrolledtreeview,
                    w.found_book_count_entry,
                    sharevars.page_size)

    if sharevars.category_tree_view is None:
        sharevars.category_tree_view = category_tree_view.CategoryTreeView(
                w.cat_scrolledtreeview,
                sharevars.category_fname,
                sharevars.category_rel_fname,
                sharevars.category_con_fname
                )

    w.check_contain_checkbutton.select()
    w.check_explicit_tag_checkbutton.deselect()

    if os.path.exists(sharevars.TAG_FILE_NAME):
        with open(sharevars.TAG_FILE_NAME, 'rb') as AFILE:
            sharevars.tag_file_dict = pickle.load(AFILE)

    sharevars.clip_job = features.WatchClip(w.search_string_entry,
                search_file_name)
    sharevars.clip_job.start()

    sharevars.lib_monitor = features.LibraryMonitor(['.'])
    sharevars.lib_monitor.start()

def destroy_window():
    # Function which closes the window.
    print("Save category data to disk.")
    save_tag_file_dict()

    sharevars.category_tree_view.shutdown()
    sharevars.all_book_tree_view.shutdown()

    sharevars.not_quit = False
    sharevars.clip_job.join()

    sharevars.lib_monitor.stop()
    sharevars.lib_monitor.join()

    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import library.py
    library.py.vp_start_gui()

