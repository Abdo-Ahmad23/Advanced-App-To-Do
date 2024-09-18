from odoo import fields, models,api
from datetime import datetime

class Task(models.Model):
    _name='task'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Task Name')
    assign_to=fields.Many2one('employee',string='Assign To',tracking=1)
    description=fields.Text(string='Description')
    due_date=fields.Date(string='Due Date',tracking=1)
    active=fields.Boolean(default=True)
    state=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ],default='new')
    project_id = fields.Many2one('project', string='Project')
    subtask_ids = fields.One2many('subtask', 'task_id', string='Subtasks')
    # active=fields.Boolean()
    def action_new(self):
        for rec in self:
            rec.state='new'
    
    def action_in_progress(self):
        for rec in self:
            rec.state='in_progress'

    def action_completed(self):
        for rec in self: 
            rec.state='completed'

    # change in 18 - 9 - 2024

    start_time = fields.Datetime('Start Time', readonly=True)
    end_time = fields.Datetime('End Time', readonly=True)
    total_time = fields.Char('Total Time (in hours)', compute='_compute_total_time')


    @api.depends('end_time')
    def _compute_total_time(self):
        for record in self:
            if record.start_time and record.end_time:
                duration = record.end_time - record.start_time
                total_seconds = duration.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                record.total_time = f'{hours:02}:{minutes:02}:{seconds:02}'
            else:
                record.total_time = '00:00:00'

    def write(self, vals):
        # Check if the state is changed to 'in_progress'
        if 'state' in vals and vals['state'] == 'in_progress':
            vals['start_time'] = fields.Datetime.now()

        # Check if the state is changed to 'completed'
        if 'state' in vals and vals['state'] == 'completed':
            vals['end_time'] = fields.Datetime.now()

        return super(Task, self).write(vals)


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


