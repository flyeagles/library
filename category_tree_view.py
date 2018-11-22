# by yluo, November 2018

import pandas as pd
import sys
import pickle
import os


class CategoryTreeView:
    def __init__(self, treeview, category_fname, category_rel_fname, category_con_fname):
        self.treeview = treeview
        self.category_fname = category_fname
        self.category_rel_fname = category_rel_fname
        self.category_con_fname = category_con_fname

        self.sub_contain_obj_map = dict()
        self.cat_related_map = dict()
        self.category_set = set()

        self.tag_iid_map = dict()

        self._load_cat_relations()

        self.populate_cats()

    def shutdown(self):
        #def cmd_save_category():
        with open(self.category_fname, 'wb') as AFILE:
            pickle.dump(self.category_set, AFILE)

        with open(self.category_con_fname, 'wb') as AFILE:
            pickle.dump(self.sub_contain_obj_map, AFILE)

        with open(self.category_rel_fname, 'wb') as AFILE:
            pickle.dump(self.cat_related_map, AFILE)

        sys.stdout.flush()

    def get_all_descendents_rec(self, cat):
        if cat not in self.sub_contain_obj_map.keys():
            return set()

        all_descendents = self.sub_contain_obj_map[cat]
        for item in self.sub_contain_obj_map[cat]:
            all_descendents = all_descendents.union(self.get_all_descendents_rec(item))

        return all_descendents

    def add_category(self, item):
        if item not in self.category_set:
            self.category_set.add(item)
            self.treeview.insert('', 'end', text=item)
    
    def add_cat_relation(self, sub, obj, is_contain):
        self.add_category(sub)
        self.add_category(obj)

        if is_contain:
            self._add_contain(sub, obj)
        else:
            self._add_related(sub, obj)

        print(self.sub_contain_obj_map)
        print(self.cat_related_map)

    def get_selected_cat(self):
        focus_iid = self.treeview.focus()
        return self.treeview.item(focus_iid, 'text')

    def populate_cats(self):
        forest_roots = self._get_forest_root()
        root_list = list(forest_roots)
        root_list.sort()
        self.treeview.delete()
        for item in root_list:
            self._recursive_populate('/', item, "")

    def _recursive_populate(self, folder, item, parent_iid):
        full_item_path = self._generate_path(folder, item)
        self.tag_iid_map[full_item_path] = self.treeview.insert(parent_iid, 'end', text=item)

        if item not in self.sub_contain_obj_map.keys():
            return

        for branch in self.sub_contain_obj_map[item]:
            full_branch_path = self._generate_path(full_item_path, branch)
            self._recursive_populate(full_branch_path, branch, self.tag_iid_map[full_item_path])

    def _generate_path(self, folder, item):
        return folder+'/'+item


    #============================================
    # Private methods
    #============================================

    def _get_forest_root(self):
        '''
        We will remove all categories that is contained within another category.
        then just return the roots or solo nodes       
        '''
        all_contained_set = set()
        for contained_set in self.sub_contain_obj_map.values():
            all_contained_set = all_contained_set.union(contained_set)

        return self.category_set.difference(all_contained_set)

    def _get_all_obj_cats(self):
        obj_cat_set = set()
        for obj_set in self.sub_contain_obj_map.values():
            obj_cat_set = obj_cat_set.union(obj_set)

        return obj_cat_set

    def _load_cat_relations(self):
        if os.path.exists(self.category_fname):
            with open(self.category_fname, 'rb') as AFILE:
                self.category_set = pickle.load(AFILE)

        if os.path.exists(self.category_con_fname):
            with open(self.category_con_fname, 'rb') as AFILE:
                self.sub_contain_obj_map = pickle.load(AFILE)

        if os.path.exists(self.category_rel_fname):
            with open(self.category_rel_fname, 'rb') as AFILE:
                self.cat_related_map = pickle.load(AFILE)

    def _add_related(self, cat_1, cat_2):
        # related relation is symmetric.

        cat_1_set = self.cat_related_map.get(cat_1, set())
        if cat_2 in cat_1_set:
            # already related. no need to proceed.
            return

        cat_1_set.add(cat_2)
        self.cat_related_map[cat_1] = cat_1_set

        cat_2_set = self.cat_related_map.get(cat_2, set())
        cat_2_set.add(cat_1)
        self.cat_related_map[cat_2] = cat_2_set
        
    def _add_contain(self, sub, obj):
        obj_cat_set = self.sub_contain_obj_map.get(sub, set())
        if obj in obj_cat_set:
            # already existed there. skip.
            return
        
        obj_cat_set.add(obj)
        self.sub_contain_obj_map[sub] = obj_cat_set

