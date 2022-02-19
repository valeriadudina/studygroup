from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _name = 'product.template'

    aragavaio_type = fields.Selection([('none', 'None'), ('device', 'Device'), ('cable', 'Cable')],
                                      string='AragavaIO type',
                                      default='none')
    port_ids = fields.One2many('aragavaio.port', 'obj_id', string='Ports')
    manual_url = fields.Text(string='User manual URL')

    left_connector_type = fields.Selection(
        [('Male', 'Male'), ('Female', 'Female'), ('Male/Female', 'Male/Female')], string='Type', default='Male')
    left_connector_connector = fields.Many2one('aragavaio.connector', string='Connector')

    right_connector_type = fields.Selection(
        [('Male', 'Male'), ('Female', 'Female'), ('Male/Female', 'Male/Female')], string='Type', default='Male')
    right_connector_connector = fields.Many2one('aragavaio.connector', string='Connector')

    cable_length = fields.Float()


class Port(models.Model):
    _name = 'aragavaio.port'
    _description = 'Port model'

    name = fields.Char()
    direction = fields.Selection(
        [('in', 'Input'), ('out', 'Output'), ('bi', 'Bidirectional')], default='in')
    type = fields.Selection(
        [('Male', 'Male'), ('Female', 'Female'), ('Male/Female', 'Male/Female')], string='Type', default='Male')
    connector = fields.Many2one('aragavaio.connector', string='Connector')
    interface = fields.Many2one('aragavaio.interface', string='Interface')
    required = fields.Boolean(string='Required', default=False)
    amount = fields.Integer(string='Amount', default=1)

    obj_id = fields.Many2one('product.template', string='Device')


class PortType(models.Model):
    _name = 'aragavaio.porttype'
    _description = 'Port type'

    name = fields.Char()
    port_ids = fields.One2many('aragavaio.port', 'type', string='Ports')


class Connector(models.Model):
    _name = 'aragavaio.connector'
    _description = 'Connector'

    name = fields.Char()
    port_ids = fields.One2many('aragavaio.port', 'type', string='Ports')


class Interface(models.Model):
    _name = 'aragavaio.interface'
    _description = 'Interface'

    name = fields.Char()
    port_ids = fields.One2many('aragavaio.port', 'type', string='Ports')
