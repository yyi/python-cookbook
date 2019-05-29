import openpyxl
import re

wb = openpyxl.load_workbook('F:\\document\\方正项目周报（2019-3-18至2019-3-22）.xlsx')
all_sheets = wb.get_sheet_names()
print(all_sheets)
for i in range(len(all_sheets)):
    sheet = wb.get_sheet_by_name(all_sheets[i])
    print(sheet.title + ': max_row: ' + str(sheet.max_row) + '  max_column: ' + str(sheet.max_column))
    for i in range(len(all_sheets)):
        sheet = wb.get_sheet_by_name(all_sheets[i])
        print(sheet.title + ': max_row: ' + str(sheet.max_row) + '  max_column: ' + str(sheet.max_column))

        for column in sheet.iter_cols():
            for cell2 in column:
                if cell2.value is not None:
                    #  print(cell2.value)
                    info2 = cell2.value.find('支撑人员')
                    if info2 == 0:
                        print(cell2.value)
                        row, col = cell2.row, cell2.column
        print(row, col)
        while row < sheet.max_row:
            row = row + 1
            if sheet.cell(row, col).value:
                print(sheet.cell(row, col).value + ":" + re.sub(r"\n[\s| ]*\n", '\n', sheet.cell(row, col + 2).value))
