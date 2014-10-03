import cherrypy
from handlers import author, album, song


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
    cherrypy.engine.start()
    cherrypy.engine.block()
