import sqlalchemy
from sqlalchemy import Table, MetaData, Column, Integer, Text, ForeignKey
from dbconnection import dbconnection


authors = Table('authors', MetaData(),
                Column('id', Integer, primary_key=True),
                Column('name', Text))

albums = Table('albums', MetaData(),
               Column('id', Integer, primary_key=True),
               Column('authorid', Integer, ForeignKey('authors.id')),
               Column('name', Text))

songs = Table('songs', MetaData(),
              Column('id', Integer, primary_key=True),
              Column('authorid', Integer, ForeignKey('authors.id')),
              Column('albumid', Integer, ForeignKey('albums.id')),
              Column('name', Text))


def getAnagraphicTableResults(table, query):
    """Returns a dictionary representing the results of a query on a table
    composed of two columns: id (Integer Primary Key) and Name (Text)"""
    results = []
    s = sqlalchemy.sql.select([table.c.id, table.c.name])

    if query is not None and query.strip() != '':
        s = s.where(table.c.name.like('%' + query + '%'))

    for row in dbconnection.execute(s):
        r = {}
        r['id'] = row[0]
        r['name'] = row[1]
        results.append(r)
    return results


def getBasicSearch(query):
    """Returns a combined search of authors, albums and songs matching the query"""
    r = {}
    r['authors'] = getAuthors(query)
    r['albums'] = getAlbums(query, None)
    r['songs'] = getSongs(query, None, None)
    return r


def getAuthors(query):
    """Returns a dictionary of authors array"""
    return getAnagraphicTableResults(authors, query)


def getAlbums(query, authorid):
    """Returns a dictionary of albums array"""
    results = []
    s = sqlalchemy.sql.select([albums.c.id, albums.c.name, authors.c.id,
                               authors.c.name]).where(
                                   albums.c.authorid == authors.c.id)

    if query is not None and query.strip() != '':
        s = s.where(albums.c.name.like('%' + query + '%'))

    if authorid is not None and authorid.strip() != '':
        try:
            s = s.where(authors.c.id == int(authorid))
        except ValueError:
            pass

    for row in dbconnection.execute(s):
        r = {"id": row[0],
             "name": row[1],
             "author": {"id": row[2],
                        "name": row[3]}}
        results.append(r)
    return results


def getSongs(query, author, album):
    """Returns a dictionary of songs array"""
    results = []
    s = sqlalchemy.sql.select([songs.c.id, songs.c.name,
                               authors.c.id, authors.c.name,
                               albums.c.id, albums.c.name]).where(
                                   songs.c.authorid == authors.c.id).where(
                                       songs.c.albumid == albums.c.id)

    if query is not None and query.strip() != '':
        s = s.where(songs.c.name.like('%' + query + '%'))

    for row in dbconnection.execute(s):
        r = {"id": row[0],
             "name": row[1],
             "author": {
                 "id": row[2],
                 "name": row[3]},
             "album": {
                 "id": row[4],
                 "name": row[5]}}
        results.append(r)

    return results
