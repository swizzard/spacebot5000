#!/home/ubuntu/spacebot/venv/bin/python
import json
import logging
import multiprocessing
import os
from random import randrange
import subprocess
import sys
import time

from twython import Twython


def get_client(cfg_path):
    with open(cfg_path) as cfg_fil:
        cfg = json.load(cfg_fil)
    return Twython(app_key=cfg['consumer_key'],
                   app_secret=cfg['consumer_secret'],
                   oauth_token=cfg['token'],
                   oauth_token_secret=cfg['secret'])


def make_tweets(client):
    try:
        with open('/home/ubuntu/spacebot/space/space.png', 'rb') as img_file:
            try:
                resp = client.upload_media(media=img_file)
            except Exception as e:
                logging.exception(e.message)
            else:
                media_id = resp['media_id']
        caption = 'SP{}CE'.format('A' * randrange(1, 21))
        yield {'status': caption, 'media_ids': [media_id]}
    except IOError as err:
        logging.exception(err.message)
        raise


def prep_env():
    try:
        subprocess.check_call(['sudo', 'Xvfb', ':1', '-screen', '0',
                               '1024x768x24'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        logging.warning('Xvfb already running')
    os.environ['DISPLAY'] = ':1'


def make_proc():

    def prc():
        subprocess.call(['/home/ubuntu/processing-3.0.1/processing-java',
                         '--sketch=/home/ubuntu/spacebot/space', '--run'])

    proc = multiprocessing.Process(target=prc)
    return proc


def run(path, dry):
    proc = make_proc()
    proc.start()
    time.sleep(120)  # wait for processing to boot up
    cnt = 0
    client = get_client(path)
    for tweet in make_tweets(client):
        if dry:
            print tweet
        else:
            try:
                logging.info(tweet)
                client.update_status(**tweet)
            except Exception as err:
                logging.exception(err.message)
            else:
                cnt += 1
                if cnt > 500:
                    try:
                        proc.terminate()
                    except Exception as err:
                        logging.exception(err.message)
                    proc = make_proc()
                    proc.start()
                time.sleep(2100)


if __name__ == '__main__':
    logging.basicConfig(filename='spacebot.log', level=logging.INFO)
    err = False
    dry = False
    if len(sys.argv) == 1:
        err = True
    elif len(sys.argv) == 3:
        dry = sys.argv[2] in ('true', 'True', '1')
    elif not os.path.exists(sys.argv[1]):
        err = True
    if err:
        print 'usage:\n\tspacebot.py path/to/config.json [dry]'
    else:
        prep_env()
        run(sys.argv[1], dry)

