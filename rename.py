import os, random
# print(__path__)
# os.rename('./log_erz.log', './log_pp.log')
c=''
try:
    with open('log_temp.txt', mode='r') as fo:
        c = fo.read(1024)
except:
    pass

logfile = ''
if '$START_FBTA_TEST$' in c:
    p = str(c).splitlines()
    for i in p:
        if '$START_FBTA_TEST$' in i:
            logfile = str(i).split('/')[-1]
            print(f'Renamed {logfile}')

if logfile:
    os.rename('log_temp.txt', f'log_{logfile}_w_{random.randint(1,10)}.txt')
