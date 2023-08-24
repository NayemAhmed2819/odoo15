from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

class OdooPlayground(models.Model):
    _name = "odoo.playground"
    _description = "Odoo Playground"

    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string="Code")
    result = fields.Text(string="Result")

    def action_clear(self):
        self.code=''
        self.result=''

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            if self.code:
                self.result = "Enter some codes to evaluate"
        except Exception as e:
            self.result.str(e)

    def orm_test(self):
        vals = self.env['hospital.patient'].fields_get()
        print(vals)