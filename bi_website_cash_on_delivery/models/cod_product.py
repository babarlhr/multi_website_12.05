# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from eagle import fields, models, api, _
from eagle.exceptions import UserError
from eagle import SUPERUSER_ID


class ProductCODFees(models.Model):
    _inherit = 'product.template'

    cod_available = fields.Boolean('Allow Cash on Delivery', default=True)
    delivery_fees = fields.Float('Delivery Fees', compute='update_fees')
    
    @api.multi
    @api.onchange('list_price')
    def min_max_calculation_product(self):
        cod_acq = self.env['ir.model.data'].xmlid_to_object('bi_website_cash_on_delivery.payment_acquirer_cod')
        for p in self:
            if p.list_price < cod_acq.cod_config.min_amt or p.list_price > cod_acq.cod_config.max_amt:
                p.update({'cod_available': False}) 
            elif p.list_price > cod_acq.cod_config.min_amt or p.list_price < cod_acq.cod_config.max_amt:
                p.update({'cod_available': True})
    
    def update_fees(self):
        cod_obj = self.env['ir.model.data'].xmlid_to_object('bi_website_cash_on_delivery.payment_acquirer_cod')
        if cod_obj.delivery_fees:
            for p in self:
                if p.cod_available == True:
                    p.update({'delivery_fees': cod_obj.delivery_fees})


'''class ProductProductCOD(models.Model):
    
    _inherit = 'product.product'
    
    @api.multi
    @api.onchange('list_price')
    def min_max_calculation_product(self):
        cod_acq = self.env['ir.model.data'].xmlid_to_object('bi_website_cash_on_delivery.payment_acquirer_cod')
        for p in self:
            if p.list_price < cod_acq.cod_config.min_amt or p.list_price > cod_acq.cod_config.max_amt:
                p.update({'cod_available': False}) 
            elif p.list_price > cod_acq.cod_config.min_amt or p.list_price < cod_acq.cod_config.max_amt:
                p.update({'cod_available': True})'''

            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
