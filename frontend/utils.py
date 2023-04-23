from frontend.models import *


def get_skill_table():
    skills = Skill.objects.all().order_by('order')
    skills_1 = []
    skills_2 = []

    count = 0
    for elem in skills:
        count += 1
        if count == 1:
            skills_1.append(elem)
        elif count == 2:
            skills_2.append(elem)
            count = 0

    return skills_1, skills_2
