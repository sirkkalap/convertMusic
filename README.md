# convertMusic
Python script to convert video files to audio files using ffmpeg

Here I manage my youtube videos and convert them into tagged audio files. 

It is a lot more Python code than I wanted. And it is throughly hardcoded to my liking.
 
**My paths are default and artist list too.**

***DONT BOTHER RUNNING THIS ON YOUR ENV.***

Requirements
------------

- Python + pip (+ virtualenv)
- ffmpeg + lame ( --enable-libmp3lame )
- posix

Running
--------

````bash
    pip install -r requirements.txt
    python ConvertMusic.py folder folder
````

