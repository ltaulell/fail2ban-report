#!/usr/bin/python3
# coding: utf-8
# Julien Pecqueur <julien@peclu DOT net>

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import geoip2.database
from matplotlib.backends.backend_pdf import PdfPages
from sys import argv


def load_file(file):
    data = []
    f = open(file)
    for l in f:
        ip, date, time = l.split(";")
        data.append([ip, date])
    return(data)

def get_nb_ban_by_date(data):
    d = {}
    for ip, date in data:
        if date in d.keys():
            d[date] += 1
        else:
            d[date] = 1
    return(d)

def get_nb_ban_by_ip(data):
    d = {}
    for ip, date in data:
        if ip in d.keys():
            d[ip] += 1
        else:
            d[ip] = 1
    return(d)

def get_nb_ban_by_country(data, f_country):
    reader = geoip2.database.Reader(f_country)
    d = {}
    for ip, date in data:
        try:
            response = reader.country(ip)
            country = response.country.name
        except:
            country = "n/c"
        if country in d.keys():
            d[country] += 1
        else:
            d[country] = 1
    reader.close()
    return(d)

# Creating autocpt arguments
def reformat(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    # return "{:.1f}%\n({:d} g)".format(pct, absolute)
    return f'{absolute}'

def generate_report(f_log, f_country, f_pdf):
    
    data = load_file(f_log)
    
    pp = PdfPages(f_pdf)

    nb_ban_by_date = get_nb_ban_by_date(data)
    df = pd.DataFrame.from_dict(nb_ban_by_date, orient='index').rename(columns={0:"Bans"}).sort_index()
    plot = df.plot(title="Bans by date", figsize=(10.0,4.0))
    fig = plot.get_figure()
    fig.savefig(pp, format='pdf')
    
    nb_ban_by_country = get_nb_ban_by_country(data, f_country)
    # df = pd.DataFrame.from_dict(nb_ban_by_country, orient='index').rename(columns={0:"Bans"}).sort_values(by='Bans', ascending=False).head(20)
    df = pd.DataFrame.from_dict(nb_ban_by_country, orient='index').sort_values(by=0, ascending=False).head(20).rename(columns={0:""})
    # autopct='%1.1f%%'
    plot = df.plot(title="Bans by country (top 20)", kind='pie', subplots=True, legend=False, figsize=(10.0,10.0), autopct=lambda pct: reformat(pct, df))
    fig = plot[0].get_figure()
    fig.savefig(pp, format='pdf')

    nb_ban_by_ip = get_nb_ban_by_ip(data)
    df = pd.DataFrame.from_dict(nb_ban_by_ip, orient='index').sort_values(by=0, ascending=False).head(20).rename(columns={0:""})
    plot = df.plot(title="Bans by IP (top 20)", kind='pie', legend=False, subplots=True, figsize=(10.0,10.0), autopct=lambda pct: reformat(pct, df))
    fig = plot[0].get_figure()
    fig.savefig(pp, format='pdf')
    
    pp.close()

if len(argv) != 4:
    print("Usage: fail2ban-report <fail2ban.csv> <GeoLite2-Country.mmdb> <report.pdf>")
    print("Compute fail2ban CSV file and generate PDF report.")
else:
    generate_report(argv[1], argv[2], argv[3])

