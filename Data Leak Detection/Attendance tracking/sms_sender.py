import requests
from django.utils import timezone

from attendance.models import Attendance

data = {
    'uname': 'rubais',
    'pwd': 'smsapi123',
    'senderid': 'ThreeG',
    'to': '',
    'msg': '',
    'route': 'T',
}

BASE_URL = "http://sms.lyvee.com/sendsms"

today_date = timezone.now()


def send_sms():
    for attendance in Attendance.objects.filter(date=today_date.date()):
        if not attendance.is_present:
            data['to'] = str(attendance.student.phone)
            data['msg'] = 'Your ward ' + attendance.student.user.username + ' Was absent on ' + str(
                timezone.now().date())
            r = requests.get(BASE_URL, data)
            print(r.url)
