# coding=gb2312
import xlwt

def write(file, data, sheet_name='Sheet1', encoding='gb2312'):
    wb = xlwt.Workbook(encoding=encoding)
    sht = wb.add_sheet(sheet_name)
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            sht.write(r, c, cell)

    wb.save(file)


if __name__ == "__main__":
    _data = [
     [
      "a", "b", "3"], [4, 5, 6]]
    write("test.xls", _data, sheet_name="测试用例")
