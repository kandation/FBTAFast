import os,shutil
dir_name = "../save"
dirs = os.listdir(dir_name)
for dir in dirs:
    if 'save_' in dir:
        cpt = sum([len(files) for r, d, files in os.walk(f'{dir_name}/{dir}')])
        if cpt <= 0:
            shutil.rmtree(f'{dir_name}/{dir}')
            print(f'Remove {dir} ({cpt}) files')