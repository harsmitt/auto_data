def next_num_page(**kwargs):
    num=''
    if '-' in kwargs['data'][kwargs['line_num']].split()[int(kwargs['index'])]:
        num = kwargs['data'][kwargs['line_num']].split()[int(kwargs['index'])].split('-')[1]

    elif kwargs['data'][kwargs['line_num'] + 1].strip().split()[int(kwargs['index'])].isdigit():
        if not (kwargs['data'][kwargs['line_num'] + 1]).isdigit():
            num = str(int(kwargs['data'][kwargs['line_num'] + 1].strip().split()[int(kwargs['index'])]) +  kwargs['i'])

    elif len(kwargs['data']) - 1 > kwargs['line_num'] + 2 and\
            kwargs['data'][kwargs['line_num'] + 2].strip().split()[int(kwargs['index'])].isdigit():
        if not (kwargs['data'][kwargs['line_num'] + 2]).isdigit():
            num = str(int(kwargs['data'][kwargs['line_num'] + 2].strip().split()[int(kwargs['index'])]) +  kwargs['i'])

    return num