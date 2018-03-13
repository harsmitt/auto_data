from DataExtraction.common_files.utils import *
from DataExtraction.common_files.all_regex import *
from DataExtraction.common_files.basic_functions import *
notes_key =['net sales', 'cost of sales','selling, general and administrative expenses','interest expense', 'other (income) expense, net']



def get_notes_data(**kwargs):
    import copy
    # import pdb;pdb.set_trace()
    date_obj = []
    new_key_dict = OrderedDict()
    old_data_dict = copy.deepcopy(kwargs['page_data'])
    notes_sec_start=False

    sec_name = list(kwargs['notes_sec'].keys())
    for sec in sec_name:

        start= kwargs['notes_sec'][sec].split('-')[0]#list(kwargs['notes_sec'].values())[0].split('-')[0]
        end = kwargs['notes_sec'][sec].split('-')[1]#list(kwargs['notes_sec'].values())[0].split('-')[-1]

        total_notes = int(end) - int(start)
        for notes in range(int(start) - 1, int(end) + 5):
            print (notes)
            # import pdb;pdb.set_trace()
            data = get_page_content(seprator='@@', page=notes, path=kwargs['path'], file=kwargs['file'])
            keys = list(kwargs['page_data'].keys())
            if any(i in get_alpha(sec,pnl=True) for i in data) and not notes_sec_start:
                notes_sec_start = True
                for key in keys:
                    r1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$' % (key)
                    r2 = '%s[ ,A-Za-z0-9.-]*$' % (key)
                    re_obj = re.compile(r1, re.I)
                    re_obj2 = re.compile(r2, re.I)
                    for line in data:
                        if re_obj.match(line) or re_obj2.match(line):
                            print ("match kr gya")

            elif notes_sec_start:
                date_obj = []
                new_key_dict = OrderedDict()
                for key in keys:
                    if key in notes_key:
                        r1 = notes_re1 % (key)
                        r2 = notes_re2 % (key)
                        re_obj = re.compile(r1, re.I)
                        re_obj2 = re.compile(r2, re.I)
                        if any(re_obj2.match(line) for line_num, line in enumerate(data)):
                            key_line_num = [line_num for line_num, line in enumerate(data) if re_obj2.match(line)]
                            for num, line in enumerate(data[key_line_num[0]:key_line_num[0]+5]):
                                print (line)
                                # import pdb;
                                # pdb.set_trace()
                                if kwargs['pdf_type'] =='year':
                                    date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                                         year_end=kwargs['year_end'],data=data,
                                                                     date_obj=date_obj,
                                                                     date_line=0,
                                                                     l_num=num)
                                else:
                                    next_line = data[num+1] if len(data) > num+1 else ''
                                    date_obj, date_line = check_date_obj(pdf_type=kwargs['pdf_type'], line=line,
                                                                         year_end=kwargs['year_end'],data=data,
                                                                         date_obj=date_obj,
                                                                         date_line=0,l_num=num)
                            if date_obj == kwargs['date_obj']:
                                for num, line in enumerate(data[key_line_num[0]+date_line-1:]):
                                    if line.split()[0].split('-')[0].istitle() and not num_there(line):
                                        if line.lower() in kwargs['page_data']:
                                            pass
                                        elif alpha_there(line) and not num_there(line):
                                            # new_key = get_aplha(word)
                                            new_key_dict[line.strip().lower()] = OrderedDict()

                                        elif new_key_dict and num_there(line) and not alpha_there(line):
                                            values = list(filter(lambda name: num_there(name), line.split()))
                                            new = list(
                                                map(lambda num: get_digit(num),
                                                    list(filter(lambda x: num_there(x), values))))

                                            dict1 = list(zip(date_obj, new))
                                            for d1 in new_key_dict:
                                                for key in new_key_dict[d1]:
                                                    if new_key_dict[d1][key] in [[], {}]:
                                                        new_key_dict[d1][key] = dict1
                                        elif new_key_dict and alpha_there(line) and not check_datetime(line.split()[0]):
                                            new_key = get_alpha(line,pnl=True)
                                            # old_dict = new_key_dict[list(new_key_dict.keys())[-1]]
                                            if new_key_dict[list(new_key_dict.keys())[-1]] in [[], {}]:
                                                    new_key_dict[list(new_key_dict.keys())[-1]] = OrderedDict({new_key: OrderedDict()})

                                    elif line.split()[0].split('-')[0].istitle() and len(re.split('  +', line)) > 1:
                                        values = re.split('  +', line)
                                        new_key = values[0]
                                        val = values[1].split() if len(values) == 2  else values[1:]
                                        new_key = new_key.strip().lower()
                                        if new_key not in keys:
                                            if 'total' not in new_key:
                                                new = list(
                                                    map(lambda num: str(get_digit(num)),
                                                        list(filter(lambda x: num_there(x), val))))
                                                if kwargs['page_data'][key] != list(zip(date_obj, new)):
                                                    new_key_dict[new_key] = list(zip(date_obj, new))
                                                else:
                                                    old_data_dict.update(new_key_dict)
                                                    break;

                                            elif new_key.split()[0].lower() == 'total':
                                                new = list(
                                                    map(lambda num: get_digit(num),
                                                        list(filter(lambda x: num_there(x), val))))
                                                if kwargs['page_data'][key] != list(zip(date_obj, new)):
                                                    new_key_dict[new_key] = list(zip(date_obj, new))

                                                old_data_dict.update(new_key_dict)
                                                break;
                                        elif (new_key == key):
                                            old_data_dict.update(new_key_dict)
                                            break;

            else:
                print ("different page")
    # import pdb;pdb.set_trace()
    return old_data_dict

