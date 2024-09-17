from odoo import fields,models

class Employee(models.Model):
    _name='employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Name')
    