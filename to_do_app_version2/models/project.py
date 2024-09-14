from odoo import fields,models

from odoo.exceptions import ValidationError

class Project(models.Model):
    _name='project'


    name=fields.Char(string='Project Name')
    dead_line=fields.Date(string='Dead Line')
    project_manager_id=fields.Many2one('manager')
    task_line_ids = fields.One2many('project.task.line', 'project_id', string='Tasks')
    project_state=fields.Selection([
        ('new','New'),
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

        
    