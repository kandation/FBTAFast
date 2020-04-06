import os, random, os.path
import datetime

path = './Logs/'
ori_file = 'log_temp.log'
c = ''
if os.path.isfile(ori_file):

    try:
        with open(ori_file, mode='r') as fo:
            c = fo.read(1024)
    except:
        pass

    is_sequnce_log = False

    logfile = ''
    if '$START_FBTA_TEST$' in c:
        p = str(c).splitlines()
        for i in p:
            if '$START_FBTA_TEST$' in i:
                logfile = str(i).split('/')[-1]
                print(f'Renamed {logfile}')

    if logfile:
        same_file = len([name for name in os.listdir(path) if logfile in name])
        n = f'{path}save_log_{logfile}_w_{str(same_file).zfill(4)}.txt'
        os.rename(ori_file, n + f'')
    else:
        dae = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
        os.rename(ori_file, f'{path}log_{dae}.txt')
