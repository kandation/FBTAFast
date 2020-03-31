import os, random
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
        os.rename(ori_file, f'{path}save_log_{logfile}_w_{random.randint(1, 10)}.txt')
    else:
        dae = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
        os.rename(ori_file, f'{path}log_{dae}.txt')
