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


def getAnagraphicTableResults(table, query, limit, offset):
    """Returns a dictionary representing the results of a query on a table
    composed of two columns: id (Integer Primary Key) and Name (Text)"""
    results = []
    s = sqlalchemy.sql.select([table.c.id, table.c.name])

    if query is not None and query.strip() != '':
        s = s.where(table.c.name.like('%' + query + '%'))

    if limit != -1:
        s = s.limit(limit)

    if offset != -1:
        s = s.offset(offset)

    for row in dbconnection.execute(s):
        r = {}
        r['id'] = row[0]
        r['name'] = row[1]
        results.append(r)
    return results


def getBasicSearch(query, limit, offset):
    """Returns a combined search of authors, albums and songs matching the query"""
    r = {}
    r['authors'] = getAuthors(query, limit, offset)
    r['albums'] = getAlbums(query, None, limit, offset)
    r['songs'] = getSongs(query, None, None, limit, offset)
    return r


def getAuthors(query, limit, offset):
    """Returns a dictionary of authors array"""
    return getAnagraphicTableResults(authors, query, limit, offset)


def getAlbums(query, authorid, limit, offset):
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

    if limit != -1:
        s = s.limit(limit)

    if offset != -1:
        s = s.offset(offset)

    for row in dbconnection.execute(s):
        r = {"id": row[0],
             "name": row[1],
             "author": {"id": row[2],
                        "name": row[3]}}
        results.append(r)
    return results


def getSongs(query, authorid, albumid, limit, offset):
    """Returns a dictionary of songs array"""
    results = []
    s = sqlalchemy.sql.select([songs.c.id, songs.c.name,
                               authors.c.id, authors.c.name,
                               albums.c.id, albums.c.name]).where(
                                   songs.c.authorid == authors.c.id).where(
                                       songs.c.albumid == albums.c.id)

    if query is not None and query.strip() != '':
        s = s.where(songs.c.name.like('%' + query + '%'))

    if authorid is not None and authorid.strip() != '':
        try:
            s = s.where(authors.c.id == int(authorid))
        except ValueError:
            pass

    if albumid is not None and albumid.strip() != '':
        try:
            s = s.where(albums.c.id == int(albumid))
        except ValueError:
            pass

    if limit != -1:
        s = s.limit(limit)

    if offset != -1:
        s = s.offset(offset)

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
