# -*- coding: utf-8 -*-
from odoo import fields, models, _
import xlsxwriter
import base64
from io import BytesIO
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
from dateutil import relativedelta
from odoo.exceptions import UserError, AccessError, ValidationError
import time
from odoo.tools import float_round

class TicketsReportExcel(models.TransientModel):
    _name = 'tickets.team.excel'

    team_id = fields.Many2one('hd.team',string="Team",required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress','In Progress'),
        ('solved','Solved'),
        ('cancelled','Cancelled'),],string='Status')

    def print_report(self):

        for report in self:
            team_id = report.team_id
            state = report.state


            file_name = _('Ticket Per Team Report.xlsx')
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            sheet = workbook.add_worksheet('Ticket Per Team Report')
            header_format = workbook.add_format(
                {'bold': True, 'font_color': 'white', 'bg_color': '#808080', 'border': 4})
            header_format_sequence = workbook.add_format(
                {'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            format = workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            title_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#cbcbcb'})
            title_format.set_align('center')
            format.set_align('center')
            header_format_sequence.set_align('center')
            header_format.set_align('center')
            header_format.set_text_wrap()
            header_format.set_num_format('#,##0.00')
            sheet.set_row(5, 20)
            sheet.set_column('F:U', 20, )
            format.set_text_wrap()
            format.set_num_format('#,##0.00')
            format_details = workbook.add_format()
            format_details.set_num_format('#,##0.00')
            nex_format =  workbook.add_format({'bold': False, 'font_color': 'black', 'bg_color': 'white', 'border': 1})
            nex_format.set_num_format('#,##   ')

            sheet.merge_range('C2:F2', 'Ticket Per Team ', title_format)
            sheet.merge_range('C1:F1', '', title_format)
            sheet.merge_range('C3:F3', '', title_format)
            sheet.merge_range('C4:F4', '')

            row = 5
            col = 1


            sequence_id = 0
            tickets = self.env['hd.ticket'].search([('hd_team.id','=',team_id.id)])

            if team_id and not state:
                sheet.write(row, col, 'NO', header_format)
                sheet.set_column(row, col, 20)
                col += 1
                sheet.write(row, col, 'Ticket ID', header_format)
                sheet.set_column(row, col, 25)
                col += 1
                sheet.write(row, col, 'Name', header_format)
                sheet.set_column(row, col, 25)
                col += 1
                sheet.write(row, col, 'Priority', header_format)
                sheet.set_column(row, col, 25)
                col += 1
                sheet.write(row, col, 'State', header_format)
                sheet.set_column(row, col, 25)
                
                for rec in tickets:
                    ticket_id = rec.sequence
                    name = rec.name,
                    priority =  rec.priority_type
                    state =  rec.state

                    


                col = 1
                row += 1
                sequence_id += 1

                sheet.write(row, col, sequence_id, header_format_sequence)
                col += 1
                sheet.write(row, col, str(ticket_id), nex_format)
                col += 1
                sheet.write(row, col, str(name), nex_format)
                col += 1
                sheet.write(row, col, priority, nex_format)
                col += 1
                sheet.write(row, col, state, format)
                col += 1


            if team_id and state:
                sheet.write(row, col, 'NO', header_format)
                sheet.set_column(row, col, 20)
                col += 1
                sheet.write(row, col, 'Ticket ID', header_format)
                sheet.set_column(row, col, 25)
                col += 1
                sheet.write(row, col, 'Name', header_format)
                sheet.set_column(row, col, 25)
                col += 1
                sheet.write(row, col, 'Priority', header_format)
                sheet.set_column(row, col, 25)
                col += 1

                for rec in tickets.filtered(lambda x:x.state == state):
                    ticket_id = rec.sequence
                    name = rec.name,
                    priority =  rec.priority_type
                    state =  rec.state

                    


                col = 1
                row += 1
                sequence_id += 1

                sheet.write(row, col, sequence_id, header_format_sequence)
                col += 1
                sheet.write(row, col, str(ticket_id), nex_format)
                col += 1
                sheet.write(row, col, str(name), nex_format)
                col += 1
                sheet.write(row, col, priority, nex_format)
                col += 1



        workbook.close()
        file_download = base64.b64encode(fp.getvalue())
        fp.close()
        wizardmodel = self.env['tickets.team.wizard']
        res_id = wizardmodel.create({'name': file_name, 'file_download': file_download})
        return {
            'name': 'Files to Download',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tickets.team.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': res_id.id,
        }


class TicketsTeamWizard(models.TransientModel):
    _name = "tickets.team.wizard"

    name = fields.Char(string='Job Status', size=256, readonly=True)
    file_download = fields.Binary(string='Job Status', readonly=True)
