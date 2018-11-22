#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.18
#  in conjunction with Tcl version 8.6
#    Nov 21, 2018 10:10:57 PM CST  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import library_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    library_support.set_Tk_var()
    top = Toplevel1 (root)
    library_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    library_support.set_Tk_var()
    top = Toplevel1 (w)
    library_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {Courier New} -size 10 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1762x983+384+254")
        top.title("Multi-Category Library")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.bind('<Key-Alt_L>x',lambda e:library_support.quit_app(e))
        top.bind('<Key-Control_L>c',lambda e:library_support.open_filename_change(e))

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.715, rely=0.041, height=26, width=46)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Books''')

        self.style.configure('Treeview.Heading',  font="TkDefaultFont")
        self.cat_scrolledtreeview = ScrolledTreeView(top)
        self.cat_scrolledtreeview.place(relx=0.028, rely=0.092, relheight=0.79
                , relwidth=0.182)
        self.cat_scrolledtreeview.heading("#0",anchor="center")
        self.cat_scrolledtreeview.column("#0",width="297")
        self.cat_scrolledtreeview.column("#0",minwidth="20")
        self.cat_scrolledtreeview.column("#0",stretch="1")
        self.cat_scrolledtreeview.column("#0",anchor="w")
        self.cat_scrolledtreeview.bind('<Key-Return>',lambda e:library_support.search_book_in_category(e))

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.023, rely=0.031, height=26, width=77)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Categories''')

        self.tag_candidate_scrolledlistbox = ScrolledListBox(top)
        self.tag_candidate_scrolledlistbox.place(relx=0.63, rely=0.371
                , relheight=0.516, relwidth=0.071)
        self.tag_candidate_scrolledlistbox.configure(background="white")
        self.tag_candidate_scrolledlistbox.configure(disabledforeground="#a3a3a3")
        self.tag_candidate_scrolledlistbox.configure(font="TkFixedFont")
        self.tag_candidate_scrolledlistbox.configure(foreground="black")
        self.tag_candidate_scrolledlistbox.configure(highlightbackground="#d9d9d9")
        self.tag_candidate_scrolledlistbox.configure(highlightcolor="#d9d9d9")
        self.tag_candidate_scrolledlistbox.configure(selectbackground="#c4c4c4")
        self.tag_candidate_scrolledlistbox.configure(selectforeground="black")
        self.tag_candidate_scrolledlistbox.configure(width=10)
        self.tag_candidate_scrolledlistbox.bind('<Key-Return>',lambda e:library_support.add_tag_2_cat(e))

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.63, rely=0.092, height=26, width=109)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Tag Candidates''')

        self.books_scrolledtreeview = ScrolledTreeView(top)
        self.books_scrolledtreeview.place(relx=0.715, rely=0.122, relheight=0.851
                , relwidth=0.267)
        self.books_scrolledtreeview.configure(columns="surfix, size")
        self.books_scrolledtreeview.heading("#0",anchor="center")
        self.books_scrolledtreeview.column("#0",width="447")
        self.books_scrolledtreeview.column("#0",minwidth="20")
        self.books_scrolledtreeview.column("#0",stretch="1")
        self.books_scrolledtreeview.column("#0",anchor="w")
        self.books_scrolledtreeview.heading("surfix,",anchor="center")
        self.books_scrolledtreeview.column("surfix,",width="200")
        self.books_scrolledtreeview.column("surfix,",minwidth="20")
        self.books_scrolledtreeview.column("surfix,",stretch="1")
        self.books_scrolledtreeview.column("surfix,",anchor="w")
        self.books_scrolledtreeview.heading("size",anchor="center")
        self.books_scrolledtreeview.column("size",width="200")
        self.books_scrolledtreeview.column("size",minwidth="20")
        self.books_scrolledtreeview.column("size",stretch="1")
        self.books_scrolledtreeview.column("size",anchor="w")
        self.books_scrolledtreeview.bind('<ButtonRelease-1>',lambda e:library_support.record_title(e))
        self.books_scrolledtreeview.bind('<KeyRelease>',lambda e:library_support.all_book_view_control(e))

        self.Button4 = tk.Button(top)
        self.Button4.place(relx=0.094, rely=0.02, height=33, width=107)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(command=library_support.cmd_save_category)
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Save Category''')

        self.search_books_scrolledtreeview = ScrolledTreeView(top)
        self.search_books_scrolledtreeview.place(relx=0.323, rely=0.122
                , relheight=0.851, relwidth=0.284)
        self.search_books_scrolledtreeview.configure(columns="surfix, size")
        self.search_books_scrolledtreeview.heading("#0",anchor="center")
        self.search_books_scrolledtreeview.column("#0",width="477")
        self.search_books_scrolledtreeview.column("#0",minwidth="20")
        self.search_books_scrolledtreeview.column("#0",stretch="1")
        self.search_books_scrolledtreeview.column("#0",anchor="w")
        self.search_books_scrolledtreeview.heading("surfix,",anchor="center")
        self.search_books_scrolledtreeview.column("surfix,",width="200")
        self.search_books_scrolledtreeview.column("surfix,",minwidth="20")
        self.search_books_scrolledtreeview.column("surfix,",stretch="1")
        self.search_books_scrolledtreeview.column("surfix,",anchor="w")
        self.search_books_scrolledtreeview.heading("size",anchor="center")
        self.search_books_scrolledtreeview.column("size",width="200")
        self.search_books_scrolledtreeview.column("size",minwidth="20")
        self.search_books_scrolledtreeview.column("size",stretch="1")
        self.search_books_scrolledtreeview.column("size",anchor="w")
        self.search_books_scrolledtreeview.bind('<ButtonRelease-1>',lambda e:library_support.pick_searched_item(e))
        self.search_books_scrolledtreeview.bind('<KeyRelease>',lambda e:library_support.search_book_view_control(e))

        self.Label1_3 = tk.Label(top)
        self.Label1_3.place(relx=0.315, rely=0.081, height=26, width=206)
        self.Label1_3.configure(activebackground="#f9f9f9")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#d9d9d9")
        self.Label1_3.configure(disabledforeground="#a3a3a3")
        self.Label1_3.configure(foreground="#000000")
        self.Label1_3.configure(highlightbackground="#d9d9d9")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(text='''Found Books in category''')

        self.Label3_3 = tk.Label(top)
        self.Label3_3.place(relx=0.241, rely=0.056, height=26, width=109)
        self.Label3_3.configure(activebackground="#f9f9f9")
        self.Label3_3.configure(activeforeground="black")
        self.Label3_3.configure(background="#d9d9d9")
        self.Label3_3.configure(disabledforeground="#a3a3a3")
        self.Label3_3.configure(foreground="#000000")
        self.Label3_3.configure(highlightbackground="#d9d9d9")
        self.Label3_3.configure(highlightcolor="black")
        self.Label3_3.configure(text='''Chosen Tags''')

        self.chosen_tag_scrolledlistbox = ScrolledListBox(top)
        self.chosen_tag_scrolledlistbox.place(relx=0.238, rely=0.102
                , relheight=0.546, relwidth=0.071)
        self.chosen_tag_scrolledlistbox.configure(background="white")
        self.chosen_tag_scrolledlistbox.configure(disabledforeground="#a3a3a3")
        self.chosen_tag_scrolledlistbox.configure(font="TkFixedFont")
        self.chosen_tag_scrolledlistbox.configure(foreground="black")
        self.chosen_tag_scrolledlistbox.configure(highlightbackground="#d9d9d9")
        self.chosen_tag_scrolledlistbox.configure(highlightcolor="#d9d9d9")
        self.chosen_tag_scrolledlistbox.configure(selectbackground="#c4c4c4")
        self.chosen_tag_scrolledlistbox.configure(selectforeground="black")
        self.chosen_tag_scrolledlistbox.configure(width=10)
        self.chosen_tag_scrolledlistbox.bind('<Key-Return>',lambda e:library_support.remove_tag_4_search(e))

        self.filename_entry = tk.Entry(top)
        self.filename_entry.place(relx=0.721, rely=0.081, height=24
                , relwidth=0.241)
        self.filename_entry.configure(background="white")
        self.filename_entry.configure(disabledforeground="#a3a3a3")
        self.filename_entry.configure(font="TkFixedFont")
        self.filename_entry.configure(foreground="#000000")
        self.filename_entry.configure(highlightbackground="#d9d9d9")
        self.filename_entry.configure(highlightcolor="black")
        self.filename_entry.configure(insertbackground="black")
        self.filename_entry.configure(selectbackground="#c4c4c4")
        self.filename_entry.configure(selectforeground="black")

        self.Button_remove_space = tk.Button(top)
        self.Button_remove_space.place(relx=0.624, rely=0.916, height=33
                , width=128)
        self.Button_remove_space.configure(activebackground="#d9d9d9")
        self.Button_remove_space.configure(activeforeground="#000000")
        self.Button_remove_space.configure(background="#d9d9d9")
        self.Button_remove_space.configure(command=library_support.change_file_name)
        self.Button_remove_space.configure(disabledforeground="#a3a3a3")
        self.Button_remove_space.configure(foreground="#000000")
        self.Button_remove_space.configure(highlightbackground="#d9d9d9")
        self.Button_remove_space.configure(highlightcolor="black")
        self.Button_remove_space.configure(pady="0")
        self.Button_remove_space.configure(text='''Change file name''')

        self.Button3 = tk.Button(top)
        self.Button3.place(relx=0.238, rely=0.02, height=33, width=102)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=library_support.rescan_folder)
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Rescan folder''')

        self.all_book_count_entry = tk.Entry(top)
        self.all_book_count_entry.place(relx=0.766, rely=0.041, height=24
                , relwidth=0.116)
        self.all_book_count_entry.configure(background="white")
        self.all_book_count_entry.configure(disabledforeground="#a3a3a3")
        self.all_book_count_entry.configure(font="TkFixedFont")
        self.all_book_count_entry.configure(foreground="#000000")
        self.all_book_count_entry.configure(highlightbackground="#d9d9d9")
        self.all_book_count_entry.configure(highlightcolor="black")
        self.all_book_count_entry.configure(insertbackground="black")
        self.all_book_count_entry.configure(selectbackground="#c4c4c4")
        self.all_book_count_entry.configure(selectforeground="black")

        self.found_book_count_entry = tk.Entry(top)
        self.found_book_count_entry.place(relx=0.437, rely=0.081, height=24
                , relwidth=0.116)
        self.found_book_count_entry.configure(background="white")
        self.found_book_count_entry.configure(disabledforeground="#a3a3a3")
        self.found_book_count_entry.configure(font="TkFixedFont")
        self.found_book_count_entry.configure(foreground="#000000")
        self.found_book_count_entry.configure(highlightbackground="#d9d9d9")
        self.found_book_count_entry.configure(highlightcolor="black")
        self.found_book_count_entry.configure(insertbackground="black")
        self.found_book_count_entry.configure(selectbackground="#c4c4c4")
        self.found_book_count_entry.configure(selectforeground="black")

        self.search_string_entry = tk.Entry(top)
        self.search_string_entry.place(relx=0.318, rely=0.02, height=34
                , relwidth=0.258)
        self.search_string_entry.configure(background="white")
        self.search_string_entry.configure(disabledforeground="#a3a3a3")
        self.search_string_entry.configure(font="TkFixedFont")
        self.search_string_entry.configure(foreground="#000000")
        self.search_string_entry.configure(highlightbackground="#d9d9d9")
        self.search_string_entry.configure(highlightcolor="black")
        self.search_string_entry.configure(insertbackground="black")
        self.search_string_entry.configure(selectbackground="#c4c4c4")
        self.search_string_entry.configure(selectforeground="black")

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.59, rely=0.02, height=33, width=89)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(command=library_support.search_file_name)
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Search Files''')

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.221, rely=0.763, height=26, width=79)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''File Details''')

        self.file_detail_entry = tk.Entry(top)
        self.file_detail_entry.place(relx=0.216, rely=0.804, height=24
                , relwidth=0.099)
        self.file_detail_entry.configure(background="white")
        self.file_detail_entry.configure(disabledforeground="#a3a3a3")
        self.file_detail_entry.configure(font="TkFixedFont")
        self.file_detail_entry.configure(foreground="#000000")
        self.file_detail_entry.configure(highlightbackground="#d9d9d9")
        self.file_detail_entry.configure(highlightcolor="black")
        self.file_detail_entry.configure(insertbackground="black")
        self.file_detail_entry.configure(selectbackground="#c4c4c4")
        self.file_detail_entry.configure(selectforeground="black")

        self.manual_tag_entry = tk.Entry(top)
        self.manual_tag_entry.place(relx=0.627, rely=0.132, height=24
                , relwidth=0.076)
        self.manual_tag_entry.configure(background="white")
        self.manual_tag_entry.configure(disabledforeground="#a3a3a3")
        self.manual_tag_entry.configure(font="TkFixedFont")
        self.manual_tag_entry.configure(foreground="#000000")
        self.manual_tag_entry.configure(highlightbackground="#d9d9d9")
        self.manual_tag_entry.configure(highlightcolor="black")
        self.manual_tag_entry.configure(insertbackground="black")
        self.manual_tag_entry.configure(selectbackground="#c4c4c4")
        self.manual_tag_entry.configure(selectforeground="black")
        self.manual_tag_entry.bind('<Key-Return>',lambda e:library_support.add_tag_e(e))

        self.Button_tag = tk.Button(top)
        self.Button_tag.place(relx=0.636, rely=0.173, height=33, width=66)
        self.Button_tag.configure(activebackground="#d9d9d9")
        self.Button_tag.configure(activeforeground="#000000")
        self.Button_tag.configure(background="#d9d9d9")
        self.Button_tag.configure(command=library_support.add_tag)
        self.Button_tag.configure(disabledforeground="#a3a3a3")
        self.Button_tag.configure(foreground="#000000")
        self.Button_tag.configure(highlightbackground="#d9d9d9")
        self.Button_tag.configure(highlightcolor="black")
        self.Button_tag.configure(pady="0")
        self.Button_tag.configure(text='''Add tag''')

        self.file_tags_scrolledlistbox = ScrolledListBox(top)
        self.file_tags_scrolledlistbox.place(relx=0.63, rely=0.224
                , relheight=0.119, relwidth=0.071)
        self.file_tags_scrolledlistbox.configure(background="white")
        self.file_tags_scrolledlistbox.configure(disabledforeground="#a3a3a3")
        self.file_tags_scrolledlistbox.configure(font="TkFixedFont")
        self.file_tags_scrolledlistbox.configure(foreground="black")
        self.file_tags_scrolledlistbox.configure(highlightbackground="#d9d9d9")
        self.file_tags_scrolledlistbox.configure(highlightcolor="#d9d9d9")
        self.file_tags_scrolledlistbox.configure(selectbackground="#c4c4c4")
        self.file_tags_scrolledlistbox.configure(selectforeground="black")
        self.file_tags_scrolledlistbox.configure(width=10)
        self.file_tags_scrolledlistbox.bind('<Key-Return>',lambda e:library_support.remove_file_tag(e))

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.034, rely=0.905, height=33, width=87)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=library_support.set_tag_as_sub)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Subject Cat''')

        self.Button5 = tk.Button(top)
        self.Button5.place(relx=0.091, rely=0.905, height=33, width=82)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(command=library_support.set_tag_as_obj)
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Object Cat''')

        self.sub_cat_entry = tk.Entry(top)
        self.sub_cat_entry.place(relx=0.034, rely=0.956, height=24
                , relwidth=0.11)
        self.sub_cat_entry.configure(background="white")
        self.sub_cat_entry.configure(disabledforeground="#a3a3a3")
        self.sub_cat_entry.configure(font=font10)
        self.sub_cat_entry.configure(foreground="#000000")
        self.sub_cat_entry.configure(insertbackground="black")
        self.sub_cat_entry.configure(width=194)

        self.obj_cat_entry = tk.Entry(top)
        self.obj_cat_entry.place(relx=0.184, rely=0.956, height=24
                , relwidth=0.116)
        self.obj_cat_entry.configure(background="white")
        self.obj_cat_entry.configure(disabledforeground="#a3a3a3")
        self.obj_cat_entry.configure(font=font10)
        self.obj_cat_entry.configure(foreground="#000000")
        self.obj_cat_entry.configure(insertbackground="black")

        self.Button6 = tk.Button(top)
        self.Button6.place(relx=0.15, rely=0.951, height=33, width=38)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(command=library_support.swap_tags)
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''<->''')

        self.check_contain_checkbutton = tk.Checkbutton(top)
        self.check_contain_checkbutton.place(relx=0.176, rely=0.905
                , relheight=0.032, relwidth=0.048)
        self.check_contain_checkbutton.configure(activebackground="#d9d9d9")
        self.check_contain_checkbutton.configure(activeforeground="#000000")
        self.check_contain_checkbutton.configure(background="#d9d9d9")
        self.check_contain_checkbutton.configure(disabledforeground="#a3a3a3")
        self.check_contain_checkbutton.configure(foreground="#000000")
        self.check_contain_checkbutton.configure(highlightbackground="#d9d9d9")
        self.check_contain_checkbutton.configure(highlightcolor="black")
        self.check_contain_checkbutton.configure(justify='left')
        self.check_contain_checkbutton.configure(text='''contains''')
        self.check_contain_checkbutton.configure(variable=library_support.check_cat_contains)

        self.Button7 = tk.Button(top)
        self.Button7.place(relx=0.238, rely=0.905, height=33, width=125)
        self.Button7.configure(activebackground="#d9d9d9")
        self.Button7.configure(activeforeground="#000000")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(command=library_support.add_cat_relation)
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="#000000")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Add Cat Relation''')

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    vp_start_gui()




