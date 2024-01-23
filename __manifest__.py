# __manifest__.py
{
    'name': 'Sincronizacion de odoo 14',
    'version': '1.0',
    'author': 'Abraham Bronstein',
    'category': 'Tools',
    'depends': ['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/sync_model.xml',
        'views/res_config_settings_views.xml',
        'views/ir_cron.xml',
    ],
    'application': True,
    'installable': True,
}
