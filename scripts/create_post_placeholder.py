#!/usr/bin/env python

# =======================================================
# Creates posts directories with empty placeholder files.
# =======================================================

from datetime import datetime
from datetime import timedelta
import os


# The date range I want to create directories for.
NEXT_N_DAYS = 90


# I will most likely never create posts in the past.
t = datetime.today()
for i in range(NEXT_N_DAYS):
    t = t + timedelta(days=1)
    week_of_year = t.isocalendar()[1]
    day_of_week = t.isoweekday()

    if week_of_year % 2 != 1 or day_of_week != 5:
        # We only care about the Fridays in odd calendar weeks.
        continue

    directory = "../posts/%s/%02d/%02d/" % (t.year, t.month, t.day)
    if os.path.exists(directory):
        # I can execute the script whenever I want.
        continue

    os.makedirs(directory)
    os.mknod(directory + ".placeholder")
