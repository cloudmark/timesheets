from core.models import WorkType, WorkDay, Holiday
from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import dateutil.parser
import json


def home(request):
    r = RequestContext(request, {})
    return render_to_response('home.html', r)


def calculate(request):
    object = json.loads(request.body)

    start_date = dateutil.parser.parse(object['fromDate'])
    end_date = dateutil.parser.parse(object['toDate'])
    start_with = object['startType']
    start_i = 0

    for work in WorkType._order:
        if work == start_with:
            break
        else:
            start_i += 1

    current_date = start_date
    WorkDay.objects.all().delete()
    while current_date <= end_date:
        WorkDay(day=current_date, day_type=WorkType._order[start_i], description=WorkType._order[start_i]).save()
        start_i += 1
        if start_i == len(WorkType._order):
            start_i = 0
        current_date += datetime.timedelta(days=1)

    # Some extra hours for the month.
    for extra in object['extra']:
        WorkDay(day=dateutil.parser.parse(extra['date']), day_type=WorkType.EXTRA, hours=float(extra['hour']), description=WorkType.EXTRA).save()

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
            normalised_work_days.append(WorkDay(day=valid_work_day.day + datetime.timedelta(days=1), hours=5, day_type=WorkType.NIGHT, description=WorkType.NIGHT))
        if valid_work_day.day_type == WorkType.DAY:
            valid_work_day.hours = 11
            normalised_work_days.append(valid_work_day)
        if valid_work_day.day_type == WorkType.EXTRA:
            normalised_work_days.append(valid_work_day)

    per_day = []
    for valid_work_day in normalised_work_days:
        nwh = 0
        swh = 0

        if valid_work_day.day.weekday() == 6 or valid_work_day.day in holidays_in_period:
            swh = valid_work_day.hours
            per_day.append({'day': str(valid_work_day.day), 'friendly_day': valid_work_day.day.strftime('%A'), 'type': str(valid_work_day.day_type), 'nwh': nwh, 'swh': swh, 'special': True})
        else:
            nwh = valid_work_day.hours
            per_day.append({'day': str(valid_work_day.day), 'friendly_day': valid_work_day.day.strftime('%A'), 'type': str(valid_work_day.day_type), 'nwh': nwh, 'swh': swh, 'special': False})

        sswh += swh
        snwh += nwh

    return HttpResponse(json.dumps({'status': 'OK',
                                    'details': {
                                        'total': snwh + sswh,
                                        'nwh': snwh,
                                        'swh': sswh,
                                        'per_day': per_day
                                        }
                                    }))