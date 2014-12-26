
import time
import mysql.connector

class db_writer(object):
    def __init__(self, table):
        u = 'forest_writer'
        p = 'forestroot'
        h = '192.168.40.14'
        d = 'forest'
        connect = mysql.connector.connect(user=u, password=p, host=h, database=d)
        cursor = connect.cursor()
        self.connect = connect
        self.cursor = cursor
        self.table = table
        
        keylist = [k[0] for k in self.desc if not k in ['id', 'timestamp']]
        self.keylist = keylist
        pass
        
    def insert(self, keys=None, values=None, keydict=None):
        if keydict is not None:
            keys = keydict.keys()
            values = keydict.values()
            pass
        
        self.keycheck(keys)
        
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        key = ','.join(keys)
        value = str(values)
                
        sql = "INSERT INTO %s(timestamp,%s) VALUES('%s',%s);"%(self.table, key, ts, value)
        self.cursor.execute(sql)
        return
        
    def desc(self, table=None):
        if table is None: table = self.table
        self.cursor.execute('DESC %s'%(table))
        desc = self.cursor.fetchall()
        return desc
    
    def keycheck(self, keys):
        for k in keys:
            if not k in self.keylist:
                raise KeyError('%s is not a key of %s'%(k, self.table))
            continue
        return
