
import json
import datetime
import calendar
import pickle
import zlib
import multiprocessing
import threading
import cherrypy
import mysql.connector



u = 'forest_reader'
p = 'forest'
h = '133.40.197.38'
d = 'forest'



class database(object):
    def __init__(self):
        self.tables = [_t for _t in self.show_tables('csv').split()]
        pass
        
    def _verify_table(self, table):
        if table not in self.tables:
            raise Exception('Database: Table "%s" is not avairable.'%(table))
        return True
    
    def format(self, data, fmt, table=None):
        if table == 'spana': data = self._format_spana(data)
        
        if fmt == 'raw': return self._format_raw(data)
        elif fmt == 'csv': return self._format_csv(data)
        elif fmt == 'json': return self._format_json(data)
        elif fmt == 'table': return self._format_table(data)
        elif fmt == 'list': return self._format_list(data)
        pass
    
    def _format_spana(self, data):
        new_data = []
        for dset in data:
            new_dset = []
            new_dset.append(dset[0])
            new_dset.append(dset[1])
            new_dset.append(list(pickle.loads(dset[2])))
            new_dset.append(list(pickle.loads(dset[3])))
            new_dset.append(list(pickle.loads(dset[4])))
            new_dset.append(list(pickle.loads(dset[5])))
            new_data.append(new_dset)
            continue
        return new_data
        
    def _format_raw(self, data):
        return str(data)
    
    def _format_csv(self, data):
        csv = ''
        for line in data:
            for item in line:
                csv += '%s, '%(str(item))
                continue
            csv = csv[:-2] + '\n'
            continue
        return csv[:-1]
    
    def _format_json(self, data):
        str_data = [[str(_d) for _d in dd] for dd in data]
        json_data = json.dumps(str_data)
        return json_data
    
    def _format_table(self, data):
        table = '<table>\n'
        for line in data:
            table += '<tr>'
            for item in line:
                table += '<td>%s</td>'%(str(item))
                continue
            table += '</tr>\n'
            continue
        table += '</table>'
        return table
    
    def _format_list(self, data):
        li = '<ul>\n'
        for line in data:
            li += '<li><ul>'
            for item in line:
                li += '<li>%s</li>'%(str(item))
                continue
            li += '</ul></li>\n'
            continue
        li += '</ul>'
        return li
        
    def execute(self, sql):
        con = mysql.connector.connect(user=u, password=p, host=h, database=d)
        cur = con.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
        return ret
    
    @cherrypy.expose
    def show_tables(self, fmt='table'):
        db_ret = self.execute('SHOW TABLES')
        db_fmt = self.format(db_ret, fmt)
        return db_fmt
    
    @cherrypy.expose
    def latest(self, table, n=100, fmt='table'):
        self._verify_table(table)
        sql = 'SELECT * FROM %s ORDER BY id DESC LIMIT %d'%(table, int(n))
        db_ret = self.execute(sql)
        db_fmt = self.format(db_ret, fmt, table=table)
        return db_fmt
        
    @cherrypy.expose
    def by_date(self, table, date, fmt='table'):
        self._verify_table(table)
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('date format is %Y-%m-%d (ex. 2015-01-23).')
        start = date.strftime('%Y-%m-%d')
        end = (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        sql = 'SELECT * FROM %s WHERE timestamp BETWEEN "%s" AND "%s"'%(table, start, end)
        db_ret = self.execute(sql)
        db_fmt = self.format(db_ret, fmt, table=table)
        return db_fmt
        
    @cherrypy.expose
    def by_month(self, table, month, fmt='table'):
        self._verify_table(table)
        try:
            month = datetime.datetime.strptime(month, '%Y-%m')
        except ValueError:
            raise ValueError('month format is %Y-%m (ex. 2015-01).')
        start = month.strftime('%Y-%m-%d')
        month_days = calendar.monthrange(month.year, month.month)[1]
        end = (month + datetime.timedelta(days=month_days)).strftime('%Y-%m-%d')
        sql = 'SELECT * FROM %s WHERE timestamp BETWEEN "%s" AND "%s"'%(table, start, end)
        db_ret = self.execute(sql)
        db_fmt = self.format(db_ret, fmt, table=table)
        return db_fmt
        
    @cherrypy.expose
    def by_time(self, table, time, around=5, fmt='table'):
        self._verify_table(table)
        try:
            time = datetime.datetime.strptime(time, '%Y-%m-%d_%H:%M:%S')
        except ValueError:
            raise ValueError('time format is %Y-%m-%d_%H:%M:%S (ex. 2015-01-23_19:20:12).')
        delta = datetime.timedelta(minutes=float(around))
        start = (time - delta).strftim('%Y-%m-%d %H:%M:%S')
        end = (time + delta).strftime('%Y-%m-%d %H:%M:%S')
        sql = 'SELECT * FROM %s WHERE timestamp BETWEEN "%s" AND "%s"'%(table, start, end)
        db_ret = self.execute(sql)
        db_fmt = self.format(db_ret, fmt, table=table)
        return db_fmt
        
    
