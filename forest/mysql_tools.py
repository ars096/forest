
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
        
        keylist = [k[0] for k in self.desc() if not k in ['id', 'timestamp']]
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
        value = str(values).strip('()[]')
        
        sql = "INSERT INTO %s(timestamp,%s) VALUES('%s',%s);"%(self.table, key, ts, value)
        #print(sql)
        self.cursor.execute(sql)
        return
        
    def update(self, keydict, interval=60):
        db_latest = self.get_latest_item()
        db_latest_timestamp = time.mktime(db_latest[1].timetuple())
        db_latest_items = sorted(db_latest[2:])
        latest_items = sorted(keydict.values())
        
        def check(data1, data2):
            for d1, d2 in zip(data1, data2):
                if type(d1) == float:
                    if abs(d1 - d2) > 0.0001:
                        #print(d1, d2)
                        return False
                    pass
                if d1 != d2:
                    #print(d1, d2)
                    return False
                continue
            return True
        
        now = time.time()
        if check(db_latest_items, latest_items):
            if (now - db_latest_timestamp) < interval: return
            pass
        
        now = time.time()
        self.insert(keydict=keydict)
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
    
    def get_latest_item(self, num=1):
        sql = 'SELECT * FROM %s ORDER BY id DESC LIMIT %d'%(self.table, num)
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        if num == 1: return ret[0]
        return ret
