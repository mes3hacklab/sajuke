import json
import dao


class Album:
    """Class to query Albums"""

    exposed = True

    def GET(self, author=None, query=None, limit=-1, offset=-1):
        """Return a json array of albums"""
        return json.dumps(dao.getAlbums(query, author, limit, offset), ensure_ascii=False)
