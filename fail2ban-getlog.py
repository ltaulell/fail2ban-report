#!/usr/bin/env python3
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

# init empty
old_lines = []
old = []

try:
    with open(args.fileout, 'r') as csvfile:
        old_lines = csvfile.readlines()
        entries = len(old_lines)
        print(f'{entries} existing lines')
except FileNotFoundError:
    print(f'{args.fileout} does not exist, creating empty one')
    Path(args.fileout).touch()
except IOError as e:
    print(f'unable to open {args.fileout}: {e}')

# cleanup lines from '\n'
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
                        # filter out, keep IP;date[YYYY-MM-dd];time[hh:mm:ss]
                        if args.debug:
                            print(line)
                        outline = line[-1] + ';' + line[0] + ';' + line[1][0:-4]
                        if outline not in old:
                            # only keep new ones
                            if args.debug:
                                print(f'{c}, {outline}')
                            csvfile.write(outline + '\n')
                            c += 1
        except IOError as e:
            print(f'unable to open {logfile.name}: {e}')

except IOError as e:
    print(f'error with {csvfile.name}: {e}')

print(f'added {c} lines')
