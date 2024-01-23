import logging
import xmlrpc.client
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class SyncModel(models.Model):
    _name = 'bdev.sync.model'
    _description = 'Synchronization Data Model'

    status = fields.Text(string='status', Required=True)
    log = fields.Text(string='Log', multiline=True)
    

    def sync(self):
        log = 'Starting Odoo 14 Sync! '
        try:
            status = 'Incomplete'
            username = self.env['ir.config_parameter'].sudo().get_param('bdev.username')
            password = self.env['ir.config_parameter'].sudo().get_param('bdev.password')
            url = self.env['ir.config_parameter'].sudo().get_param('bdev.url')
            db = self.env['ir.config_parameter'].sudo().get_param('bdev.db')
            _logger.info('username: ' + username)
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            _logger.info(common.version())
            uid = common.authenticate(db, username, password, {})

            if uid:
                _logger.info("Successfully authenticated with the server.")
                log = log+"Successfully authenticated with the server. "
                models_xmlrpc_client = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                models_to_update = ['product.category','product.product']
                # List all product inventory
                for model_to_update in models_to_update:
                    models = models_xmlrpc_client.execute_kw(db, uid, password, model_to_update, 'search_read', [[]])
                    #get the first item
                    #_logger.info(models[0])
                    properties = []
                    for prop in models[0].keys():
                        properties.append(prop)
                    _logger.info('properties: ')
                    _logger.info(properties)

                    internal_properties = []
                    arbitrary = self.env[model_to_update]
                    fields = arbitrary._fields
                    for field in fields.keys():
                        internal_properties.append(field)
                    _logger.info('fields: ')
                    _logger.info(internal_properties)

                    

                    log + log + 'model_to_update: '+model_to_update+' '
                    # Add the products to the database
                    for model in models:
                        try:
                            log = log +str(model['name'])+' '
                            #delete properties that are not in the model
                            for prop in properties:
                                #if the prop value is array get the first value
                                if isinstance(model[prop], list):
                                    #verify the array length
                                    if len(model[prop])>0:
                                        model[prop] = model[prop][0]
                                if prop not in internal_properties:
                                    del model[prop]
                            #print the model
                            _logger.info("transformed model:")
                            _logger.info(model)
                            model_id = self.env[model_to_update].sudo().search([('name', '=', model['name'])])
                            if not model_id:
                                log = log +'model not found, creating new one'+' '
                                _logger.info(model)
                                model_id = self.env[model_to_update].sudo().create(model)
                                if model_id:
                                    log = log + str(model_id['name'])+' created '
                                else:
                                    log = log + str(model_id['name'])+' not created '
                            else:
                                log = log +'model found'+' '
                                _logger.info(model)
                                model_id = self.env[model_to_update].sudo().write(model)
                                if model_id:
                                    log = log + str(model['name'])+' updated '
                                else:
                                    log = log + str(model['name'])+' not updated '
                        except Exception as e:
                            if hasattr(e, 'message'):
                                log = log +e.message+' '
                            else:
                                _logger.info(e)
                                log = log +'ValueError'+' '
                            pass
                    status = 'Success'
            else:
                log = log+"Wrong credentials "
        except Exception as e:
            if hasattr(e, 'message'):
                log = log +e.message+' '
            else:
                _logger.info(e)
                log = log +'ValueError'+' '
            status = 'Error'
        self.log = log
        self.status = status
        pass


    