from odoo import fields,models

class Manager(models.Model):
    _name='manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Manager Name')
    