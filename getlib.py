#!/usr/bin/python3
import subprocess, time, os, sys, re
import shutil

ldd_path = '/usr/bin/ldd'
not_found = 'not found'
link_to_lib = '=>'
libs_collected = 'clibs/'


def parse_lib(lib_file):
    print('\r\nSTART PARSE FILE {}'.format(lib_file))
    cmd = [ ldd_path, lib_file, ]
    text = subprocess.check_output(cmd, encoding='utf8')
    text = text.splitlines()
    for line in text:
        filename = get_filename(line)
        if filename:
            copy_lib(filename)
            parse_lib(filename)


def copy_lib(libname):
    print('Source libname: {}'.format(libname))
    dst_name = libname
    if '/' in libname:
        dst_name = libname.split('/')[-1]
        print('dst_name:', dst_name)

    result = shutil.copy(libname, libs_collected+dst_name, follow_symlinks=True)
    if result:
        print('Copied filename: {}'.format(result))
    else:
        print('Filename {} not copied!!!'.format(libname))


def get_filename(line):
    math = re.search(not_found, line)
    if math:
        print('Lib {} not found...'.format(line))
        return False

    split_line = line.split(' ')
    second_parm = check_parm(split_line, 1)

    if second_parm.startswith('('):
        return False

    third_parm = check_parm(split_line, 2)
    if third_parm:
        return third_parm

    return False


def check_parm(line, index):
    parm = ''
    try:
        parm = line[index]
        # !!!
        parm = remove_space(parm)
    except IndexError:
        print('{} parm not found in {}'.format(index, line))
        return False
    return parm


def remove_space(line):
    return re.sub("^\s+|\n|\r|\s+$", '', line)


def main():
    try:
        libname = sys.argv[1]
    except IndexError:
        print('Enter lib name! Example {} libname'.format(sys.argv[0]))
    print('Using: {}'.format(libname))
    parse_lib(libname)


if __name__ == '__main__':
    main()
