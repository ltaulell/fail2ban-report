#!/usr/bin/python3
# coding: utf-8
# Julien Pecqueur <julien@peclu DOT net>
# Loïs Taulelle <ltaulell>

#from sys import argv

import argparse

from pathlib import Path

parser = argparse.ArgumentParser(description='Extract fail2ban logs to CSV file')
parser.add_argument('-d', '--debug', action='store_true', help='toggle debug')
parser.add_argument('filein', type=str, help='fail2ban log file to process')
parser.add_argument('fileout', type=str, help='CSV file to append to')
args = parser.parse_args()

old = []
old_lines = []

try:
    with open(args.fileout, 'r') as csvfile:
        old_lines = csvfile.readlines()
        entries = len(old_lines)
        print(f'{entries} existing lines')
except FileNotFoundError:
    print(f'{args.fileout} does not exist, creating')
    Path(args.fileout).touch()

for line in old_lines:
    old.append(line.strip())

if args.debug:
    print(old)

try:
    with open(args.fileout, 'a') as csvfile:
        try:
            with open(args.filein, 'r') as logfile:
                c = 0
                for line in logfile:
                    line = line[0:-1].split(' ')
                    if 'Ban' in line:
                        if args.debug:
                            print(line)
                        outline = line[-1] + ';' + line[0] + ';' + line[1][0:-4]
                        if outline not in old:
                            if args.debug:
                                print(f'{c}, {outline}')
                            csvfile.write(outline + '\n')
                            c += 1
        except IOError:
            print(f'unable to open {logfile.name}')

except IOError:
    print(f'error with {csvfile.name}')

print(f'added {c} lines')


"""

else:
    F_LOG = argv[1]
    f_old = open(argv[2], "r")
    old = []
    for l in f_old:
        old.append(l[0:-1])
    f_old.close()
    print(len(old), "existing line(s).")
    f_in = open(F_LOG, "r")
    f_out = open(argv[2], "a+")
    c = 0
    for l in f_in:
        l = l[0:-1].split(" ")
        if "Ban" in l:
            l = l[-1]+";"+l[0]+";"+l[1][0:-4]
            if not l in old:
                f_out.write(l+"\n")
                c += 1
    f_in.close()
    f_out.close() 
    print("Added", c, "new line(s).")
"""
