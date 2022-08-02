# -*- coding: utf-8 -*-

from babel.dates import format_datetime, format_date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from random import randint



class HdTicket(models.Model):
    _name = 'hd.ticket'
    _inherit = ['mail.thread' ,'mail.activity.mixin']
    _rec_name = 'name' 



    name = fields.Char(string="Name",tracking=True)
    sequence = fields.Char(readonly=True)
    hd_team = fields.Many2one('hd.team',string="Team",tracking=True)
    description = fields.Html(required=True)
    assigned_to = fields.Many2one('res.users',string="Assigned to",tracking=True,default=lambda self: self.env.user)
    priority_type = fields.Selection([('low','Low'),('medium','Medium'),('higher','Higher')],default= 'low',copy=False,tracking=True)
    customer = fields.Many2one('res.partner',string="Customer",tracking=True)
    customer_email = fields.Char(related='customer.email',string="Email")
    customer_phone = fields.Char(related='customer.phone',string="Phone")
    tage = fields.Many2many('ticket.tags')
    hosting_type = fields.Selection([('on-premise','On-premise'),('cloud','Cloud')],default= 'on-premise',required=True,copy=False,tracking=True)
    server_url = fields.Char(string="Server URl")

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress','In Progress'),
        ('solved','Solved'),
        ('cancelled','Cancelled'),],default='new',tracking=True,string='Status')

    def button_new(self):
        for rec in self:
            rec.state = 'in_progress'

    def button_in_progress(self):
        for rec in self:
            rec.state = 'solved'

    def action_cancel(self):
        self.write({'state': 'cancelled'})
   
    def unlink(self):
        for order in self:
            if order.state not in ('new',):
                raise UserError(_('You can not delete record not in draft state.'))
        return super(HdTicket, self).unlink()

    @api.model
    def create(self, vals):
        code = vals['hd_team']
        team = self.env['hd.team'].browse(code)
        team_name = team.name

        seq = self.env['ir.sequence'].next_by_code('hd.ticket.seq') or 'New'
        vals['sequence'] = str(team_name) + '/' + seq
        return super(HdTicket, self).create(vals)





class TicketTags(models.Model):
    """ Tags of Ticket's """
    _name = "ticket.tags"
    _description = "Ticket Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]



class ResPartner(models.Model):
    _inherit = 'res.partner'


    count_ticket = fields.Float('Ticket', compute="_compute_ticket")

    @api.depends('self')
    def _compute_ticket(self):
        ticket = self.env['hd.ticket']
        for record in self:
            record.count_ticket = ticket.search_count([('customer', '=', self.id)])

    def get_tickets(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'view_mode': 'tree,form',
            'res_model': 'hd.ticket',
            'domain': [('customer', '=', self.id)],
            'context': "{'create': False}"
        }


class ResUsers(models.Model):
    _inherit = 'res.users'


    count_ticket = fields.Float('Ticket', compute="_compute_ticket")

    @api.depends('self')
    def _compute_ticket(self):
        ticket = self.env['hd.ticket']
        for record in self:
            record.count_ticket = ticket.search_count([('assigned_to', '=', self.id)])

    def get_users_tickets(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'view_mode': 'tree,form',
            'res_model': 'hd.ticket',
            'domain': [('assigned_to', '=', self.id)],
            'context': "{'create': False}"
        }
