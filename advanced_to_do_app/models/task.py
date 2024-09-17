from odoo import fields, models

class Task(models.Model):
    _name='task'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Task Name')
    assign_to=fields.Many2one('employee',string='Assign To',tracking=1)
    description=fields.Text(string='Description')
    due_date=fields.Date(string='Due Date',tracking=1)
    state=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ],default='new')
    project_id = fields.Many2one('project', string='Project')
    subtask_ids = fields.One2many('subtask', 'task_id', string='Subtasks')
    active=fields.Boolean()
    def action_new(self):
        for rec in self:
            rec.state='new'
    
    def action_in_progress(self):
        for rec in self:
            rec.state='in_progress'

    def action_completed(self):
        for rec in self: 
            rec.state='completed'


class SubTask(models.Model):
    _name = 'subtask'
    _description = 'Subtask'

    name = fields.Char(string='SubTask Name')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='new')
    task_id = fields.Many2one('task' )


