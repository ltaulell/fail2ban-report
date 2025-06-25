# fail2ban-report
This tool generate a simple report of fail2ban activity.

```bash
python3 -m pip install pandas matplotlib geoip2 -U
```

## Extract fail2ban log in a CSV file

```bash
$ python3 fail2ban-getlog.py logfile log.csv
```

You could create a cron task to regulary run `fail2ban-getlog log.csv` and populate CSV file.

## Extract multiple fail2ban logs in the same CSV file

```bash
$ for i in fail2ban.log* ;
$ do python3 fail2ban-getlog.py "${i}" log.csv ;
$ done
```

Not optimized at all, slower with larger log.csv.

## Generate the PDF report using the CSV data and GeoLite2-Country database

```bash
$ python3 fail2ban-report.py log.csv GeoLite2-Country.mmdb report.pdf
```

GeoLite2-Country.mmdb has to be downloaded from maxmind.com (no charges), after creating an account.

