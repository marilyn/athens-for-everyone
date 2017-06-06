#!/usr/bin/env python

""" Voter data processor for Athens For Everyone. Finds:

Voter status:
    1 - Unregistered or currently unmatched - Name is not present in 
        voting data file
    2 - Registered but not locally active - Name is present in voting 
        data file, but no vote in May 2016 or May 2014
    3 - Registered and active - May 2014 or May 2016 vote present
    4 - Confirmed cannot vote in ACC
                
todo: Commission district (if in group 2 or 3) """

__author__  = 'Marilyn C. Cole'
__date__    = 'January 29, 2017'
__version__ = '1.0.0'

import csv

emails = csv.reader(open('a4e-email-list-2017-03-20.csv', 'rb'))
votes = open('voter-history.csv', 'r').readlines()
writer = csv.writer(open('a4e-email-list-output-2017-06.csv', 'wb'))

for member in emails:
    [ email, first, last, cur_status ] = member
    status = 1
    if first or last:
        csv_name = '%s,%s' % (first, last)
        csv_name = csv_name.lower()
        for record in votes:
            if csv_name in record.lower():
                status = 2
                if (record.find('2014-05') != -1 or record.find('2016-05') != -1):
                    status = 3
                    break
        if (cur_status == '4' and status == 1):
            status = 4
    writer.writerow([email, first, last, status]);
