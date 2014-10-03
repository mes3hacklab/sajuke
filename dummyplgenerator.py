#!/usr/bin/python2

import sqlite3
from xml.dom.minidom import parse
import sys


def create_db(conn):
    """Crea il database e le relative tabelle"""
    conn.execute("DROP TABLE IF EXISTS songs")
    conn.execute("DROP TABLE IF EXISTS albums")
    conn.execute("DROP TABLE IF EXISTS authors")
    conn.execute("""
                 CREATE TABLE authors(
                 id      INTEGER PRIMARY KEY,
                 name    TEXT
                 )""")
    conn.execute("""
                 CREATE TABLE albums(
                 id          INTEGER PRIMARY KEY,
                 authorid    INTEGER,
                 name        TEXT,
                 FOREIGN KEY (authorid) REFERENCES authors(id)
                 )""")
    conn.execute("""
                 CREATE TABLE songs(
                 id          INTEGER PRIMARY KEY,
                 authorid    INTEGER,
                 albumid     INTEGER,
                 name        TEXT,
                 FOREIGN KEY (authorid) REFERENCES authors(id),
                 FOREIGN KEY (albumid) REFERENCES albums(id)
                 )""")
    conn.commit()


def fill_authors(tracklist, conn):
    authors = []
    for track in tracklist:
        if track['author'] not in authors:
            authors.append(track['author'])
    # caccia i dati nel db
    for a in authors:
        print "Inserting author " + a
        conn.execute("""
                        INSERT INTO authors (name) VALUES (:name)
                        """, {"name": a})
        conn.commit()


def fill_albums(tracklist, conn):
    albums = []
    for track in tracklist:
        if (track['author'], track['album']) not in albums:
            albums.append((track['author'], track['album']))
    for a in albums:
        print "Inserting album " + a[1] + " for author " + a[0]
        author_id = get_author_id(a[0], conn)
        conn.execute("""
                        INSERT INTO ALBUMS (authorid, name) VALUES (:authorid, :name)
                        """, {"authorid": author_id, "name": a[1]})
        conn.commit()


def fill_songs(tracklist, conn):
    for track in tracklist:
        print "Inserting track " + track['title'] + " for author " + track['author']
        author_id = get_author_id(track['author'], conn)
        album_id = get_album_id(track['album'], author_id, conn)
        title = track['title']
        conn.execute("""
                     INSERT INTO songs (authorid, albumid, name)
                     VALUES
                     (:authorid, :albumid, :name)""",
                     {"authorid": author_id,
                      "albumid": album_id,
                      "name": title[title.find(' - ') + 3:]})
        conn.commit()


def get_author_id(author, conn):
    """Estrai dal db l'id dell'autore"""
    c = conn.cursor()
    c.execute("SELECT id FROM authors WHERE name = :name", {"name": author})
    return c.fetchone()[0]


def get_album_id(album, author_id, conn):
    """Estrai dal db l'id dell'album, fornendo l'id dell'autore"""
    c = conn.cursor()
    c.execute("SELECT id FROM albums WHERE name = :album AND authorid = :authorid",
              {"album": album, "authorid": author_id})
    return c.fetchone()[0]


def get_data(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
            return ''.join(rc)


def parse_xml(path):
    dom = parse(path)
    tracks = []
    for track in dom.getElementsByTagName('track'):
        new_track = {}
        new_track['title'] = get_data(track.getElementsByTagName('title')[0].childNodes)
        new_track['author'] = get_data(track.getElementsByTagName('creator')[0].childNodes)
        new_track['album'] = get_data(track.getElementsByTagName('album')[0].childNodes)
        tracks.append(new_track)
    return tracks


if __name__ == '__main__':
    conn = sqlite3.connect("tracklist.db")
    create_db(conn)
    tracklist = parse_xml("testpl.xspf")
    fill_authors(tracklist, conn)
    fill_albums(tracklist, conn)
    fill_songs(tracklist, conn)
    conn.close()
