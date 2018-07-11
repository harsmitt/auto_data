from .tranform_data import *
import openpyxl
from django.http import HttpResponse
# from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from .inline_dump_functions import *


def FillBalanceSheet(sheet,data,row,date_list,loop_key,total_row,crosscheck):

    for loop in data:
        if data[loop]:
            ch=66
            #add sec key
            sf_row=row
            s_start_col=[]
            sheet = set_allign(sheet= sheet, row_no=row, value=loop)
            row+=1

            # s_start_col = row
            for sub in data[loop]:
                sheet,row ,s_start_col =subsec_write(data=sub,row_no=row,date_list=date_list,sheet=sheet,\
                                          s_start_col=s_start_col,loop_key=loop_key)

            s_end_col=row-1
            ch=66
            for d1 in date_list:
                str1=''
                for r1 in s_start_col:
                    str1 += (chr(ch)+str(r1))+','
                sheet[chr(ch) + str(sf_row)].value ='=SUM('+str1+')'
                sheet[chr(ch) + str(sf_row)].fill = format_excel.my_g1
                sheet[chr(ch) + str(sf_row)].border = format_excel.thin_border
                ch += 1
        elif 'total' in loop.lower():
            sheet = set_allign(sheet=sheet, row_no=row, value=loop)
            ch = 66
            for d1 in date_list:
                str1 = ''
                for r1 in total_row[:-1]:
                    str1 += (chr(ch) + str(r1)) + ','
                sheet[chr(ch) + str(row)].value = '=SUM(' + str1 + ')'
                sheet[chr(ch) + str(row)].fill = format_excel.my_g1
                sheet[chr(ch) + str(row)].border = format_excel.thin_border
                ch += 1
            crosscheck.append(row)
            print ("bvhvhghjjhjhhkhkkjkjjk "+str(crosscheck))
            row+=1
            total_row=[]
        else:
            sheet = set_allign(sheet=sheet, row_no=row, value=loop)
            ch = 66
            for d1 in date_list:
                str1 = ''
                str1 += (chr(ch) + str(crosscheck[0])) + '-' +(chr(ch) + str(crosscheck[1]))
                sheet[chr(ch) + str(row)].value = '=ROUND(' + str1 + ')'
                sheet[chr(ch) + str(row)].fill = format_excel.my_y2
                sheet[chr(ch) + str(row)].border = format_excel.thin_border
                ch += 1
            row += 1



    return sheet,row,total_row,crosscheck


def FillPNL(sheet,data,row,date_list,loop_key,total_form):

    for loop in data:
        if data[loop]:
            ch = 66
            # add sec key
            sf_row = row
            s_start_col = []
            sheet = set_allign(sheet=sheet, row_no=row, value=loop)
            row += 1

            # s_start_col = row
            for sub in data[loop]:
                total_form.append(row)
                sheet, row, s_start_col = subsec_write(data=sub, row_no=row, date_list=date_list, sheet=sheet, \
                                                       s_start_col=s_start_col, loop_key=loop_key)

            # s_end_col = row - 1
            ch = 66

            for d1 in date_list:
                str1 = ''
                for r1 in s_start_col:
                    str1 += (chr(ch) + str(r1)) + ','
                sheet[chr(ch) + str(sf_row)].value = '=SUM(' + str1 + ')'
                sheet[chr(ch) + str(sf_row)].fill = format_excel.my_g1
                sheet[chr(ch) + str(sf_row)].border = format_excel.thin_border
                ch += 1
        else:

            sheet = set_allign(sheet=sheet, row_no=row, value=loop)
            ch = 66
            for d1 in date_list:
                str1=''
                for r1 in total_form:
                    str1 += (chr(ch)+str(r1))+','
                sheet[chr(ch) + str(row)].value ='=SUM('+str1+')'
                sheet[chr(ch) + str(row)].fill = format_excel.my_g1
                sheet[chr(ch) + str(row)].border = format_excel.thin_border
                ch += 1
            row += 1
    return sheet, row, total_form

def download_dump(request):
    wb = openpyxl.Workbook()
    ws1 =  wb.active
    c_obj = CompanyList.objects.get(id = request.GET['c_id'])

    data_list, date_list, loop_key = get_data(req_type='bsheet', c_id=c_obj.id, section_type='Balance Sheet')
    ch=66
    row=1
    ws1['A' + str(row)].value = "Balance Sheet"
    for d1 in date_list:
        ws1[chr(ch) + str(row)].value = d1
        ch+=1
    row=3
    total_row =[]
    crosscheck =[]
    for data in data_list:
        total_row.append(row)
        ws1,row,total_row,crosscheck = FillBalanceSheet(ws1,data,row,date_list,loop_key,total_row,crosscheck)

    ws1.column_dimensions["A"].width = 30.0

#pnl
    ws2 = wb.create_sheet('PNL')
    data_list, date_list, loop_key = get_data(req_type='pnl', c_id=c_obj.id, section_type='Profit and Loss')
    ch = 66
    row = 1
    ws2['A' + str(row)].value = "Profit Loss"
    for d1 in date_list:
        ws2[chr(ch) + str(row)].value = d1
        ch += 1
    row = 3
    total_form =[]
    for data in data_list:
        ws2, row, total_form= FillPNL(ws2,data,row,date_list,loop_key,total_form)

    ws2.column_dimensions["A"].width = 30.0

    stream = save_virtual_workbook(wb)
    response = HttpResponse(stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % (c_obj.company_name)
    # wb.save(response)
    return response

    # Add this line