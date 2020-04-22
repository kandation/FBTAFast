import os, shutil

"""
Move All File ind name_ to SPLIT_DIR
"""

dir_name = "../mixa"

name_ = ''
old_dir = f'{dir_name}/{name_}'
files = [f for f in os.listdir(old_dir) if os.path.isfile(f'{old_dir}/{f}')]

count = 0

n = 20000
c = 0
new_dir = ''
for file in files:
    if count % n == 0:
        start_num = str(count).zfill(len(str(n)))
        end_num = str(n * (c+1)).zfill(len(str(n)))
        new_dir = f'{old_dir}/{name_}_{start_num}_{end_num}'
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        c += 1
    count += 1

    print(f'movw {old_dir}/{file} to {new_dir}/{file}')
    shutil.move(f'{old_dir}/{file}', f'{new_dir}/{file}')

    # move_dir = f'{dir_name}/{new_name}'
