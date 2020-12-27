"""
作用：用于把具体数据写入到 excel 中

写入逻辑：读取模板 excel 前两行的数据，复制粘贴到欲生成的 excel 中，之后每写入一行，就会使行标加1，让下一次写入的时候能够写在下一行，
最后使用 save 方法，并参入生成的路径，输出文件(这样是为了不破坏模板文件)
"""
from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet import worksheet

from model import PowerAndResponsibility


class PARExcelWriter:
    workbook: 'Workbook'
    current_row_index: 'int > 0' = 1
    template_xlsx: 'str' = None

    def __init__(
            self,
            template_path: 'str',
    ):
        """
        :keyword:

        :param template_path: 文件路径
        :param mode: 文件写入模式: 'w' 直接写在模板文件中写， 'cw' copy and write copy 模板文件的前两行，然后在第三行开始写入
        """
        self.template_xlsx = template_path
        self.current_row_index = 1
        self.workbook = Workbook()
        self._init_workbook()

    def _init_workbook(self):
        """
        把模板的前两行给复制到产出 excel 文件中
        :return:
        """
        curr_wb = load_workbook(self.template_xlsx)
        curr_ws = curr_wb.active

        ws = self.workbook.active
        for row_index in range(1, 3):
            for col_index in range(1, 57):
                ws.cell(row_index, col_index, curr_ws.cell(row_index, col_index).value)
        self.current_row_index += 2
        curr_wb.close()

    def write_row(self, data: 'PowerAndResponsibility'):
        work_sheet = self.workbook.active

        assert isinstance(work_sheet, worksheet.Worksheet)
        assert isinstance(self.current_row_index, int)
        assert isinstance(data, PowerAndResponsibility)
        # 标题
        work_sheet[f'A{self.current_row_index}'] = data.libNum or ''
        work_sheet[f'B{self.current_row_index}'] = data.catalogId or ''
        work_sheet[f'C{self.current_row_index}'] = data.title or ''
        work_sheet[f'D{self.current_row_index}'] = data.issuedNum or ''
        # 发布者
        work_sheet[f'E{self.current_row_index}'] = data.publisher or ''
        # 发布日期
        work_sheet[f'F{self.current_row_index}'] = data.publishDate or datetime.now().strftime('%d/%m/%Y')
        work_sheet[f'G{self.current_row_index}'] = data.source or '广东省政务服务网'
        work_sheet[f'H{self.current_row_index}'] = data.belongDomain or ''
        work_sheet[f'I{self.current_row_index}'] = data.genre or '清单'
        work_sheet[f'J{self.current_row_index}'] = data.classify or ''
        work_sheet[f'L{self.current_row_index}'] = data.originalAddress or ''
        work_sheet[f'M{self.current_row_index}'] = data.htmlContent or ''
        work_sheet[f'N{self.current_row_index}'] = data.creatorName or ''
        self.current_row_index += 1

    def save(self, out_xlsx: 'str'):
        self.workbook.save(out_xlsx)
