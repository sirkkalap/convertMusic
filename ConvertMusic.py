# This Python file uses the following encoding: utf-8
import argparse
import os
import re
import subprocess as sp
import sys
import unicodedata

__author__ = 'sirpete@iki.fi'

from mutagen.easyid3 import EasyID3
from os import listdir
from os.path import isfile, join
from sys import platform as _platform
from titlecase import titlecase


class Song:
    def __init__(self, artist, name, filename):
        self.artist = artist
        self.name = name
        self.filename = filename


class SongMatcher:
    def __init__(self, knownartists):
        self.KnownArtists = knownartists
        self.m1 = re.compile(r"^[^\w\d]*([\w\d]+[\w\d\s,\.!'_\(\)\[\]\+&-]*?)\s*[-~]\s+([\w\d]+[\w\d\s,\.!'_\(\)\[\]\+&-]*?)\s*$", re.U)

    def tosong(self, f, filename):
        for artist in self.KnownArtists.keys():
            artist_name = self.KnownArtists[artist]
            if f.startswith(artist):
                song = Song(artist_name, f, filename)
                return song

        match = self.m1.search(f)
        if match:
            song = Song(match.group(1), f, filename)
            if song.artist not in self.KnownArtists:
                self.KnownArtists[song.artist] = song.artist
            return song

        song = Song(u'Unknown', f, filename)
        return song


def builduc(names):
    assert isinstance(names, [].__class__)
    return u''.join([unicodedata.lookup(n) for n in names])


def sanitize(filename):
    assert isinstance(filename, unicode)
    tubehash = re.search(r"^(.*)-[0-9A-Za-z_-]{11}\.mp[34]$", filename)
    if tubehash:
        f = titlecase(tubehash.group(1))
    else:
        mp4 = re.search(r"^(.*)\.mp[34]$", filename)
        if mp4:
            f = titlecase(mp4.group(1))
        else:
            f = titlecase(filename)

    apostrophe = builduc(['APOSTROPHE'])
    f = f.replace(builduc(['GRAVE ACCENT']), apostrophe)
    f = f.replace(builduc(['ACUTE ACCENT']), apostrophe)
    f = f.replace(builduc(['SPACE', 'COMBINING ACUTE ACCENT']), apostrophe)
    assert not builduc(['COMBINING DIAERESIS']) in f
    assert not builduc(['COMBINING ACUTE ACCENT']) in f
    assert not builduc(['COMBINING GRAVE ACCENT']) in f
    return f


def get_filepaths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def antidarvin(filename):
    if _platform == "darwin":
        # OS X
        return unicodedata.normalize(u'NFKC', filename)
    else:
        return filename


def darvin(filename):
    if _platform == "darwin":
        # OS X
        return unicodedata.normalize(u'NFKD', filename)
    else:
        return filename


def ffmpeg(srcvideo, dstaudio, ffmpeg):
    dstdir = os.path.dirname(dstaudio)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    command = [ffmpeg, '-y', '-i', srcvideo, dstaudio]
    child = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10 ** 8)
    streamdata = child.communicate()[1]
    rc = child.returncode

    if not rc == 0:
        print(rc, streamdata)


def idtag(dstaudio, artist, album):
    audio = EasyID3(dstaudio)
    audio['album'] = album
    audio['artist'] = artist
    audio.save()


def saneutf(filename):
    result = ''.join([c for c in filename if not unicodedata.name(c, "###UNNAMED###") == "###UNNAMED###"])
    return result


def convert(song, src, dst, ffmpegbin, album):
    srcvideo = join(src, song.filename.replace(u'.mp3', u'.mp4'))
    dstaudio = join(dst, darvin(song.artist), darvin(song.name) + u'.mp3')
    print(dstaudio)
    ffmpeg(srcvideo, dstaudio, ffmpegbin)
    idtag(dstaudio, song.artist, album)


class FileNameAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(FileNameAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values.decode(sys.getfilesystemencoding()))

def get_pair(line):
    key, sep, value = line.decode(sys.getfilesystemencoding()).strip().partition(u":")
    return key.strip(), value.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='optional src',
                        action=FileNameAction, default=u'/Volumes/movies/Musavideot')
    parser.add_argument('--dst', help='optional dst',
                        action=FileNameAction, default=u'/Volumes/music/convert')
    parser.add_argument('--ffmpeg', help='optional ffmpeg',
                        action=FileNameAction, default=u'/usr/local/bin/ffmpeg')
    parser.add_argument('--album', help='optional album',
                        action=FileNameAction, default=u'Tuupi')

    args = parser.parse_args()

    artistlist = join(args.dst, "artist-list.txt")
    if os.path.exists(artistlist):
        with open(artistlist) as fd:
            knownartists = dict([get_pair(line) for line in fd])
    else:
        knownartists = {}

    sm = SongMatcher(knownartists)

    videofiles = sorted([f for f in listdir(args.src) if isfile(join(args.src, f)) and f.endswith(u'.mp4')])
    songs = [sm.tosong(sanitize(saneutf(antidarvin(f))), f) for f in videofiles]
    songsbyname = {}
    for song in songs:
        songsbyname[song.name] = song

    oldfilenames = sorted([f.split('/')[-1] for f in get_filepaths(args.dst) if f.endswith(u'.mp3')])
    oldsongs = [sm.tosong(sanitize(saneutf(antidarvin(f))), f) for f in oldfilenames]

    oldsongsbyname = {}
    for song in oldsongs:
        oldsongsbyname[song.name] = song

    diff = sorted(set(songsbyname.keys()) - set(oldsongsbyname.keys()))

    for songname in diff:
        convert(songsbyname[songname], args.src, args.dst, args.ffmpeg, args.album)


if __name__ == "__main__":
    main()
