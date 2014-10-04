import cherrypy
from handlers import author, album, song
import os, os.path


if __name__ == '__main__':
    cherrypy.tree.mount(
        author.Author(), '/api/authors',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )
    cherrypy.tree.mount(
        album.Album(), '/api/albums',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )
    cherrypy.tree.mount(
        song.Song(), '/api/songs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )
    static_handler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.abspath(os.getcwd())+"/static")
    cherrypy.tree.mount(static_handler, '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
