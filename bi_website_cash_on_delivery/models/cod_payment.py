# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models, _
from eagle.addons.payment.models.payment_acquirer import ValidationError
from eagle.tools.float_utils import float_compare


class CODAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cod', 'Cash on Delivery')], default='transfer')


    #def cod_get_form_action_url(self):
     #   return '/cod/payment/feedback'
    def _get_providers(self):
        providers = super(CODAcquirer, self)._get_providers()
        providers.append(['cod', _('Cash on Delivery')])
        return providers

    def cod_get_form_action_url(self):
        return '/cod/payment/feedback'

    @api.multi
    def cod_compute_fees(self, amount, currency_id, country_id):
        """ Compute paypal fees.

            :param float amount: the amount to pay
            :param integer country_id: an ID of a res.country, or None. This is
                                       the customer's country, to be compared to
                                       the acquirer company country.
            :return float fees: computed fees
        """
        if not self.fees_active:
            return 0.0
        country = self.env['res.country'].browse(country_id)
        if country and self.company_id.country_id.id == country.id:
            #percentage = self.fees_dom_var
            fixed = self.delivery_fees
            print("======================if====================",fixed)
        else:
            #percentage = self.fees_int_var
            fixed = self.delivery_fees
            print("======================else====================",fixed)
        fees = fixed #(percentage / 100.0 * amount + fixed) / (1 - percentage / 100.0)
        return fees



    '''def cod_compute_fees(self, amount, currency_id, country_id):
        """ Compute paypal fees.

            :param float amount: the amount to pay
            :param integer country_id: an ID of a res.country, or None. This is
                                       the customer's country, to be compared to
                                       the acquirer company country.
            :return float fees: computed fees
        """
        acquirer = self.browse()

        if not acquirer.fees_active:
            return 0.0
        else:
            fixed = acquirer.delivery_fees
        fees = fixed
        return fees'''
        

class CODPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _cod_form_get_tx_from_data(self, data):
        reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
        tx = self.search([('reference', '=', reference)])

        if not tx or len(tx) > 1:
            error_msg = _('received data for reference %s') % (pprint.pformat(reference))
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        return tx
