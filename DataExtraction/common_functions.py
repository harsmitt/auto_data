import os
import errno
import re

DEFAULT_DATA_PATH = '/home/administrator/DataAutomation/images/'


def num_there(s):
    if s in ['-','—']:
        return True

    return any(i.isdigit() for i in s)


def alpha_there(s):
    return any(i.isalpha() for i in s)


def get_digit(s):
    if s in ['-','—']:
        return s
    else:
        digit = ("".join(re.findall("[0-9()]+", s.lower().strip())))

        return int(digit.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))

def get_number(s):
    digit = ("".join(re.findall("[0-9]+", s.lower().strip())))

    return int(digit) if digit else 0

def get_aplha(s):
    str1 = s.split('(')[0]

    return (" ".join(re.findall("[a-zA-Z,]+", str1.lower().strip())))


def get_aplha_pnl(s):
    # str1 = s.split('(')[0]

    return (" ".join(re.findall("[a-zA-Z,]+", s.lower().strip())))


def make_directory(company_name):
    # Making the directory to save comapny filings
    path = os.path.join(DEFAULT_DATA_PATH, company_name.split()[0].decode('utf-8'))

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


from datetime import datetime, timedelta


def qtr_date():
    date_time = datetime.now() - timedelta(days=45)
    month = date_time.month
    year = date_time.year
    if month <= 3:
        year = year - 1
        qtr5 = 'December ' + str(year)
        qtr4 = 'September ' + str(year)
        qtr3 = 'June ' + str(year)
        qtr2 = 'March ' + str(year)
        qtr1 = 'December ' + str(year - 1)
    elif month > 3 and month <= 6:
        year1 = year - 1
        qtr5 = 'March ' + str(year)
        qtr4 = 'December ' + str(year1)
        qtr3 = 'September ' + str(year1)
        qtr2 = 'June ' + str(year1)
        qtr1 = 'March ' + str(year1)
    elif month > 6 and month <= 9:
        year1 = year - 1
        qtr5 = 'June ' + str(year)
        qtr4 = 'March ' + str(year)
        qtr3 = 'December ' + str(year1)
        qtr2 = 'September ' + str(year1)
        qtr1 = 'June ' + str(year1)
    elif month > 9 and month <= 12:
        year1 = year - 1
        qtr5 = 'September ' + str(year)
        qtr4 = 'June ' + str(year)
        qtr3 = 'March ' + str(year)
        qtr2 = 'December ' + str(year1)
        qtr1 = 'September ' + str(year1)
    qtr_dict = {'q1': qtr1, 'q2': qtr2, 'q3': qtr3, 'q4': qtr4, 'lrq': qtr5}
    return qtr_dict


def year_date():
    year = datetime.now().year
    year_dict = {'y1': year - 4, 'y2': year - 3, 'y3': year - 2, 'y4': year - 1}
    return year_dict


# get next and last month from a current month
def next_last_month(current_month):
    next_month = datetime.strptime(current_month, '%B %Y')
    if datetime.strptime(current_month, '%B %Y').month != 1:
        last_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=datetime.strptime(current_month, '%B %Y').month - 1)).strftime('%B %Y')
    else:
        month = 12
        year = datetime.strptime(current_month, '%B %Y').year - 1
        last_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=month, year=year)).strftime('%B %Y')
    if datetime.strptime(current_month, '%B %Y').month != 12:
        next_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=datetime.strptime(current_month, '%B %Y').month + 1)).strftime('%B %Y')
    else:
        month = 1
        year = datetime.strptime(current_month, '%B %Y').year + 1
        next_month = datetime.date(datetime.strptime(current_month, '%B %Y').replace(
            month=month, year=year)).strftime('%B %Y')
    return last_month, next_month


def get_list(s_data):
    data_list = []
    for i in s_data:
        for val in i:
            val_list = val.split('##')
            for v1 in val_list: data_list.append(v1)
    return data_list


from wand.display import display
from wand.image import Image


def save_image(path, page, company_name):
    import os
    path1 = path + str([int(page) - 1])
    make_directory(company_name)
    with Image(filename=path1) as img:
        # img.transform(resize="%dx%d>" % (width, height))
        img_path = os.path.join(DEFAULT_DATA_PATH, company_name.split()[0].decode('utf-8'))
        img_path = img_path + '/' + path.split('/')[-1].split('.')[0] + '.png'
        import os.path
        if not os.path.exists(img_path):
            img.save(filename=img_path)
    return img_path


def get_quarter_name(date_obj):
    quarter_val = ''
    qtr_dict = qtr_date()
    for key, val in qtr_dict.items():
        last_month, next_month = next_last_month(val)
        if date_obj == val or date_obj == last_month or date_obj == next_month:
            quarter_val = key
            break;
    return quarter_val


def get_year_name(date_obj):
    year_val = ''
    year_dict = year_date()
    for key, val in year_dict.items():
        if int(date_obj) == val:
            year_val = key
            break;
    return year_val


def get_year(date_obj, str1, date_val, require):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    if not len(get_year) == 2 and not date_obj and date_val == False:
        for i in str1.split():
            try:
                if not num_there(i):
                    d_obj = datetime.strptime(i, '%B')
                    if d_obj and type(d_obj) == datetime:
                        date_obj.append(i)
                else:
                    break;
            except:
                return date_obj, False, date_val
    else:
        if len(get_year) == 2:
            date_obj = get_year
            date_val = True
            require = True
    return date_obj, require, date_val


def get_date_obj(date_obj, str1, date_val, require):
    get_year = [i for i in str1.split() if len(i) == 4 and i.isdigit()]
    get_month = [i for i in str1.split() if not num_there(i)]
    try:
        if len(get_month) in [2, 0]:
            if not date_obj and not date_val and not get_year:
                date_obj = get_month
            else:
                month_year = zip(date_obj, get_year) if date_obj else zip(get_month, get_year)
                date_obj = []
                for r1 in month_year:
                    obj = r1[0] + ' ' + r1[1]
                    d_obj = datetime.strptime(obj, '%B %Y')
                    if type(d_obj) == datetime:
                        date_obj.append(obj)
                qtr_list = qtr_date().values()
                for obj in date_obj:
                    last_month, next_month = next_last_month(obj)
                    month_op = [obj, last_month, next_month]
                    if any(i in qtr_list for i in month_op):
                        date_val = True
                        require = True
                        break;
                    else:
                        date_val, require = False, False
    except:
        date_val, require = False, False

    return date_obj, require, date_val


def check_datetime(obj):
    try:
        if type(datetime.strptime(obj, '%B')) == datetime:
            return True
    except:
        try:
            if type(datetime.strptime(obj, '%Y')) == datetime:
                return True
        except:
            return False


def y_sorting(year_list):
    list1 = [int(i.split('.')[0]) for i in year_list]
    for loop1 in range(0, len(list1)):
        for i, j in enumerate(list1):
            if len(list1) > 1 and len(list1) != (i + 1):
                if list1[i] < list1[i + 1]:
                    temp = list1[i]
                    list1[i] = list1[i + 1]
                    list1[i + 1] = temp
    return list1


def q_sorting(q_list):
    name_list = [i.split('.pdf')[0].replace('_', ' ') for i in q_list]
    for loop in range(0, len(name_list)):
        for i, j in enumerate(name_list):
            if len(name_list) > 1 and len(name_list) != (i + 1):
                if datetime.strptime(name_list[i], '%B %Y') < datetime.strptime(name_list[i + 1], '%B %Y'):
                    temp = name_list[i]
                    name_list[i] = name_list[i + 1]
                    name_list[i + 1] = temp
    return name_list
    #
    # def get_queryset(self, request):
    #     import pdb;
    #     pdb.set_trace()
    #     qs = super(GBCADMIN, self).get_queryset(request)
    #     sec = Section.objects.all()
    #     for i in sec:
    #         sub_obj = SubSection.objects.filter(section=i)
    #         for sub in sub_obj:
    #             gbc_obj = GbcData.objects.filter(subsection=sub, section=i, gbc_name_id=request.GET['gbc_name'])
    #             if gbc_obj:
    #                 pass
    #             else:
    #                 gbc_dict = {'gbc_name_id': request.GET['gbc_name'], 'section': i,
    #
    #                             'q1': None, 'subsection': sub, 's2section': None,
    #                             'q2': None, 'q3': None, 'q4': None, 'y1': None, 'y2': None,
    #                             'y3': None, 'y4': None,
    #                             }
    #                 query1 = GbcData(**gbc_dict)
    #                 query1.save()
    #             s2_obj = S2Section.objects.filter(subsection=sub)
    #             if s2_obj:
    #                 for s2 in s2_obj:
    #                     gbc_obj = GbcData.objects.filter(subsection=sub, section=i, s2section=s2,
    #                                                      gbc_name_id=request.GET['gbc_name'])
    #                     if gbc_obj:
    #                         pass
    #                     else:
    #                         gbc_dict = {'gbc_name_id': request.GET['gbc_name'], 'section': i,
    #
    #                                     'q1': None, 'subsection': sub, 's2section': s2,
    #                                     'q2': None, 'q3': None, 'q4': None, 'y1': None, 'y2': None,
    #                                     'y3': None, 'y4': None,
    #                                     }
    #                         query1 = GbcData(**gbc_dict)
    #                         query1.save()
    #
    #     qs = qs.filter(section_id=1)
    #     return qs


from .models import *


def add_quarter(path, page, company_name):
    q_dict = {}
    qtr_dict = qtr_date()
    for k, v in qtr_dict.items():
        key_dict = {'description': '', 'quarter_date': v, 'q1': 0,
                    'pdf_page': page,
                    'pdf_image_path': path}
        query1 = quarter_data(**key_dict)
        query1.save()
        q_dict[k] = query1
    return q_dict


def add_year(path, page, c_name):
    y_dict = {}
    year_dict = year_date()
    for k, v in year_dict.items():
        key_dict = {'description': '', 'year_date': v, 'y1': 0,
                    'pdf_page': page,
                    'pdf_image_path': path}
        query1 = year_data(**key_dict)
        query1.save()
        y_dict[k] = query1
    return y_dict


def Create_blank_sheet(c_name, path, page):
    c_obj = CompanyList.objects.filter(company_name__icontains=c_name)
    if not c_obj:
        c_dict = {'company_name': c_name.decode('utf-8')}
        c_obj = CompanyList(**c_dict)
        c_obj.save()
    else:
        c_obj = c_obj[0]
    sec_obj = Section.objects.filter(i_related='Balance Sheet')

    img_path = save_image(path, page, c_name)
    for sec in sec_obj:
        exist = add_gbc(img_path, page, c_name, c_obj, sec)
        if not exist:
            sub_obj = SubSection.objects.filter(section=sec)
            for sub in sub_obj:
                x = add_gbc(img_path, page, c_name, c_obj, sec, sub_obj=sub)
                s2_obj = S2Section.objects.filter(subsection=sub)
                if s2_obj:
                    for s2 in s2_obj:
                        x = add_gbc(img_path, page, c_name, c_obj, sec, sub_obj=sub, s2_obj=s2)
        else:
            break;
    return img_path, c_obj.company_name


def Create_pnl(c_name, path, page):
    c_obj = CompanyList.objects.filter(company_name__icontains=c_name)
    if not c_obj:
        c_dict = {'company_name': c_name.decode('utf-8')}
        c_obj = CompanyList(**c_dict)
        c_obj.save()
    else:
        c_obj = c_obj[0]
    sec_obj = Section.objects.filter(i_related='Profit and Loss')

    img_path = save_image(path, page, c_name)
    for sec in sec_obj:
        exist = add_gbc(img_path, page, c_name, c_obj, sec)
        if not exist:
            sub_obj = SubSection.objects.filter(section=sec)
            for sub in sub_obj:
                x = add_gbc(img_path, page, c_name, c_obj, sec, sub_obj=sub)
                s2_obj = S2Section.objects.filter(subsection=sub)
                if s2_obj:
                    for s2 in s2_obj:
                        x = add_gbc(img_path, page, c_name, c_obj, sec, sub_obj=sub, s2_obj=s2)
        else:
            break;
    return img_path, c_obj.company_name


def add_gbc(img_path, page, c_name, c_obj, sec, sub_obj=None, s2_obj=None):
    q_dict = add_quarter(img_path, page, c_name)
    y_dict = add_year(img_path, page, c_name)
    gbc_obj = GbcData.objects.filter(subsection=sub_obj, section=sec, gbc_name=c_obj, s2section=s2_obj)

    if not gbc_obj:
        gbc_dict = {'gbc_name': c_obj, 'section': sec, 'q1': q_dict['q1'],
                    'q2': q_dict['q2'], 'q3': q_dict['q3'], 'q4': q_dict['q4'],
                    'lrq': q_dict['lrq'], 'y1': y_dict['y1'], 'y2': y_dict['y2'], 'y3': y_dict['y3'],
                    'y4': y_dict['y4'],
                    }

        if sub_obj and s2_obj:
            gbc_dict['subsection'] = sub_obj
            gbc_dict['s2section'] = s2_obj

        elif sub_obj and not s2_obj:
            gbc_dict['subsection'] = sub_obj

        query1 = GbcData(**gbc_dict)
        query1.save()
        return False

    return True

