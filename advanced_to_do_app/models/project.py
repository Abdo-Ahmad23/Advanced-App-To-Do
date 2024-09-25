from email.policy import default

from odoo import fields,models,api

from odoo.exceptions import ValidationError

from datetime import datetime


class Project(models.Model):
    _name='project'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Project Name')
    dead_line=fields.Date(string='Dead Line')
    project_manager_id=fields.Many2one('manager',ondelete='cascade')
    task_line_ids = fields.One2many('project.task.line', 'project_id', string='Tasks',ondelete='cascade')
    # New computed field for counting task lines
    task_line_count = fields.Integer(string='Task Line Count', compute='_compute_task_line_count')
    seq=fields.Char(default='New',readonly=1)
    start_time = fields.Datetime('Start Time', readonly=True)
    end_time = fields.Datetime('End Time', readonly=True)
    total_time = fields.Char('Total Time (in hours)', compute='_compute_total_time')

    @api.depends('task_line_ids')
    def _compute_task_line_count(self):
        for project in self:
            project.task_line_count = len(project.task_line_ids)

    project_state=fields.Selection([
        ('new','Draft'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ] ,default='new')
    def action_new(self):
        for rec in self:
            rec.project_state='new'

    def action_in_progress(self):
        for rec in self:
            rec.project_state='in_progress'
    
    def action_completed(self):
        ok=1
        for rec in self:
            
            for rec2 in rec.task_line_ids:
                if rec2.state!='completed':
                    ok=0
        if ok:
            rec.project_state='completed'
        else:
            raise ValidationError('This project is not enough completed !')

    @api.model
    def create(self, vals):
        # Create the record and get its ID
        record = super(Project, self).create(vals)
        # Set the sequence based on the record's ID
        record.seq = 'PR' + str(record.id).zfill(5)
        return record


    @api.onchange('task_line_ids')
    def _onchange_task_ids(self):
        for project in self:
            if any(task.state == 'in_progress' for task in project.task_line_ids):
                project.project_state = 'in_progress'
                if not project.start_time:
                    project.start_time = fields.Datetime.now()
            elif all(task.state == 'new' for task in project.task_line_ids):
                project.project_state = 'new'
                project.start_time=False
            elif all(task.state == 'in_progress' for task in project.task_line_ids):
                project.project_state = 'in_progress'
                if not project.start_time:
                    project.start_time = fields.Datetime.now()
            elif all(task.state == 'completed' for task in project.task_line_ids):
                project.project_state = 'completed'

                project.end_time=fields.Datetime.now()


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
        if 'project_state' in vals and vals['project_state'] == 'in_progress':
            vals['start_time'] = fields.Datetime.now()

        # Check if the state is changed to 'completed'
        if 'project_state' in vals and vals['project_state'] == 'completed':
            vals['end_time'] = fields.Datetime.now()

        return super(Project, self).write(vals)




