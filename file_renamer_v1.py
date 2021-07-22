"""
Renames files in a given directory according to a template.
Was needed to rename photo images made in different points in time chronologically.
NOTE: files are renamed by their last modification date, not creation date, as creation
date may change during copying files between data storages (flash, HDD, smartphone, etc.)
------------------------------------------------------------------------------------------
Dependencies:
None
"""
# TODO: enable choosing between different methods of renaming (date, number, maybe more?)
# TODO: code this using classes (OOP ftw)

import os
import re
from datetime import datetime
from fnmatch import fnmatch
import random

# choose target directory
while True:
    filesdir = input('\nEnter path to the folder with stored files (e.g. c:\\renamefiles): \n')
    if os.path.exists(filesdir): break
    else:
        print('Folder does not exist.')
        continue
filesdir = os.path.normpath(filesdir)

#  show contents of the target directory
print('Contents of "' + filesdir + '": ')
print('\tTYPE  | NAME')
print('-'*60)
dir_slice = 10      # reduce the shown contents of the target dir
for item in os.listdir(filesdir)[:dir_slice]:
    if os.path.isdir(os.path.join(filesdir, item)):
        print('\t<DIR>  ', item)
    elif os.path.isfile(os.path.join(filesdir, item)):
        print('\t<FILE> ', item)
    else:
        print('\t<OTHER>', item)
if len(os.listdir(filesdir)) > dir_slice:
    print('\t... and', len(os.listdir(filesdir)) - dir_slice, 'more.')

print('-' * 60)

# choose method of renaming
method = input('Choose renaming method (by "date" or by "number"): ')
while method not in ['date', 'number']:
    print('Enter "date" or "number": ', end='')
    method = input()
if method == 'date':
    print('*** Files will be renamed according to their creation or '
          '\nmodification time (whichever is earlier).')
if method == 'number':
    print('*** Files will be renamed in the following pattern: 00001.ext, 00002.ext, etc.')

start = input('Do you want to start renaming? ("y" = start / any key = exit): ')
if start == 'y':
    renamed = 0                                     # counter for renamed files
    failed = 0                                      # counter for failed renames
    failedlist = []                                 # list of failed renames (rename manually?)
    skipped = 0                                     # counter for skipped files
    trace = True                                   # True if you want to trace process
    #### RENAME BY DATE ####
    if method == 'date':
        for file in os.listdir(filesdir):
            ext = os.path.splitext(file)[1].lower()     # extract and decapitalize file's extention (.JPG -> .jpg)
            fpath_old = os.path.join(filesdir, file)    # path to the original (not renamed) file
            addname = 1                                 # number to add to new name if it is already in use (0001_1.jpg)
            if os.path.isfile(fpath_old):                       # check if item is a file (not renaming folders)
                fdate = min(os.path.getctime(fpath_old),        # choose the earliest among
                            os.path.getmtime(fpath_old))        # creation or modification time
                fdate_format = datetime.fromtimestamp(fdate).strftime('%d.%m.%Y_%H-%M') # formatting date
                fpath_new = os.path.join(filesdir, fdate_format)    # path to the renamed file
                ptrn = '??.??.????*'                                # pattern of renaming (? is for any char)
                # check if file is already renamed according to the pattern
                # this allows to avoid re-renaming files (supposedly?)
                if fnmatch(file, ptrn):
                    if trace: print('File', file, 'is already renamed. Skipping.')
                    skipped += 1
                    continue
                # try to rename, raises exception if a file with such name
                # already exists in the directory;
                # exception handled by adding a number to a filename
                try:
                    os.rename(fpath_old, fpath_new + ext)
                    if trace: print('Renamed file', file, 'to', os.path.basename(fpath_new + ext))
                    renamed += 1
                except FileExistsError:
                    fpath_new = os.path.join(filesdir, fdate_format + '_' + str(addname))
                    while os.path.basename(fpath_new + ext) in os.listdir(filesdir):
                        addname += 1
                        fpath_new = os.path.join(filesdir, fdate_format + '_' + str(addname))
                    try:
                        os.rename(fpath_old, fpath_new + ext)
                        if trace: print('Renamed file', file, 'to', os.path.basename(fpath_new + ext))
                        renamed += 1
                    except FileExistsError:
                        if trace: print('Failed to rename file', file)
                        failed += 1
                        failedlist.append(fpath_old)
                        continue
            else: continue

    #### RENAME BY NUMBER ####
    if method == 'number':
        # rename files randomly to avoid
        for file in os.listdir(filesdir):
            ext = os.path.splitext(file)[1].lower()  # extract and decapitalize file's extention (.JPG -> .jpg)
            os.rename(os.path.join(filesdir, file), os.path.join(filesdir, str(random.randint(1, 99999)) + ext))
        # list of files sorted by date
        srtd_lst = sorted([os.path.join(filesdir, file) for file in os.listdir(filesdir)],
                          key=os.path.getmtime)
        name = 1 # starting number for renaming
        for file in srtd_lst:
            fpath_old = os.path.join(filesdir, file)
            if os.path.isfile(file):                # check if item is a file (not renaming folders)
                # increase number in {} if you have a LOT of files
                fpath_new = os.path.join(filesdir, '{:04d}'.format(name))
                # renaming
                os.rename(fpath_old, fpath_new + ext)
                renamed += 1
                name += 1
            else: continue

    print('-' * 60)
    print('Finished. Successfully renamed', renamed, 'files. \n'
          'Skipped', skipped, 'files.\n'
          'Failed to rename', failed, 'files.')
    print('-' * 60)
    if failedlist:
        print('List of files with failed renames:')
        for file in failedlist:
            print(file)
        print('*** These files have to be renamed by hand.')

else:
    print('Goodbye!')

# input('\nPress Enter to exit')
