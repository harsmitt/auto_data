# if [i for i in data if r1.search(i.decode('utf-8'))]:
#
#
#     for i in data:
#         i = i.decode('utf8')
#         if i and num_there(i) and not date_val:
#             date_obj, qtr_exists, date_val = get_date_obj(date_obj, i, date_val,
#                                                           qtr_exists) if file_type == 'qtr' \
#                 else get_year(date_obj, i, date_val, qtr_exists)
#             if qtr_exists == False and len(date_obj) > 1:
#                 qtr_exists = False
#                 break;
#         elif date_val == True:
#             word = i.strip().replace(':', '')
#             print (word)
#             if any(val in word.lower() for val in pass_list):
#                 pass
#             elif word.istitle() and len(word) < 100 and any(
#                     check_datetime(str1) for str1 in word.split()) == False:
#                 if word.lower() in data_dict:
#                         pass
#                 else:
#                     new_key = get_aplha(word)
#                     data_dict[new_key.lower()] = {}
#
#             elif len(word) > 100:
#                 values = re.split('  +', word)
#
#                 new_key = values[0] if len(values[0]) < 60 else values[0].split(',')[0]
#
#                 new_key = get_aplha(new_key)
#
#                 new_values = list(map(lambda x: x.replace(x, '-') if x in spl_char else x, values[1:]))
#                 data_dict[new_key] = \
#                     list(zip(date_obj, list(filter(lambda num: num_there(num), new_values))))
#                     # break;
#             elif len(word) > 100 and ('                       ') not in word:
#
#                 if list(filter(lambda x: True if str('total ' + str(x)) == word.lower() else False,
#                                total_comp)):
#                     pass
#                 else:
#                     word = word.split(',')[0]
#                     new_key = [word.replace(i, '-') for i in spl_char if i in word]
#                     new_key = "".join(new_key[0].split()) if new_key else word
#
#                     data_dict[list(data_dict.keys())[-1]] = {new_key: {}}