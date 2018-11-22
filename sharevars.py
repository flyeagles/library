
# variables for all_books tree_view.
all_book_tree_view = None


# searched book treeview
search_book_tree_view = None


# all category treeview
category_tree_view = None
# complete set of categories
#category_set = set()
category_fname = 'fcategory.pkl'
category_rel_fname = 'fcatrel.pkl'
category_con_fname = 'fcatcont.pkl'



# string of the selected title of the last in-focus tree view
title_in_focus = ""

# the list of candidate tags generated from the selected book title.
# It is used to populate the tag_candidate_scrolledlistbox widget.
tag_candidates = None

# the page-down/up scroll page size in Book treeview.
page_size = 40


# chosen tag listbox
chosen_tags_set = set()

# file name change candidate list
title_changes = []
title_full_path_changes = []

# target dir for the target library folder
target_folder = '.'
lib_index_file = 'findex.pkl'

# control for clip watching thread
not_quit = True
clip_job = None

# tag --> set{file} map
tag_file_dict = dict()   # set item is (title, surfix, folder, size)
TAG_FILE_NAME = 'tagfile.pkl'

# library file monitor
lib_monitor = None