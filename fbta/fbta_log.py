import datetime
import logging
import os

if not os.path.exists('./logs/'):
    os.mkdir('./logs')
logName = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
logging.basicConfig(filename='./logs/log_' + logName + '.log', level=99, format='%(message)s')

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(99)

SHOW_STREAM = True


def log(*args):
    if SHOW_STREAM:
        text = ''

        for i, t in enumerate(args):
            text += str(t) + str('\t' if i != len(args) - 1 else '')
        print(text)

        logger.log(level=99, msg=text.encode('utf8'))



def log_header(*args):
    print('■' * 30)
    log(*args)
    print('■' * 30)


def log_summery(*args):
    print('-' * 100)
    log(*args)
    print('-' * 100, '\n\n')
