# fail2ban-report
This tool generate a simple report of fail2ban activity.

```bash
python3 -m pip install pandas matplotlib geoip2 -U
```

## Extract fail2ban logs in a CSV file

```bash
$ ./fail2ban-getlog logfile log.csv
```
You could create a cron task to regulary run `fail2ban-getlog log.csv` and populate CSV file.

## Generate the PDF report using the CSV data and GeoLite2-Country database

```bash
./fail2ban-report log.csv GeoLite2-Country.mmdb report.pdf
```

GeoLite2-Country.mmdb has to be downloaded from maxmind.com, after creating an account.

