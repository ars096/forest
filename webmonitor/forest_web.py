
import os
import cherrypy

import forest_web_monitor
import forest_web_database


class forest_web(object):
    def __init__(self):
        self.database = forest_web_database.database()
        self.database.exposed = True
        
        self.monitor = forest_web_monitor.forest_monitor()
        self.monitor.exposed = True
        
        self.index = self.monitor.index
        pass
        
    
if __name__ == '__main__':
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
        '/dist' : { 
            'tools.staticdir.on': True ,
            'tools.staticdir.dir': './dist'
        },
        '/css' : {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './css'
        },
        '/js' : {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './js'
        },
        }
    
    cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
            })
    cherrypy.quickstart(forest_web(), '/', conf)
