# Odoo 14 to 17 Synchronization Model

## Overview

This project implements a synchronization model that allows for data synchronization between odoo 14 to odoo 17.

## How to Use

To use this synchronization model, follow these steps:

1. Zip the whole folder in .zip format like `odoo14to17.zip`

## Models

The synchronization model consists of the following models:

- **res_config_settings**: Represents the general settings configuration for this module, you can setup the parameters to communicate between XMLRPC and the syncronization intervals
- **sync_model**: Represents the logging about the syncronization events, the date and their log

- you can setup the model of syncronization by modifyng the line `33` of the file sync_model.py
  `models_to_update = ['product.category','product.product']` actually you can add more items to the array to try to sync new models.

## Views

The synchronization model provides the following views to interact with the data:

- **ir_cron**: It registers the Scheduled Action by default for the model
- **menu**: Provides the Application shorcut on the odoo menu
- **res_config_settings_views**: Provides the General settings UI for the configuration
- **sync_model**: provides the basic model for create a new syncronization with the Sync button

## Security

To ensure the security of the synchronized logs, the synchronization model implements the file `security/ir.model.access.csv` it can handle the permissions for the model and you can override it to avoid users deleting the logs
