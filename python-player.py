from __future__ import print_function
import httplib2
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import pyglet
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

results = []
gauth = ""
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def display_music_list(results):
    music = []
    if not results:
        print('No files found.')
    else:
        print('Music:')
        i = 1
        for item in results:
            if '.mp3' in item['title']:
                print('{0}: {1} ({2})'.format(i, item['title'], item['id']))
                music.append(item)
                i = i + 1
        pick_file = input('Choose file to play: \n')
        pick_file = pick_file-1
        play_music(music[pick_file])


def play_music(item):
    drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance
    path = os.getcwd()
    file6 = drive.CreateFile({'id': item['id']}) # Initialize GoogleDriveFile instance with file id
    music_path = os.path.join(path, item['title'])
    if not os.path.exists(music_path):
        print ('Downloading file: {0}\n'.format(item['title']))
        file6.GetContentFile(item['title']) # Download file as title of item
    music_path = os.path.join(path, item['title'])
    print ('Music path is {0}\n'.format(music_path))
    
    player = pyglet.media.Player()
    music = pyglet.media.load(music_path)
    
    try:
        music.play()
        pyglet.app.run()
    except:
        pyglet.app.exit
        display_music_list(results)

def main():
    global results
    global gauth
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)
    results = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    display_music_list(results)

if __name__ == '__main__':
    main()
