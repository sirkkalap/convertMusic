# This Python file uses the following encoding: utf-8
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
    def __init__(self):
        self.KnownArtists = {
            u'AMORPHIS': u'AMORPHIS',
            u'Abba': u'Abba',
            u'Accept': u'Accept',
            u'Advanced Art': u'Advanced Art',
            u'Aikakone': u'Aikakone',
            u'Alexia': u'Alexia',
            u'Alizee': u'Alizee',
            u'Anna Abreu': u'Anna Abreu',
            u'Antique': u'Antique',
            u'Apocalyptica': u'Apocalyptica',
            u'Apocalyptica Ft Nina Hagen': u'Apocalyptica Ft Nina Hagen',
            u'BATTLE BEAST': u'BATTLE BEAST',
            u'Bad Boys Blue': u'Bad Boys Blue',
            u'Bad English': u'Bad English',
            u'Basic Element': u'Basic Element',
            u'Bednaya Nastya': u'Bednaya Nastya',
            u'Billy Idol': u'Billy Idol',
            u'Blackstar Halo': u'Blackstar Halo',
            u'Boga': u'Boga',
            u'Bonfire': u'Bonfire',
            u'Brooklyn Bounce': u'Brooklyn Bounce',
            u'Bryan Adams': u'Bryan Adams',
            u'C-Block': u'C-Block',
            u'Cappella': u'Cappella',
            u'Cher': u'Cher',
            u'City Lights': u'City Lights',
            u'Corona': u'Corona',
            u'DEAD OR ALIVE': u'DEAD OR ALIVE',
            u'Dead or Alive' u'DEF LEPPARD': u'Dead or Alive' u'DEF LEPPARD',
            u'DJ BoBo': u'DJ BoBo',
            u'Daryl Hall & John Oates': u'Daryl Hall & John Oates',
            u'Deep Purple': u'Deep Purple',
            u'Deftones': u'Deftones',
            u'Depeche Mode': u'Depeche Mode',
            u'Don Johnson': u'Don Johnson',
            u'Donna Summer': u'Donna Summer',
            u'Doom Unit': u'Doom Unit',
            u'EUROPE': u'EUROPE',
            u'Eagles': u'Eagles',
            u'East 17': u'East 17',
            u'Edwyn Collins': u'Edwyn Collins',
            u'Enigma': u'Enigma',
            u'Europe': u'Europe',
            u'Faith No More': u'Faith No More',
            u'Five Star': u'Five Star',
            u'Foreigner': u'Foreigner',
            u'Franklin Zoo': u'Franklin Zoo',
            u"Frehley's Comet": u"Frehley's Comet",
            u'Golden Earring': u'Golden Earring',
            u'HIM': u'HIM',
            u'Happoradio': u'Happoradio',
            u'Heart': u'Heart',
            u'Hollywood Beyond': u'Hollywood Beyond',
            u'INFERNAL': u'INFERNAL',
            u'Imagination': u'Imagination',
            u'Inxs': u'Inxs',
            u'Iron Maiden': u'Iron Maiden',
            u'Jam & Spoon': u'Jam & Spoon',
            u'Janis Joplin': u'Janis Joplin',
            u'Jenni Vartiainen': u'Jenni Vartiainen',
            u'Jonna Tervomaa': u'Jonna Tervomaa',
            u'Judas Priest': u'Judas Priest',
            u'Katy Perry': u'Katy Perry',
            u'Kepes Mode': u'Kepes Mode',
            u'Killing Joke': u'Killing Joke',
            u'Kim Wilde': u'Kim Wilde',
            u'Kiss': u'Kiss',
            u'Korn': u'Korn',
            u'Kwan': u'Kwan',
            u'La Bouche': u'La Bouche',
            u'Lady GaGa': u'Lady Gaga',
            u'Lady Gaga': u'Lady Gaga',
            u'Larry Greene': u'Larry Greene',
            u'Laura Branigan (Clip)': u'Laura Branigan (Clip)',
            u'Led Zepplin': u'Led Zepplin',
            u'Leila K': u'Leila K',
            u'Lestat': u'Lestat',
            u'Linkin Park': u'Linkin Park',
            u'Lita Ford': u'Lita Ford',
            u'Lordi': u'Lordi',
            u'Lords of the New Church': u'Lords of the New Church',
            u'Lou Gramm': u'Lou Gramm',
            u'Madonna': u'Madonna',
            u'Maggie Reilly': u'Maggie Reilly',
            u'ManOwaR': u'ManOwaR',
            u'Marilyn Manson': u'Marilyn Manson',
            u'Martti Vainaa & Sallitut Aineet': u'Martti Vainaa & Sallitut Aineet',
            u'McAuley Schenker Group (MSG)': u'McAuley Schenker Group (MSG)',
            u'Mekanism': u'Mekanism',
            u'Melodie Mc': u'Melodie Mc',
            u'Metallica': u'Metallica',
            u'Michael Sembello': u'Michael Sembello',
            u'Mikko Sipola': u'Mikko Sipola',
            u'Modern Talking': u'Modern Talking',
            u'Mortiis': u'Mortiis',
            u'Mr. President': u'Mr. President',
            u'Mr. Zivago': u'Mr. Zivago',
            u'Mummy Calls': u'Mummy Calls',
            u'Nancy Spungen': u'Nancy Spungen',
            u'Nicke Borg': u'Nicke Borg',
            u'Nightcore': u'Nightcore',
            u'Nightwish': u'Nightwish',
            u'Nina Hagen': u'Nina Hagen',
            u'Nirvana': u'Nirvana',
            u'No Doubt': u'No Doubt',
            u'Ozzy Osbourne': u'Ozzy Osbourne',
            u'Pandora': u'Pandora',
            u'Pantera': u'Pantera',
            u'Pet Shop Boys': u'Pet Shop Boys',
            u'Placebo': u'Placebo',
            u'Poets of the Fall': u'Poets of the Fall',
            u'Rainbow': u'Rainbow',
            u'Rammstein': u'Rammstein',
            u'Revengine': u'Revengine',
            u'Rihanna': u'Rihanna',
            u'Rod Stewart': u'Rod Stewart',
            u'Roxette': u'Roxette',
            u'Ruinside': u'Ruinside',
            u'Rush': u'Rush',
            u'Sabrina': u'Sabrina',
            u'Sade': u'Sade',
            u'Sammy Hagar': u'Sammy Hagar',
            u'Santa Esmeralda Starring Leroy Gomez': u'Santa Esmeralda Starring Leroy Gomez',
            u'Savage Garden': u'Savage Garden',
            u'Shakira': u'Shakira',
            u'Shout': u'Shout',
            u'Sid Vicious': u'Sid Vicious',
            u'Silent Circle': u'Silent Circle',
            u'Smack': u'Smack',
            u'Snap!': u'Snap!',
            u'Stacey Q': u'Stacey Q',
            u'Stephanie': u'Stephanie',
            u'Stevie Ray Vaughan & Double Trouble': u'Stevie Ray Vaughan & Double Trouble',
            u'Stig': u'Stig',
            u'TO_DIE_FOR': u'To Die For',
            u'Ted Nugent': u'Ted Nugent',
            u'The Chamber': u'The Chamber',
            u'The Corrs': u'The Corrs',
            u'The Human League': u'The Human League',
            u'The Veronicas': u'The Veronicas',
            u'To Die For': u'To Die For',
            u'To_Die_For': u'To Die For',
            u'Wa Wa Nee': u'Wa Wa Nee',
            u"Waldo's People": u"Waldo's People",
            u'Waldos People': u"Waldo's People",
            u'Warmen': u'Warmen',
            u'Within Temptation': u'Within Temptation',
            u'Yngwie Malmsteen': u'Yngwie Malmsteen',
            u't.A.T.u': u't.A.T.u',
            u'\u0410\u043d\u0436\u0435\u043b\u0438\u043a\u0430 \u0412\u0430\u0440\u0443\u043c': u'\u0410\u043d\u0436\u0435\u043b\u0438\u043a\u0430 \u0412\u0430\u0440\u0443\u043c',
            u'\u041d\u0410\u0422\u0410\u041b\u042c\u042f \u0412\u0415\u0422\u041b\u0418\u0426\u041a\u0410\u042f': u'\u041d\u0410\u0422\u0410\u041b\u042c\u042f \u0412\u0415\u0422\u041b\u0418\u0426\u041a\u0410\u042f'
        }
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
            if not self.KnownArtists.has_key(song.artist):
                self.KnownArtists[song.artist] = song.artist
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

def ffmpeg(srcvideo, dstaudio):
    dstdir = os.path.dirname(dstaudio)
    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    FFMPEG_BIN = os.getenv("FFMPEG_BIN", '/usr/local/bin/ffmpeg')

    command = [FFMPEG_BIN, '-y', '-i', srcvideo, dstaudio]
    child = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10**8)
    streamdata = child.communicate()[1]
    rc = child.returncode

    if not rc == 0:
        print rc, streamdata

def idtag(dstaudio, artist):
    audio = EasyID3(dstaudio)
    audio['album'] = u'Tuupi'
    audio['artist'] = artist
    audio.save()


def saneutf(filename):
    result = ''.join([c for c in filename if not unicodedata.name(c, "###UNNAMED###") == "###UNNAMED###"])
    return result

def convert(song, src, dst):
    srcvideo = join(src, song.filename.replace(u'.mp3', u'.mp4'))
    dstaudio = join(dst, darvin(song.artist), darvin(song.name) + u'.mp3')
    print dstaudio
    ffmpeg(srcvideo, dstaudio)
    idtag(dstaudio, song.artist)

def main():
    src = u'/Volumes/movies/Musavideot'
    dst = u'/Volumes/music/convert3'
    if len(sys.argv) > 1:
        src = sys.argv[1].decode(sys.getfilesystemencoding())
    if len(sys.argv) > 2:
        dst = sys.argv[2].decode(sys.getfilesystemencoding())

    sm = SongMatcher()

    videofiles = sorted([f for f in listdir(src) if isfile(join(src, f)) and f.endswith(u'.mp4')])
    songs = [sm.tosong(sanitize(saneutf(antidarvin(f))), f) for f in videofiles]
    songsbyname = {}
    for song in songs:
        songsbyname[song.name] = song

    oldfilenames = sorted([f.split('/')[-1] for f in get_filepaths(dst) if f.endswith(u'.mp3')])
    oldsongs = [sm.tosong(sanitize(saneutf(antidarvin(f))), f) for f in oldfilenames]

    oldsongsbyname = {}
    for song in oldsongs:
        oldsongsbyname[song.name] = song

    diff = sorted(set(songsbyname.keys()) - set(oldsongsbyname.keys()))

    for songname in diff:
        convert(songsbyname[songname], src, dst)

if __name__ == "__main__":
    main()
