import json
import dao


class Song:
    """Class to query songs"""
    exposed = True

    def GET(self, query=None, author=None, album=None, limit=-1, offset=-1):
        """Return a json array of songs"""
        return json.dumps(dao.getSongs(query, author, album, limit, offset), ensure_ascii=False)
