from user.models import *


def get_val_in_type(value, val_type):
    try:
        if val_type == 'str':
            value = str(value)
        elif val_type == 'int':
            value = int(value)
        elif val_type == 'float':
            value = float(value)
        elif val_type == 'bool':
            if str(value).lower() == 'true':
                value = True
            elif str(value).lower() == 'false':
                value = False
            elif str(value).lower() == 'none':
                value = None
            else:
                value = None
    except:
        value = None

    return value


def get_parameter(setting, val_type='str'):
    try:
        parameter = GeneralSetting.objects.get(setting=setting).parameter
    except:
        parameter = ''

    parameter = get_val_in_type(parameter, val_type)

    return parameter


def get_image(setting):
    try:
        image = ImageSetting.objects.get(setting=setting).file.url
        if not image:
            raise Exception
    except:
        image = settings.DEFAULT_PNG

    return image


def get_Skill_table():
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

