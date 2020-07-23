import os
import sqlite3

from base import *
from src.utils.log import *


class TestDB(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)
        db_path = os.path.join(root_path, 'tmp/test/test.db')
        self.db = sqlite3.connect(db_path)
        
    def test_operations(self):
        create(self.db, "test", id="integer PRIMARY KEY", name="text", height="real")
        
        insert(self.db, 'test', name='a', height='175.01')
        rid = insert(self.db, 'test', rtn_id=True, name='b', height='180.01')
        print(rid)
        
        update(self.db, 'test', rid, name='c')
        data = select(self.db, 'test')
        print(data)

        data = select(self.db, 'test', name='c')
        print(data)
        

config = {'dataset': 'CIFAR10',
          'lr': 0.1,
          'optim': 'sgd',
          'batch_size': 128}

class TestLog(TestBase):
    def __init__(self, *args, **kwargs):
        super(TestLog, self).__init__(*args, **kwargs)
        db_path = os.path.join(root_path, 'tmp/test/test.db')
        self.logger = Logger(db_path)
        
    def test_new(self):
        self.logger.new(config)
        
    # def test_getter(self):
    #     log = self.logger[0]
    #     print(log)

if __name__ == '__main__':
    run_test()
