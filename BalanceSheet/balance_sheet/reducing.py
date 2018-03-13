def save_year_data(**kwargs):#obj_name,obj_val,obj_dict,type,c_name):
    print (kwargs['comp'])
    for i, j in enumerate(kwargs['pdf_obj']):
        y_key = get_year_name(j[0])
        if y_key:
            if 'section' not in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj'] :
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=kwargs['c_name'],section__item=kwargs['d_obj']['item'],
                                                 subsection_id=None
                                                 )
            elif 'section' in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj']:
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=kwargs['c_name'],section_id=kwargs['d_obj']['section'],
                                                 subsection__item=kwargs['d_obj']['item'])
            else:
                gbc_obj = GbcData.objects.filter(gbc_name__company_name=kwargs['c_name'],section_id=kwargs['d_obj']['subsection__section'],
                                                 subsection_id=kwargs['d_obj']['subsection'],s2section__item=kwargs['d_obj']['item'])

            if gbc_obj and kwargs['type']=='synonym':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if kwargs['comp'] =='total assets':
                    old_obj = GbcData.objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
                                           subsection_id=None)
                    old_y_obj = year_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(int(j[1]) - int(old_y_obj[0].y1))
                    y_dict = {'y1':new_val}
                else:
                    y_dict = {'y1':('0' if j[1] in ['-','—'] else j[1])}
                y_obj.update(**y_dict)

            elif gbc_obj and kwargs['type']=='breakdown':
                get_id = y_key + '_id'
                y_obj = year_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if y_obj:
                    if kwargs['comp'] not in y_obj[0].description.split(','):
                        if '(' in j[1] or '(' in y_obj[0].y1:
                            i2 = int(j[1].replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = int(y_obj[0].y1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            val = int(y_obj[0].y1.replace(',', ''))+int(('0' if j[1] in ['-','—'] else j[1]).replace(',', ''))
                        description = y_obj[0].description +'##'+kwargs['comp']+'('+ str(j[1])+')' if y_obj[0].description else kwargs['comp']+'('+ str(j[1])+')'
                        y_dict = {'y1': val,'description':description}
                        y_obj.update(**y_dict)
                    else:
                        pass
    return True
