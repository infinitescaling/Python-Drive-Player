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

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)


    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication

    results = service.files().list(maxResults=10).execute()
    items = results.get('items', [])
    music = []
    if not items:
        print('No files found.')
    else:
        print('Music:')
        i = 1
        for item in items:
            if '.mp3' in item['title']:
                print('{0}: {1} ({2})'.format(i, item['title'], item['id']))
                music.append(item)
                i = i + 1
        pick_file = input('Choose file to play: \n')
        pick_file = pick_file-1
        play_music(gauth, music[pick_file])
                

def play_music(gauth, item):
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
    music.play()
    pyglet.app.run()

if __name__ == '__main__':
    main()
