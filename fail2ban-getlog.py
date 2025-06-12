#!/usr/bin/python3
# coding: utf-8
# Julien Pecqueur <julien@peclu.net>

from sys import argv

if len(argv) != 3:
    print("Usage: fail2ban-getlog <log> <file>")
    print("Extract fail2ban logs to CSV file.")
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

