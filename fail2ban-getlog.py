#!/usr/bin/python3
# coding: utf-8
# Julien Pecqueur <julien@peclu DOT net>
# Loïs Taulelle <ltaulell>

from sys import argv

import argparse

parser = argparse.ArgumentParser(description="Extract fail2ban logs to CSV file")
parser.add_argument("-d", action="store_true", help="toggle debug")
parser.add_argument("filein", type=str, help="fial2ban log file to process")
parser.add_argument("fileout", type=str, help="CSV file to append to")
args = parser.parse_args()

old = []

if args.fileout:
    try:
        with open(args.fileout, 'r') as csvfile:
            old = csvfile.readlines()
            entries = len(old)
            print(f'{entries} existing lines')
    except IOError:
        print(f'unable to open {csvfile.name}')

if args.filein:
    try:
        with open(args.filein, 'r') as logfile:
            c = 0
            for line in logfile:
                line = line[0:-1].split(".")
                if "Ban" in line:
                    line = line[-1] + ";" + line[0] + ";" + line[1][0:-4]
                    if not line in old:
                        c += 1

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
