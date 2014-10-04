import json
import dao


class BasicSearch:
    """Class for the basic search query"""

    exposed = True

    def GET(self, query=None):
        """Return a json array of albums"""
        return json.dumps(dao.getBasicSearch(query), ensure_ascii=False)
