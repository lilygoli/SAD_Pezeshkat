from calendar import HTMLCalendar
import datetime
import jdatetime
from accounts.models import User, DoctorProfileInfo
from django.urls import reverse

from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year, month, day, doctor, curr_user, offset):
        self.curr_user = curr_user
        self.doctor = doctor
        self.year = year
        self.month = month
        self.day = day
        self.date = datetime.date(year, month, day) + datetime.timedelta(days=abs(offset) * 7) if offset > 0 else\
                    datetime.date(year, month, day) - datetime.timedelta(days=abs(offset) * 7)
        self.jyear, self.jmonth, self.jday, self.week_day = self.find_jdate(self.date.year, self.date.month,
                                                                            self.date.day)
        self.jmonth_range = self.fix_kabise(self.jyear)
        self.week = self.find_current_week()
        self.day_abr = {0: 'شنبه', 1: 'یکشنبه', 2: 'دوشنبه', 3: 'سه شنبه', 4: 'چهارشنبه', 5: 'پنجشنبه', 6: 'جمعه'}
        self.month_name = {0: 'فروردین', 1: 'اردیبهشت', 2: 'خرداد', 3: 'تیر', 4: 'مرداد', 5: 'شهریور', 6: 'مهر',
                           7: 'آبان', 8: 'آذر', 9: 'دی', 10: 'بهمن', 11: 'اسفند'}
        super(Calendar, self).__init__(firstweekday=0)

    @staticmethod
    def find_jdate(year, month, day):
        jdate = jdatetime.GregorianToJalali(year, month, day)
        jdate = jdatetime.date(jdate.jyear, jdate.jmonth, jdate.jday)
        return jdate.year, jdate.month, jdate.day, jdate.weekday()

    @staticmethod
    def fix_kabise(year):
        jmonth_range = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        indicators = [1, 5, 9, 13, 17, 22, 26, 30]
        if year < 1343:
            indicators[-3] = 21
        if year % 33 in indicators:
            jmonth_range[-1] = 30
        return jmonth_range

    def find_current_week(self):
        jweek = []
        weekday = self.week_day
        day = self.jday
        if day - weekday < 1:
            previous_month = (self.jmonth - 1) % 12
            year = self.jyear - 1 if self.jmonth == 1 else self.jyear
            jmonth_range = self.fix_kabise(year)
            w_range = (jmonth_range[previous_month] - weekday + day, jmonth_range[previous_month] + 1)
            count = 0
            for i in range(w_range[0], w_range[1]):
                date = jdatetime.date(year, previous_month, i)
                jweek += [(date, count)]
                count += 1
        begin = (day - weekday, 0) if day - 1 >= weekday else (1, weekday - day + 1)
        count = 0
        for i in range(begin[0], day + 1):
            date = jdatetime.date(self.jyear, self.jmonth, i)
            jweek += [(date, begin[1] + count)]
            count += 1
        last_day = jweek[-1][1] + 1
        next_month_days = 1
        next_month = (self.jmonth + 1) % 12
        year = self.jyear + 1 if self.jmonth == 12 else self.jyear
        next = False
        while last_day < 7:
            if jweek[-1][0].day + 1 <= self.jmonth_range[self.month] and not next:
                date = jdatetime.date(self.jyear, self.jmonth, jweek[-1][0].day + 1)
                jweek += [(date, last_day)]
            else:
                date = jdatetime.date(year, next_month, next_month_days)
                jweek += [(date, last_day)]
                next_month_days += 1
                next = True
            last_day += 1
        return jweek

    @staticmethod
    def iter_hours(duration):
        h_range = [8 + i * duration for i in range(int((20-8)/duration) + 1)]
        for i in h_range:
            yield i

    def format_weekdays(self, week, events, duration, start_hour, available_days, end_hour):
        out = ''
        for date, i in week:
            gdate = jdatetime.JalaliToGregorian(date.year,date.month, date.day)
            cal = f'<th class="%s">%s</th>' % (
                self.cssclasses_weekday_head[i], self.day_abr[i])
            for hour in self.iter_hours(duration):
                event_of_hour = events.filter(start_hour=hour, start_time__day=gdate.gday, start_time__month=gdate.gmonth,
                                              start_time__year=gdate.gyear)
                if event_of_hour:
                    if not self.curr_user.id == self.doctor:
                        if self.curr_user.id == event_of_hour[0].patient_user.id:
                            if gdate.gyear > self.year or gdate.gmonth > self.month or gdate.gday > self.day:
                                o = f'{event_of_hour[0].get_html_url}'
                            else:
                                o = f'<p class="cal-title">{event_of_hour[0].title}'
                        else:
                            o = f'<p class="cal-title">{event_of_hour[0].title}</p>'
                        cal += f'<td class="reserved"> {o} </td>'
                    else:
                        patient = User.objects.filter(email=event_of_hour[0].patient_user)
                        title = patient[0].name + " " + patient[0].family_name
                        url = reverse('accounts:mini_profile', args=(event_of_hour[0].patient_user.id,))
                        cal += f'<td><p class = "cal_title">{title}</p><a href="{url}"> اطلاعات بیمار </a> </td>'
                else:
                    if not(start_hour <= hour <= end_hour and available_days[i] == '1'):
                        cal += f'<td class="Unavailable-slot">' '</td>'

                    else:
                        if gdate.gyear > self.year or gdate.gmonth > self.month or gdate.gday > self.day:
                            cal += f'<td class="available" onclick=tdclick(' + '"' + str(date) + '#' + str(hour) + '"' + ')>    </td>'
                        else:
                            cal += f'<td onclick=myAlert()>   </td>'

            out += f'<tr>{cal}<tr>'
        return out

    @staticmethod
    def format_hour(hour):
        str_hour = hour // 1
        if str_hour != hour:
            str_minute = str(30 if hour - str_hour == 0.5 else (15 if hour - str_hour == 0.25 else 45))
        else:
            str_minute = '00'
        if hour >= 13:
            out = str(int(str_hour % 12)) + ':' + str_minute + ' عصر'
        else:
            out = str(int(str_hour)) + ':' + str_minute + ' صبح'
        return '<th>%s</th>' % out

    def format_day_header(self, duration):
        s = f'<th>  </th>'
        s += ''.join(self.format_hour(i) for i in self.iter_hours(duration))
        return '<tr>%s</tr>' % s

    def format_month_name(self, theyear, themonth, date_range, duration):
        s = '%s %s' % (self.month_name[themonth-1], theyear)
        out = '<tr><th colspan="30" class="%s">%s <pre> از تاریخ %s تا %s </pre></th></tr>' % (
            'date-header', s, str(date_range[0]), str(date_range[1]))
        return out

    def format_month(self):
        events = Event.objects.filter(doctor_user=self.doctor)
        doctor = DoctorProfileInfo.objects.get(user_id=self.doctor)
        duration = doctor.visit_duration
        start_hour = doctor.start_hour
        end_hour = doctor.end_hour
        available_days = doctor.available_weekdays

        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.format_month_name(self.jyear, self.jmonth, (self.week[0][0], self.week[-1][0]), duration)}\n'
        cal += f'{self.format_day_header(duration)}\n'
        cal += f'{self.format_weekdays(self.week, events, duration, start_hour, available_days, end_hour)}\n'
        return cal
