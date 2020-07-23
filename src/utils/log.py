'''
Experiment data logger

convert experiment data to the approriate form to be stored in the databse

'''

import os
import sqlite3

from src.utils.sys import load_json


'''
sqlite wrapper


'''

def is_iter(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)

def create(db, table, **kwargs):
    attrs = ""
    for head, attr in kwargs.items():
        attrs += head + ' ' + attr + ','
    sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(table, attrs[:-1])
    print(sql)
    db.execute(sql)
    
def insert(db, table, rtn_id=False, **kwargs):
    keys, placeholders = "", ""
    values = []
    for k, v in kwargs.items():
        keys += str(k) + ','
        placeholders += '?,'
        values.append(v)
    sql = "INSERT INTO {}({}) VALUES({})".format(table, keys[:-1], placeholders[:-1])
    print(sql)
    db.execute(sql, values)

    if rtn_id:
        rid = db.execute("SELECT LAST_INSERT_ROWID()")
        return rid.fetchone()[0]

def update(db, table, rid, **kwargs):
    keys = ""
    values = []
    for k, v in kwargs.items():
        keys += "{}=?,".format(k)
        values.append(v)
    sql = "UPDATE {} SET {} WHERE id=?".format(table, keys[:-1])
    print(sql)
    values.append(rid)
    db.execute(sql, values)

def delete(db, table, rid):
    pass

def select(db, table, **filters):
    values = []
    if filters is None or len(filters)==0:
        sql = "SELECT * FROM {}".format(table)
    else:
        keys = ""
        for k, v in filters.items():
            keys += "{}=? AND".format(k, v)
            values.append(v)
        sql = "SELECT * FROM {} WHERE {}".format(table, keys[:-4])
    print(sql)
    return db.execute(sql, values).fetchall()
    
    
class Log:
    '''
    logical model of the experiment covering training parameters, models and the metrics
    self-recording the change of parameters in order to update the database record
    '''
    def __init__(self, info, records=None):
        # initialization from the given parameters
        self.old, self.new = {}, {}
        keys = info.keys() if records is None else records
        for k in keys:
            if hasattr(info, k):
                self.old[k] = getattr(info, k)
            else:
                try:
                    self.old[k] = info[k]
                except:
                    pass

    def __setitem__(self, k, v):
        if k not in self.old:
            raise Exception("Invalid key to set in log: {}".format(k))

        if self.old[k] != v:
            self.new[k] = v

    def __getitem__(self, k):
        if k in self.new:
            return self.new[k]
        elif k in self.old:
            return self.old[k]
        else:
            raise Exception("Invalid key to access in log: {}".format(k))
        

TABLES = load_json("/home/lin/Projects/ml-research/src/utils/db.json")
RECORDS = list(TABLES['model'].keys())

class Logger:
    '''
    layer between the database and the data model i.e. Log managing the database operations
    controller for managing the operations on the logs like delete, add and modification etc.

    '''
    def __init__(self, db_path, config=None):
        self.db = sqlite3.connect(db_path)
        for table, attrs in TABLES.items():
            create(self.db, table, **attrs)
        
        if config is not None:
            self.new(config)

    def __del__(self):
        self.db.close()
        
    def __getitem__(self, lid):
        # query the database to get metadata of the log specified by the log id
        # construct the Log instance from the queried data
        return select(self.db, 'model', id=lid)
    
    def training(self, config):
        # construct Log instance from the configuration
        # assign such instance to the attribute self.log
        self.log = Log(config, self.records)
    
    def eval(self, config, metric, value, **kwargs):
        pass

    def monitor(self, **kwrags):
        # recording high-frequency data in a separate file
        pass
    
    def save(self):
        # confirm the incremental part to be saved in the database
        
