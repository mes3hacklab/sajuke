import json
import dao
import album


class Author(object):
    """Class to query authors"""
    exposed = True

    def __init__(self):
        self.albums = album.Album()

    def GET(self, name=None):
        """Return a json array of authors"""
        return json.dumps(dao.getAuthors(name, -1, -1))
