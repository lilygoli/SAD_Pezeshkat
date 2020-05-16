from calendar import HTMLCalendar

from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, day=None, doctor=None):
        self.doctor = doctor
        self.year = year
        self.month = month
        self.week = day // 7 #todo
        self.day_abr = {5: 'شنبه', 6: 'یکشنبه', 0: 'دوشنبه', 1: 'سه شنبه', 2: 'چهارشنبه', 3: 'پنجشنبه', 4: 'جمعه'}
        self.month_name = {0: 'فروردین', 1: 'اردیبهشت', 2: 'خرداد', 3: 'تیر', 4: 'مرداد', 5: 'شهریور', 6: 'مهر',
                           7: 'آبان', 8: 'آذر', 9: 'دی', 10: 'بهمن', 11: 'اسفند'}
        super(Calendar, self).__init__(firstweekday=5)

    def iter_hours(self):
        for i in range(8, 21):
            yield i

    def formatweekdays(self, week, events, month, year):
        out = ''
        cal = ''
        print("week", week)
        print("month", self.month, self.week)
        for date, i in week:
            cal = f'<th class="%s">%s</th>' % (
                self.cssclasses_weekday_head[i], self.day_abr[i])
            for hour in self.iter_hours():
                # print("events",events.all()[0].start_time)
                event_of_hour = events.filter(start_time__hour=hour, start_time__day=date)
                if event_of_hour:
                    print("hhh", event_of_hour[0].start_time.month, event_of_hour[0].start_time.year)
                    cal += f'<td> {event_of_hour[0].get_html_url} </td>'
                else:
                    cal += f'<td>    </td>'
            out += f'<tr>{cal}<tr>'
        return out

    def formathour(self, hour):
        if hour > 12:
            out = str(hour % 12) + ' عصر'
        else:
            out = str(hour) + ' صبح'
        return '<th>%s</th>' % out

    def formatdayheader(self):
        s = f'<th>  </th>'
        s += ''.join(self.formathour(i) for i in self.iter_hours())
        print(s)
        return '<tr>%s</tr>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (self.month_name[themonth], theyear - 621)  # todo better fix of year
        else:
            s = '%s' % self.month_name[themonth]
        return '<tr><th colspan="14" class="%s">%s</th></tr>' % (
            self.cssclass_month_head, s)

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, doctor_user=self.doctor)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'  # add date
        cal += f'{self.formatdayheader()}\n'
        count = 0
        for week in self.monthdays2calendar(self.year, self.month):
            print(week)
            if count == self.week:
                cal += f'{self.formatweekdays(week, events, self.month, self.year)}\n'
                break
            count += 1
        return cal
