import statistics
from statistics import mode, mean
from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import UserError
import calendar


class TicketTeamWizard(models.TransientModel):
    _name = 'ticket.team.wizard'
    _description = 'Report showing all tickets for a particular team'

    team_id = fields.Many2one('hd.team',string="Team",required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress','In Progress'),
        ('solved','Solved'),
        ('cancelled','Cancelled'),],string='Status')

    

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form':{
            'team_id': self.team_id.id,
            'team_name': self.team_id.name,
            'state': self.state
            },}

        return self.env.ref('help_desk_team.ticket_team_report').report_action(self, data=data)


class PartsMovment(models.AbstractModel):
    _name = 'report.help_desk_team.ticket_team_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        team_id = data['form']['team_id']
        state = data['form']['state']
        team_name = data['form']['team_name']


        # docs= []
        ticket_list =[]

        tickets = self.env['hd.ticket'].search([('hd_team.id','=',team_id)])
        if team_id and not state:
            for rec in tickets:
                if rec.state == 'in_progress':
                    state = 'In Progress'

                ticket_list.append((0,0,{
                    # 'ticket_id': 1,
                    # 'name': str(rec.name),
                    # 'priority': rec.priority_type,
                    'state': state,
                    }))


        if team_id and state:
            for rec in tickets.filtered(lambda x:x.state == state):
                ticket_list.append((0,0,{
                    'ticket_id': rec.sequence,
                    'name': rec,
                    'priority': rec.priority_type,
                    }))
                print("::::::::::::::::m",ticket_list)




        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'docs':ticket_list,
            # 'ticket_list': ticket_list,
            'team_name':team_name

        }
