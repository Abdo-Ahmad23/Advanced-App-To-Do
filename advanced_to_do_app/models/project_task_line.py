from odoo import models, fields,api

from odoo.exceptions import ValidationError

class ProjectTaskLine(models.Model):
    _name = 'project.task.line'
    _description = 'Project Task Line'

    project_id = fields.Many2one('project', string='Project')
    task_id = fields.Many2one('task', string='Task', required=True)
    assign_to = fields.Many2one('employee', string='Assigned To', related='task_id.assign_to',readonly=False)
    description = fields.Text(string='Description', related='task_id.description',readonly=False)
    due_date = fields.Date(string='Due Date',related='task_id.due_date',readonly=False)
    # state = fields.Date(string='Due Date',related='task_id.due_date')
    state=fields.Selection(string='State',related='task_id.state',readonly=False)

    project_state=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed')
    ] ,default='new')
    name = fields.Char(string='Task Name', related='task_id.name', readonly=True)

    subtask_ids = fields.One2many('subtask', 'task_id', string='Subtasks')
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError('The name must be unique.')


