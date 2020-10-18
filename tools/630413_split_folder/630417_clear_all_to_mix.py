import os, shutil

"""
Move All File in many folders to a folder
"""

import datetime, time, itertools, random

if __name__ == '__main__':
    start_time = time.time()
    file_name_list = []
    out_of_file = []

    main_dir_name = "../save"
    dirs_name = [f for f in os.listdir(main_dir_name) if os.path.isdir(f'{main_dir_name}')]
    print(dirs_name)
    dir_mix_name = f"../mixa"

    statistic = {'file': 0, 'folder': 0, 'moved': 0, 'error': 0, 'not-dup': 0}

    # Create Dir if has not
    if not os.path.exists(dir_mix_name):
        os.mkdir(dir_mix_name)

    for _dir_name in dirs_name:
        print(_dir_name)

        # Surway Dir
        old_dir = f'{main_dir_name}/{_dir_name}'

        files = []

        # files = [f'{d}/{f}' for r, d, fz in os.walk(f'{old_dir}')][0:20]

        for dr,dd,fz in os.walk(f'{old_dir}'):
            for fzz in fz:
                rxp = f'{dr}/{fzz}'
                if os.path.isfile(rxp):
                    files.append(rxp)



        # Flattern list
        # files = list(itertools.chain.from_iterable(files))[1:10]
        # print(files)

        statistic['folder'] += 1

        for file in files:
            statistic['file'] += 1

            # Clear Duplicate

            statistic['not-dup'] += 1
            file_name_list.append(file)

            file_from = f'{file}'
            # file_dest = f'{dir_mix_name}/{file}'
            file_dest = f"{dir_mix_name}/{file.split('/')[-1]}"


            try:
                # Move Command
                print(f'move {file_from} to {file_dest}')
                shutil.move(file_from, file_dest)
                # os.rename(file_from, file_dest)
                # time.sleep(random.random() / 10)
                statistic['moved'] += 1
            except BaseException as e:
                out_of_file.append(file_from)
                statistic['error'] += 1
                raise e

    print(statistic)
    print(f'END TIME = {time.time() - start_time}')
    print(out_of_file)
