import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    username = fields.Char(string='Username', required=True, config_parameter='bdev.username')
    password = fields.Char(string='Password', required=True, config_parameter='bdev.password')
    url = fields.Char(string='URL', required=True, config_parameter='bdev.url')
    db = fields.Char(string='Database', required=True, config_parameter='bdev.db')
    sync_date = fields.Char(string='Set Sync Timestamp HH:mm', required=True, config_parameter='bdev.sync_date')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    interval_number = fields.Integer(string='Interval Number', default=1)
    interval_type = fields.Selection([('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], string='Interval Unit', default='days')
    active = fields.Boolean(string='Active', default=True)
    nextcall = fields.Datetime(string='Next Execution Date', default=fields.Datetime.now)
    numbercall = fields.Integer(string='Number of Calls', default=1)
    doall = fields.Boolean(string='Repeat Missed', default=False)
    priority = fields.Integer(string='Priority', default=5)


    #create a cron job at save of settings
    def execute(self):
        super(ResConfigSettings, self).execute()
        self.env['ir.cron'].sudo().create({
            'name': 'Sync',
            'model_id': self.env.ref('bdevsync.model_bdev_sync_model').id,
            'state': 'code',
            'code': 'model.sync()',
            'interval_number': self.interval_number,
            'interval_type': self.interval_type,
            'active': self.active,  
            'nextcall': self.nextcall,
            'numbercall': self.numbercall,
            'doall': self.doall,
            'priority': self.priority,
        })
        _logger.info('cron created!')
        return True