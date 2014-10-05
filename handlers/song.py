import json
import dao


class Song:
    """Class to query songs"""
    exposed = True

    def GET(self, query=None, author=None, album=None, sort_by='title', sort_order='asc'):
        """Return a json array of songs"""
        return json.dumps(dao.getSongs(query, author, album), ensure_ascii=False)
