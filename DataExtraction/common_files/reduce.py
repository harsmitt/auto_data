def save_data_p2(**kwargs):
    for i, j in enumerate(kwargs['pdf_obj']):
        print(kwargs['comp']+ '________________' + str(j))
        yq_key = valid_yq_name(j[0], kwargs['year_end'], pdf_type=kwargs['pdf_type'], p_type=kwargs['p_type'])
        if yq_key:
            if 'section' not in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj']:
                sec_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = kwargs['model'].objects.filter(gbc_name__company_name=kwargs['c_name'],
                                                         section__item=sec_item,
                                                         subsection_id=None
                                                         )
            elif 'section' in kwargs['d_obj'] and 'subsection' not in kwargs['d_obj']:
                sub_item = kwargs['d_obj']['item'].split('##')[-1]
                gbc_obj = kwargs['model'].objects.filter(gbc_name__company_name=kwargs['c_name'],
                                                         subsection__item=sub_item)
            else:
                gbc_obj = kwargs['model'].objects.filter(gbc_name__company_name=kwargs['c_name'],
                                                         section_id=kwargs['d_obj']['subsection__section'],
                                                         subsection_id=kwargs['d_obj']['subsection'],
                                                         s2section__item=kwargs['d_obj']['item'])

            if gbc_obj and kwargs['type'] == 'synonym':
                get_id = yq_key + '_id'
                val_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                description = val_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if val_obj[
                    0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                if kwargs['comp'] == 'total assets':
                    old_obj = kwargs['model'].objects.filter(gbc_name__company_name=kwargs['c_name'], section__id=1,
                                                             subsection_id=None)
                    old_y_obj = quarter_data.objects.filter(id__in=old_obj.values_list(get_id, flat=True))
                    new_val = str(int(j[1]) - int(old_y_obj[0].q1))
                    val_dict = {'q1': new_val}
                else:
                    val_dict = {'q1': ('0' if str(j[1]) in ['-', 'â','—'] else str(j[1])),
                                'description': description} if not 'insert' in kwargs else {'description': description}
                val_obj.update(**val_dict)
            elif gbc_obj and kwargs['type'] == 'breakdown':
                get_id = yq_key + '_id'
                val_obj = quarter_data.objects.filter(id__in=gbc_obj.values_list(get_id, flat=True))
                if val_obj:
                    if kwargs['comp'] not in val_obj[0].description.split(','):
                        if '(' in str(j[1]) or '(' in val_obj[0].q1:
                            i2 = int(str(j[1]).replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            i1 = int(val_obj[0].q1.replace(',', '').replace('(', '-').replace(')', '').replace('$', ''))
                            val = i1 + i2
                            val = abs(val) if val > 0 else '(' + str(abs(val)) + ')'
                        else:
                            val = int(val_obj[0].q1.replace(',', '')) + int(
                                ('0' if str(j[1]) in ['-', 'â','—'] else str(j[1])).replace(',', ''))
                        description = val_obj[0].description + '##' + kwargs['comp'] + '(' + str(j[1]) + ')' if val_obj[
                            0].description else kwargs['comp'] + '(' + str(j[1]) + ')'
                        val_dict = {'q1': val, 'description': description} if not 'insert' in kwargs else {
                            'description': description}
                        val_obj.update(**val_dict)
                    else:
                        pass