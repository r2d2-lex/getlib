#!/usr/bin/python3
import subprocess, time, os, sys, re
import shutil

ldd_path = '/usr/bin/ldd'
not_found = 'not found'
link_to_lib = '=>'
libs_collected = 'clibs/'
libs = set()

def parse_lib(lib_file):
    if lib_file not in libs:
        print('\r\nStart parse file: {}'.format(lib_file))
        cmd = [ ldd_path, lib_file, ]
        text = subprocess.check_output(cmd, encoding='utf8')
        text = text.splitlines()
        for line in text:
            filename = get_filename(line)
            if filename:
                libs.add(filename)
                copy_lib(filename)
                parse_lib(filename)


def copy_lib(libname):
    # print('Source libname: {}'.format(libname))
    dst_name = libname
    if '/' in libname:
        dst_name = libname.split('/')[-1]

    result = shutil.copy(libname, libs_collected+dst_name, follow_symlinks=True)
    if result:
        print('Copied filename: {}\r\n'.format(result))
    else:
        print('Filename {} not copied!!!\r\n'.format(libname))


def get_filename(line):
    math = re.search(not_found, line)
    split_line = line.split(' ')
    if math:
        print('Lib {} not found...\r\n'.format(check_parm(split_line, 0)))
        return False

    second_parm = check_parm(split_line, 1)

    if second_parm.startswith('('):
        return False

    third_parm = check_parm(split_line, 2)
    if third_parm:
        return third_parm


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
