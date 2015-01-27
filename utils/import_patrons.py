import django
django.setup()

from library.models import Student

def get_grade(numerical):
    if numerical == 'K':
        return 'gan'
    elif numerical == '01':
        return 'alef'
    elif numerical == '02':
        return 'bet'
    elif numerical == '03':
        return 'gimel'
    elif numerical == '04':
        return 'dalet'
    elif numerical == '05':
        return 'hay'

with open('patrons.txt') as f:
    num_cols = 0
    i = 0
    found = 0
    not_found = 0
    not_found_gan = 0
    not_found_no_grade = 0
    found_gan = 0
    for line in f:
        cols = line.split('\t')
        first_name = cols[2]
        grade = get_grade(cols[17])
        try:
            s = Student.objects.get(first_name=first_name, grade=grade)
        except:
            s = Student(first_name=first_name, grade=grade)
        
        s.bar_code=cols[0]
        s.last_name=cols[1]
        s.code=cols[4]
        s.type=cols[5]
        #s.report_to=cols[6]
        s.organization=cols[7]
        s.department=cols[8]
        s.address_1=cols[9]
        s.address_2=cols[10]
        s.city=cols[11]
        s.state=cols[12]
        s.zip=cols[13]
        s.phone=cols[15]
        s.email=cols[16]
        s.grade=cols[17]
        s.parent_info=cols[22]
        s.comments=cols[23]
        s.custom_field_1=cols[24]
        s.custom_field_2=cols[25]
        s.custom_field_3=cols[26]
        s.custom_field_4=cols[27]

        s.save()
