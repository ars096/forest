
import cherrypy

class forest_monitor(object):
    @cherrypy.expose
    def index(self):
        html = open('monitor_template.html', 'r').readlines()
        return html

