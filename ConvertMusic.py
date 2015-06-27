# This Python file uses the following encoding: utf-8
import re, os

__author__ = 'petes'

from os import listdir, walk
from os.path import isfile, join
from titlecase import titlecase


class Song:
    def __init__(self, artist, name, filename):
        self.artist = artist
        self.name = name
        self.filename = filename

class SongMatcher:
    def __init__(self):
        self.KnownArtists = set([u'Stacey Q', u'Madonna', u"Frehley's Comet",
                                 u'BATTLE BEAST',
                                 u'DEAD OR ALIVE', u'DEF LEPPARD', u'Led Zepplin'])
        self.m1 = re.compile(r"^[^\w\d]*([\w\d]+[\w\d\s,\.!'_\(\)\[\]\+&-]*?)\s*[-~]\s+([\w\d]+[\w\d\s,\.!'_\(\)\[\]\+&-]*?)\s*$", re.U)
        self.m2 = re.compile(r"^[^\w\d]*([\w\d]+[\w\d\s,\.!'_\(\)\[\]\+&-]*?)\s*$", re.U)

    def tosong(self, f, filename):
        for artist in self.KnownArtists:
            if f == artist:
                return Song(artist, artist, filename)
            if f.startswith(artist):
                song = self.tosong(f.split(artist)[1], filename)
                song.artist = artist
                return song

        match = self.m1.search(f)
        if match:
            song = Song(match.group(1), match.group(2), filename)
            self.KnownArtists.add(song.artist)
            return song

        match2 = self.m2.search(f)
        if match2:
            song = Song(u'Unknown', match2.group(1), filename)
            return song

        song = Song(u'Unknown', f, filename)
        return song


def sanitize(filename):
    tubehash = re.search(r"^(.*)-[0-9A-Za-z_-]{11}\.mp[34]$", filename)
    if tubehash:
        f = titlecase(tubehash.group(1))
    else:
        mp4 = re.search(r"^(.*)\.mp[34]$", filename)
        if mp4:
            f = titlecase(mp4.group(1))
        else:
            f = titlecase(filename)
    f = f.replace(u'´', u"'")
    f = f.replace(u'`', u"'")
    f = f.replace(u'\u0308', u"ä")
    return f

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def main():
    src = u'/Volumes/movies/Musavideot'
    dst = u'/Volumes/music/convert'
    sm = SongMatcher()
    songs = [sm.tosong(sanitize(f), f.replace('.mp4', '.mp3')) for f in listdir(src) if isfile(join(src, f)) and f.endswith(u'.mp4')]
    f = get_filepaths(dst)

    a = set([f.split('/')[-2] for f in f])
    b = set([s.artist for s in songs])
    print sorted(a-b)

if __name__ == "__main__":
    main()
