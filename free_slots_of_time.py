# Finds free time slots for two people based on their free time in calendars.
# The function will take two list of nested lists of strings representing the
# times where they have other meetings, the time at which they are at work in
# general and also the expected time of the planned meeting of these 2 people.
# Calendars are in sorted order.

from typing import List


class Time:
    def __init__(self, t: str):
        self.hours = int(t.split(":")[0])
        self.minutes = int(t.split(":")[1])
        self.in_minutes = self.hours * 60 + self.minutes


# Merging both calendars in order, so the future function can find free slots
# by looking at the gaps in between already booked times.
def merge_calendars(calendar1: List[List[str]], calendar2: List[List[str]]) \
        -> List[List[str]]:
    res = []
    i, j = 0, 0

    while i < len(calendar1) and j < len(calendar2):
        if Time(calendar1[i][0]).in_minutes < Time(calendar2[j][0]).in_minutes:
            res.append(calendar1[i])
            i += 1
        else:
            res.append(calendar2[j])
            j += 1

    return res + calendar1[i:] + calendar2[j:]


# Getting the daily bounds merged to a bound where both people are at work.
def merge_available_time(time1: List[str], time2: List[str]) -> List[str]:
    available = []
    if Time(time1[0]).in_minutes < Time(time2[0]).in_minutes:
        available.append(time2[0])
    else:
        available.append(time1[0])

    if Time(time1[1]).in_minutes < Time(time2[1]).in_minutes:
        available.append(time1[1])
    else:
        available.append(time2[1])

    return available


# This function will be getting all the available free time slots while
# filtering them based of whether there is enough time for the meeting.
def main(calendar1: List[List[str]], d_bound1: List[str],
         calendar2: List[List[str]], d_bound2: List[str],
         meeting_time: int) -> List[List[str]]:
    bounds = merge_available_time(d_bound1, d_bound2)
    calendar = merge_calendars(calendar1, calendar2)
    final = []

    if Time(calendar[0][0]).in_minutes - Time(bounds[0]).in_minutes >= \
            meeting_time:
        final.append([bounds[0], calendar[0][0]])

    for i in range(len(calendar) - 1):
        if Time(calendar[i][1]).in_minutes < Time(
                calendar[i + 1][0]).in_minutes:
            available_time = Time(calendar[i + 1][0]).in_minutes - \
                             Time(calendar[i][1]).in_minutes
            if available_time >= meeting_time:
                final.append([calendar[i][1], calendar[i + 1][0]])

    if Time(bounds[1]).in_minutes - Time(calendar[-1][1]).in_minutes >= \
            meeting_time:
        final.append([calendar[-1][1], bounds[1]])
    return final


# print(main([['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']],
#           ['9:00', '20:00'],
#          [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'],
#            ['16:00', '17:00']], ['10:00', '18:30'], 30))
