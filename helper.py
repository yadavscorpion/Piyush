"""
Author : Sidhin S Thomas

Any enquiries regarding code, email at sidhin.thomas@gmail.com

Copyright 2016 Shift2Cloud Technologies
"""

from django.shortcuts import render

from attendance.models import Attendance, Test, Marks

"""
These functions are to check is a giving User is of which type
"""


def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()


def is_student(user):
    return user.groups.filter(name='Student').exists()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_principal(user):
    return user.groups.filter(name='Principal').exists()


"""
View helper function to generate a context for the template in case error message is to be printed
"""


def get_error_context(request):
    try:
        error = request.GET['status']
        message = 'Something went wrong'
        if error == 'loginerror':
            message = 'Username or password incorrect'
        elif error == 'formerror':
            message = 'Enter the details'
        elif error == 'userexist':
            message = 'The username already exists, please try a new one'
        elif error == 'success':
            message = 'The operation was successfull'
        elif error == 'rollerror':
            message = 'Roll number repeated'
        elif error == "pherror":
            message = 'Phone number is incorrect'
        elif error == 'pswdchg':
            message = 'Password successfully changed'
        elif error == 'selecterror':
            message = 'Please select from the list'
        context = {'error_message': message}
    except KeyError:
        context = {}
    return context


########################################################
#                   Decorators                         #
########################################################

"""
These decorators help to make sure that only a particular user group is allowed access
"""


def admin_login_required(function):
    def wrapper(request):
        if not is_admin(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def teacher_login_required(function):
    def wrapper(request):
        if not is_teacher(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def principal_login_required(function):
    def wrapper(request):
        if not is_principal(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def student_login_required(function):
    def wrapper(request):
        if not is_student(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


####################################################
#           Report Generators                      #
####################################################


def mark_report_subject(student, subject):
    """
    Returns a list of dictionary containing the details of test and marks obtained by student for given subject
    """
    test_list = Test.objects.filter(subject=subject)
    mark_details = []
    for test in test_list:
        mark = Marks.objects.get(student=student, test=test)
        # ----------------------------------------------
        test_details = {
            'test_name': test.name,
            'date': test.date,
            'subject': test.subject.name,
            'marks': mark.marks,
            'total_marks': test.total_marks
        }
        # ----------------------------------------------
        mark_details.append(test_details)
    return mark_details


def get_attendance_report_from_to(student, from_date, to_date):
    """
    returns a dictionary containing the details of the student's attendance in given time range
    """
    attendance_list = Attendance.objects.filter(student=student, date__gte=from_date, date__lte=to_date)
    present = 0
    absent = 0
    total = attendance_list.count()
    for att in attendance_list:
        if att.is_present:
            present += 1
        else:
            absent += 1
    try:
        percentage_present = (float(present) / total) * 100
    except ZeroDivisionError:
        percentage_present = 0
    return {
        'present': present,
        'absent': absent,
        'total': total,
        'percentage_present': '{0:.2f}'.format(percentage_present)
    }


def get_attendance_complete(student):
    """
        returns a dictionary containing the details of the student's attendance so far
        """
    attendance_list = Attendance.objects.filter(student=student)
    present = 0
    absent = 0
    total = attendance_list.count()
    for att in attendance_list:
        if att.is_present:
            present += 1
        else:
            absent += 1
    try:
        percentage_present = (float(present) / total) * 100
    except ZeroDivisionError:
        percentage_present = 0.0
    return {
        'student': student,
        'present': present,
        'absent': absent,
        'total': total,
        'percentage_present': '{0:.2f}'.format(percentage_present,)
    }
