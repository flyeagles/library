# by yluo, November 2018

import pymysql.cursors
import argparse
import logging
import yaml
import sys
import os
import datetime
import time

# using pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


import library
import features

def set_up_logging(cleanlog):
    # log to both console and file
    filemode = 'a'
    if cleanlog:
        filemode = 'w'
    filehandler = logging.FileHandler(filename=__file__+'.log', mode=filemode)
    stdouthandler = logging.StreamHandler(stream=sys.stdout)
    logging.basicConfig( level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s', handlers=[filehandler, stdouthandler])

def get_script_path(script_dir):
    try:
        filenamepos = script_dir.rindex('\\')
        return script_dir[:filenamepos+1]
    except ValueError:
        return '.\\'

def get_cfg(script_dir, configfile):
    cfg = None
    configfile = get_script_path(script_dir) + configfile
    with open(configfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    return cfg

class FuncSingle:
    def __init__(self, sql, param):
        self.sql = sql
        self.param = param

    def op(self, cursor):
        cursor.execute(self.sql, self.param)

class FuncMany:
    def __init__(self, sql, param):
        self.sql = sql
        self.param = param

    def op(self, cursor):
        cursor.executemany(self.sql, self.param)

def generate_sql_insert_update_pattern(table_name, column_list):
    fields = ', '.join(column_list)
    parameters = ', '.join(['%s' for col in column_list])
    update_clauses = ', '.join([col+'=VALUES('+col+')' for col in column_list])
    sql = 'insert into {tname} ({clist}) VALUES({plist}) on duplicate key update {ulist}'.format(
                    tname=table_name, clist=fields, plist=parameters, ulist=update_clauses
        )

    return sql

def retry_db_exec(cursor, dbfunc):
    count = 15  # may retry five times for DB error
    while count > 0:
        try:
            dbfunc.op(cursor)
            return
        except pymysql.err.InternalError as exp:
            logging.error(exp)
            count -= 1
            if count > 0:
                time.sleep(15-count)
            else:
                raise exp
        except pymysql.err.DataError as exp:
            logging.error(pretty_list_tup(dbfunc.param))
            raise exp


def save_records_in_db(file_metrics, dbconn, tname, columns):
    with dbconn.cursor() as cursor:
        sql =  generate_sql_insert_update_pattern(tname, columns)
        retry_db_exec(cursor, FuncMany(sql, file_metrics))
    dbconn.commit()

def save_to_db(the_list, connection):
    table_name = 'books'
    columns = ['bname', 'folder', 'filename', 
                'surfix', 'authors', 'size', 'mod_date'
    ]
    save_records_in_db(the_list, connection, table_name, columns)

def get_two_chars(the_str):
    res = []
    for idx in range(len(the_str)-2):
        res.append(the_str[idx:idx+2])

    print(res)

import sharevars


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Scan specified folder and upload file info to database.')
    argparser.add_argument("-d", dest='targetdir', # metavar='Folder-root',
                           type=str, default=sharevars.target_folder, required=False,
                           help='The directory path of files. Default is current folder.')

    argparser.add_argument("--config", dest='configfile', # metavar='Folder-root',
                           type=str, default='config.yml', required=False,
                           help='The config YML file. Default is config.yml in script folder.')

    argparser.add_argument("--cleanlog", dest='cleanlog', 
                           default=False, required=False,
                           action='store_true',
                           help='Clean existing log file')

    args = argparser.parse_args()

    print(args)
    sharevars.target_folder = args.targetdir

    set_up_logging(args.cleanlog)

    # cfg = get_cfg(sys.argv[0], args.configfile)
    # Connect to the database
    '''
    connection = pymysql.connect(host=cfg['mysql']['host'],
                                port=cfg['mysql']['port'],
                                user=cfg['mysql']['user'],
                                password=cfg['mysql']['passwd'],
                                db=cfg['mysql']['db'],
                                charset="utf8",
                                cursorclass=pymysql.cursors.DictCursor)
    '''
    try:
        library.vp_start_gui()

    finally:
        sharevars.not_quit = False
        #connection.close()
