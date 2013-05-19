from datetime import timedelta
import random
import unittest
from core.models import WorkDay, Holiday
import dateutil.parser
from core.models import WorkType


class TestSequenceFunctions(unittest.TestCase):

    def testing_marie(self):
        Holiday(day=dateutil.parser.parse('2013-01-01'), description="New Year").save()
        Holiday(day=dateutil.parser.parse('2013-02-10'), description="St. Paul").save()
        Holiday(day=dateutil.parser.parse('2013-03-19'), description="St. Joseph").save()
        Holiday(day=dateutil.parser.parse('2013-03-27'), description="Good Friday").save()
        Holiday(day=dateutil.parser.parse('2013-03-31'), description="Freedom Day").save()
        Holiday(day=dateutil.parser.parse('2013-05-01'), description="Workers Day").save()
        Holiday(day=dateutil.parser.parse('2013-06-07'), description="Sette Giugno").save()
        Holiday(day=dateutil.parser.parse('2013-06-29'), description="St. Peter / St. Paul").save()
        Holiday(day=dateutil.parser.parse('2013-08-15'), description="St. Mary").save()
        Holiday(day=dateutil.parser.parse('2013-09-08'), description="St. Victoria").save()
        Holiday(day=dateutil.parser.parse('2013-09-21'), description="Independence").save()
        Holiday(day=dateutil.parser.parse('2013-12-08'), description="Immaculate Conception").save()
        Holiday(day=dateutil.parser.parse('2013-12-13'), description="Republic").save()
        Holiday(day=dateutil.parser.parse('2013-12-25'), description="Christmas").save()

        start_date = dateutil.parser.parse('2013-04-29')
        end_date = dateutil.parser.parse('2013-05-26')
        start_with = WorkType.REST
        start_i = 0

        for work in WorkType._order:
            if work == start_with:
                break
            else:
                start_i += 1

        current_date = start_date
        while current_date <= end_date:
            WorkDay(day=current_date, day_type=WorkType._order[start_i], description=WorkType._order[start_i]).save()
            start_i += 1
            if start_i == len(WorkType._order):
                start_i = 0
            current_date += timedelta(days=1)

        # Some extra hours for the month.
        WorkDay(day=dateutil.parser.parse('2013-04-30'), day_type=WorkType.EXTRA, hours=8, description=WorkType.EXTRA).save()

        valid_work_days = WorkDay.objects.filter(day__gte=start_date, day__lte=end_date).order_by('day')
        holidays_in_period = Holiday.objects.filter(day__gte=start_date, day__lte=end_date).order_by('day')
        holidays_in_period = [holiday.day for holiday in holidays_in_period]

        snwh = 0
        sswh = 0
        normalised_work_days = []

        for valid_work_day in valid_work_days:
            if valid_work_day.day_type == WorkType.NIGHT:
                valid_work_day.hours = 4.5
                normalised_work_days.append(valid_work_day)
                normalised_work_days.append(WorkDay(day=valid_work_day.day + timedelta(days=1), hours=5, description=WorkType.REST))
            if valid_work_day.day_type == WorkType.DAY:
                valid_work_day.hours = 11
                normalised_work_days.append(valid_work_day)
            if valid_work_day.day_type == WorkType.EXTRA:
                normalised_work_days.append(valid_work_day)

        for valid_work_day in normalised_work_days:
            nwh = 0
            swh = 0

            if valid_work_day.day.weekday() == 6 or valid_work_day.day in holidays_in_period:
                swh = valid_work_day.hours
                print "* %s - [%s] NWH: %s, SWH: %s" % (valid_work_day.day, valid_work_day.description, nwh, swh)
            else:
                nwh = valid_work_day.hours
                print "%s - [%s] NWH: %s, SWH: %s" % (valid_work_day.day, valid_work_day.description, nwh, swh)

            sswh += swh
            snwh += nwh

        print "==========================================================================="
        print "NWH: %s, SWH: %s" % (snwh, sswh)
