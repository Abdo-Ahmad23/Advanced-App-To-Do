from odoo import fields,models

class Manager(models.Model):
    _name='manager'


    name=fields.Char(string='Manager Name')
    