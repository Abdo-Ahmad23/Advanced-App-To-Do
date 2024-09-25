from email.policy import default

from odoo import fields, models,api
from datetime import datetime

class Task(models.Model):
    _name='task'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name=fields.Char(string='Task Name')
    assign_to=fields.Many2one('employee',string='Assign To',tracking=1,readonly=0)
    description=fields.Text(string='Description')
    due_date=fields.Date(string='Due Date',tracking=1)
    active=fields.Boolean(default=True)
    state=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ],default='new')
    project_id = fields.Many2one('project', string='Project' ,ondelete='cascade')
    project_name=fields.Char(compute="set_project_name_for_task",readonly=1)
    project_state=fields.Selection([
        ('new','Draft'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ] ,default='new',compute="set_project_name_for_task")
    subtask_ids = fields.One2many('subtask', 'task_id', string='Subtasks',ondelete='cascade')
    seq=fields.Char(default='New',readonly=1)
    completed_task_count = fields.Integer(string='Completed Task Count', compute='_compute_completed_task_count')

    # change in 18 - 9 - 2024

    start_time = fields.Datetime('Start Time', readonly=True,store=1)
    end_time = fields.Datetime('End Time', readonly=True,)
    total_time = fields.Char('Total Time (in hours)', compute='_compute_total_time')

    @api.onchange('subtask_ids')
    def _onchange_task_ids(self):
        for task in self:

            if ((any(subtask.state == 'new' for subtask in task.subtask_ids) or
                any(subtask.state == 'in_progress' for subtask in task.subtask_ids)) and
                    (any(subtask.state == 'in_progress' for subtask in task.subtask_ids) or
                     any(subtask.state == 'completed' for subtask in task.subtask_ids))):
                task.state = 'in_progress'
                if not task.start_time:
                    task.start_time = fields.Datetime.now()
            elif all(subtask.state == 'new' for subtask in task.subtask_ids):
                task.state = 'new'
            elif all(subtask.state == 'in_progress' for subtask in task.subtask_ids):
                task.state = 'in_progress'
                if not task.start_time:
                    task.start_time = fields.Datetime.now()
            elif all(subtask.state == 'completed' for subtask in task.subtask_ids):
                task.state = 'completed'

                task.end_time=fields.Datetime.now()





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

    @api.model
    def create(self, vals):
        # Create the record and get its ID
        record = super(Task, self).create(vals)
        # Set the sequence based on the record's ID
        record.seq = 'PR' + str(record.id).zfill(5)
        return record
    # Method to print all tasks for the related project
    @api.depends('assign_to','name')
    def set_project_name_for_task(self):
        # Loop through each task (self refers to the current recordset)
        for task in self:
            # Search for projects linked to this task
            projects = self.env['project'].search([])
            project_found = False  # Flag to check if project is found

            for project in projects:
                for line in project.task_line_ids:
                    # Check if the task name matches
                    if project.name and project.project_state and task.name == line.task_id.name:
                        task.project_name = project.name
                        task.project_state = project.project_state
                        project_found = True  # Mark as found
                        break  # No need to continue searching once we found a project

            # If no project is found, you can set default values or leave them as is
            if not project_found:
                task.project_name = 'No Project'
                task.project_state = 'new'  # or some default value

    @api.depends('state')
    def _compute_completed_task_count(self):
        for task in self:
            task.completed_task_count = self.search_count([('state', '=', 'completed')])
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
    task_id = fields.Many2one('task' ,ondelete='cascade')


