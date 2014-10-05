import json
import dao


class Album:
    """Class to query Albums"""

    exposed = True

    def GET(self, authorid=None, album=None, limit=-1, offset=-1):
        """Return a json array of albums"""
        return json.dumps(dao.getAlbums(album, authorid, limit, offset), ensure_ascii=False)
