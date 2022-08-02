# -*- coding: utf-8 -*-

from babel.dates import format_datetime, format_date
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class HdTeam(models.Model):
    _name = 'hd.team'
    _inherit = ['mail.thread' ,'mail.activity.mixin']



    name = fields.Char(string="Name",tracking=True)
    team_leader = fields.Many2one('res.users',string="Team Leader")
