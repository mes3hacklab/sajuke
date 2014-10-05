import json
import dao


class Album:
    """Class to query Albums"""

    exposed = True

    def GET(self, authorid=None, album=None):
        """Return a json array of albums"""
        return json.dumps(dao.getAlbums(album, authorid, -1, -1), ensure_ascii=False)
