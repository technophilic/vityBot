import day_functions


def get_response(keyword, course, user):
    """
    process the response
    :param keyword: the keyword in the query
    :param course: course object
    :param user: student object
    :return: response  as string
    """

    if not course:
        if type(keyword) == list:
            if 'debarred' in keyword and type(keyword[1]) == str:  # if index 1 is a day of the week
                """
                queries relating to missing all classes in a day
                """

                day = keyword[1]
                li = list()  # list containing courses on that day

                for c in user.courses:
                    if day in c.days:
                        li.append(c)

                res_list = list()
                response = 'attendance in each courses: '

                for c in li:
                    no_of_classes = day_functions.classes_between(day, c)
                    s = c.attendance.miss_class_on(no_of_classes)
                    response += c.course_code + ' ' + str(s) + ', '

                    if c.attendance.isDebarred(s):
                        res_list.append(c)

                if len(res_list):
                    response += '\nyou will be debarred in '

                    for c in res_list:
                        response += c.course_code + ', '
                else:
                    response += '\nyou won\'t be debarred in any courses'

                return response

        li = list()

        if 'attendance' in keyword:
            for c in user.courses:
                li.append(str(c.course_code) + ' ' + str(c.attendance.attendance_percentage))

            return li

        elif 'debarred' in keyword:
            li = list()

            for c in user.courses:
                if c.attendance.isDebarred():
                    li.append(str(c.course_code) + ' ' + str(c.attendance.attendance_percentage))

            return li

    if type(keyword) == list:
        if 'attendance' in keyword:
            if len(keyword) == 1 or type(keyword[1]) == int:  # if index 1 is no. of classes
                n = keyword[1] if len(keyword) == 2 else 1
                s = course.attendance.attend_next_class(n)

                response = 'You will have an attendance of ' + '%d in ' % s + course.course_code

                return response

            elif type(keyword[1]) == str:  # if index 1 is a day of the week
                if keyword[1] is 'how':  # questions like 'how many more classes to attend'
                    cnt = 0

                    while course.attendance.isDebarred(course.attendance.miss_next_class(cnt)):
                        cnt += 1

                    if cnt:
                        response = 'You have to attend %d more class(es)' % cnt
                    else:
                        response = 'You are not debarred'
                    return response

                else:
                    day = keyword[1]
                    no_of_classes = day_functions.classes_between(day, course)
                    s = course.attendance.attend_next_class(no_of_classes)

                    response = 'You will have an attendance of ' + '%d in ' % s + course.course_code

                    return response

        elif 'debarred' in keyword:
            if len(keyword) == 1 or type(keyword[1]) == int:  # if index 1 is no. of classes
                n = keyword[1] if len(keyword) == 2 else 1
                s = course.attendance.miss_next_class(n)

                response = 'You will have an attendance of ' + '%d in ' % s + course.course_code

                if course.attendance.isDebarred(s):
                    response += '\nYou will be debarred'
                else:
                    response += '\nYou will not be debarred'

                return response

            elif type(keyword[1]) == str:  # if index 1 is a day of the week
                if keyword[1] is 'how':  # questions like 'how many more classes i can miss'
                    cnt = 0

                    while not course.attendance.isDebarred(course.attendance.miss_next_class(cnt)):
                        cnt += 1

                    cnt -= 1

                    if cnt:
                        response = 'You can miss %d class(es)' % cnt + ' in %s' % course.course_code
                    else:
                        response = 'You can\'t miss any class' + ' in %s' % course.course_code

                    return response

                else:
                    day = keyword[1]
                    no_of_classes = day_functions.classes_between(day, course)
                    s = course.attendance.miss_class_on(no_of_classes)

                    response = 'You will have an attendance of ' + '%d in ' % s + course.course_code

                    if course.attendance.isDebarred(s):
                        response += '\nYou will be debarred'
                    else:
                        response += '\nYou will not be debarred'

                    return response

    # if keyword is not a list
    if keyword is 'attendance':
        s = course.attendance.attendance_percentage

        response = 'Your attendance in ' + course.course_code + ' is %d' % s

        return response

    elif keyword is 'debarred':
        if course.attendance.isDebarred():
            response = 'You are debarred from the course ' + course.course_code
        else:
            response = 'You are not debarred from the course ' + course.course_code

        return response
