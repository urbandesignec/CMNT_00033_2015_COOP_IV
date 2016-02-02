# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime


class LotPartner(models.Model):

    _name = 'lot.partner'
    _inherit = ['yearly.data']

    lot_number = fields.Integer('Lot number')

    _sql_constraints = [
        ('lot_uniq', 'unique (year_id,farm_id)',
         _('Error! Only one lot by year and company.'))
    ]


class Lot(models.Model):

    _name = 'lot'

    date = fields.Datetime('Date', required=True,
                           default=lambda a: datetime.now())
    user_id = fields.Many2one('res.users', 'User', required=True,
                              default=lambda self: self.env.user.id)
    farm_id = fields.Many2one('res.partner', 'Farm', required=True,
                              default=lambda self:
                              self.env.user.company_id.partner_id.id)
    lot_number = fields.Char('Lot number', compute='_get_lot_number')
    lot_details = fields.One2many('lot.detail', 'lot_id', 'Lot details')

    total_liters_sold = fields.Integer('Total liters sold')
    number_milking_cows = fields.Integer('Number of milking cows')
    liters_produced_per_day = fields.Integer('Liters produced per day')
    cs = fields.Integer('CS (X1000)')
    live_weight = fields.Integer('Live weight')
    collection_frequency = fields.Integer('Collection frequency')
    number_dry_cows = fields.Integer('Number of dry cows')
    liters_sold_per_day = fields.Integer('Liters sold per day')
    milk_price = fields.Float('Milk price(€ / 1000L)')
    liters_discarded_per_day = fields.Integer('Liters discarded per day')
    carriage_cost = fields.Integer('Carriage cost (€/month)')
    number_cubicle_lactation = fields.Integer('Nº cubicle lactation')
    mg = fields.Float('%MG')
    dry_cow_ration_cost = fields.Float('Dry cow ration cost(€/ cow and day)')
    liters_reused_day = fields.Integer('Liters reused/day')
    mp = fields.Float('%MP')
    carriage_cost_cow_day = fields.Float('Carriage cost (€/ cow and day)')

    @api.multi
    def _get_lot_number(self):
        for lot in self:
            lot_partner = self.env['lot.partner'].search(
                [('farm_id', '=', lot.farm_id.id),
                 ('year_id.date_start', '<=', lot.date),
                 ('year_id.date_stop', '>=', lot.date)])
            total_lots = lot_partner and lot_partner[0].lot_number or 0
            lot.lot_number = '%s/%s' % (len(lot.lot_details), total_lots)


class LotDetail(models.Model):

    _name = 'lot.detail'

    name = fields.Char('Name', required=True)
    description = fields.Char('Description', required=True)
    user_id = fields.Many2one('res.users', 'User', required=True,
                              default=lambda self: self.env.user.id)
    lot_id = fields.Many2one('lot', 'Lot')
    lot_contents = fields.One2many('lot.content', 'detail_id', 'Content')
    date = fields.Datetime('Date', required=True,
                           default=lambda a: datetime.now())
    rations_make_number = fields.Integer('Number of maked rations')
    surplus = fields.Float('Surplus (Kg)')
    cows_tank_number = fields.Integer('Cows tank number')
    liters_on_farm_consumption = fields.Integer('Liters on-farm consumption')
    kf_mf_carriage = fields.Float('kf MF carriage')
    cows_eat_number = fields.Integer('Cows eat number')
    tank_liters = fields.Float('Tank liters')
    retired_liters = fields.Float('Retired liters')
    number_cubicles_in_lot = fields.Integer('Number of cubicles in this lot')
    kg_plucking = fields.Integer('Plucking kg')

    kg_mf_ration_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    perc_ms_ration_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_ms_ration_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    imf_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_plucking_cow_day_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_unifed_kg_cow_day_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_plucking_kg_cow_day_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_total_kg_cow_day_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_liters_kg_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_corrected_liters_kg_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_enl_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_pb_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    real_production_deviation_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_mf_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_ms_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_cow_day_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_liter_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_corrected_milk_eur_liter_theo = fields.Float('', compute='_get_lot_calcs', readonly=True)

    kg_mf_ration_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    perc_ms_ration_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_ms_ration_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    imf_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_plucking_cow_day_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_unifed_kg_cow_day_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_plucking_kg_cow_day_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_total_kg_cow_day_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_liters_kg_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_corrected_liters_kg_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_enl_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_pb_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    real_production_deviation_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_mf_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_ms_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_cow_day_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_liter_real = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_corrected_milk_eur_liter_real = fields.Float('', compute='_get_lot_calcs', readonly=True)

    kg_mf_ration_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    perc_ms_ration_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_ms_ration_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    imf_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    kg_plucking_cow_day_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_unifed_kg_cow_day_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_plucking_kg_cow_day_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ims_total_kg_cow_day_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_liters_kg_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ic_corrected_liters_kg_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_enl_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_prediction_by_pb_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    real_production_deviation_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_mf_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_cost_eur_ton_ms_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_cow_day_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_eur_liter_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ration_carriage_cost_corrected_milk_eur_liter_anal = fields.Float('', compute='_get_lot_calcs', readonly=True)

    grs_fat_cow_day = fields.Float('', compute='_get_lot_calcs', readonly=True)
    grs_protein_cow_day = fields.Float('', compute='_get_lot_calcs', readonly=True)
    ingress_milk_cow_day = fields.Float('Ingress milk/milk cow and day', compute='_get_lot_calcs', readonly=True)
    feed_cost_cow_day = fields.Float('Feed cost cow day', compute='_get_lot_calcs', readonly=True)
    diff_ing_cost = fields.Float('Diff ing cost', compute='_get_lot_calcs', readonly=True)
    perc_feed_milk_ingress = fields.Float('Perc feed milk ingress', compute='_get_lot_calcs', readonly=True)
    perc_purchased_feed_milk_ingress = fields.Float('Perc purchased feed milk ingress', compute='_get_lot_calcs', readonly=True)
    perc_concentrated_milk_ingress = fields.Float('Perc concentrated milk ingress', compute='_get_lot_calcs', readonly=True)
    liters_produced_kg_concentrated_used = fields.Float('Liters produced kg concentrated used', compute='_get_lot_calcs', readonly=True)
    lot_threshold_point_slaughterhouse = fields.Float('Lot threshold point slaughterhouse', compute='_get_lot_calcs', readonly=True)
    lot_threshold_point_dry = fields.Float('Lot threshold point dry', compute='_get_lot_calcs', readonly=True)
    milk_cow_production = fields.Float('', compute='_get_lot_calcs', readonly=True)
    milk_cow_production_corrected = fields.Float('', compute='_get_lot_calcs', readonly=True)
    eat_cow_production = fields.Float('', compute='_get_lot_calcs', readonly=True)
    eat_cow_production_corrected = fields.Float('', compute='_get_lot_calcs', readonly=True)
    sequence = fields.Integer('sequence', default=1)

    @api.multi
    def _get_lot_calcs(self):
        for lot_detail in self:
            lot = lot_detail.lot_id
            res = {}
            total_theo_kg_ration = sum([x.theorical_kg_ration for x in lot_detail.lot_contents])
            total_kg_ration = sum([x.kg_ration for x in lot_detail.lot_contents])
            res['kg_mf_ration_theo'] = total_theo_kg_ration
            res['kg_mf_ration_real'] = total_kg_ration
            res['kg_mf_ration_anal'] = total_kg_ration
            if total_theo_kg_ration != 0.0:
                res['perc_ms_ration_theo'] = sum([x.theorical_kg_ration * x.theorical_ms for x in lot_detail.lot_contents]) / total_theo_kg_ration
            else:
                res['perc_ms_ration_theo'] = 0.0
            if total_kg_ration != 0.0:
                res['perc_ms_ration_real'] = sum([x.kg_ration * x.ms for x in lot_detail.lot_contents]) / total_kg_ration
            else:
                res['perc_ms_ration_real'] = 0.0
            res['perc_ms_ration_anal'] = 50.0
            res['kg_ms_ration_theo'] = res['kg_mf_ration_theo'] * (res['perc_ms_ration_theo'] / 100.0)
            res['kg_ms_ration_real'] = res['kg_mf_ration_real'] * (res['perc_ms_ration_real'] / 100.0)
            res['kg_ms_ration_anal'] = res['kg_mf_ration_anal'] * (res['perc_ms_ration_anal'] / 100.0)
            if lot.number_milking_cows + ((lot_detail.cows_eat_number - lot.number_milking_cows )/2) != 0:
                res['imf_theo'] = ((lot_detail.rations_make_number * total_theo_kg_ration) - lot_detail.surplus) / (lot.number_milking_cows + ((lot_detail.cows_eat_number - lot.number_milking_cows )/2))
            else:
                res['imf_theo'] = 0.0
            if (lot.number_milking_cows + ((lot_detail.cows_eat_number - lot.number_milking_cows) / 2)) != 0:
                res['imf_real'] = (lot_detail.kf_mf_carriage - lot_detail.surplus) / (lot.number_milking_cows + ((lot_detail.cows_eat_number - lot.number_milking_cows) / 2))
            else:
                res['imf_real'] = 0
            res['imf_anal'] = res['imf_real']

            res['kg_plucking_cow_day_theo'] = 0
            res['kg_plucking_cow_day_real'] = 0
            res['kg_plucking_cow_day_anal'] = 0

            res['ims_unifed_kg_cow_day_theo'] = 0
            res['ims_unifed_kg_cow_day_real'] = 0
            res['ims_unifed_kg_cow_day_anal'] = 0

            res['ims_plucking_kg_cow_day_theo'] = 0
            res['ims_plucking_kg_cow_day_real'] = 0
            res['ims_plucking_kg_cow_day_anal'] = 0

            if res['imf_theo'] != 0:
                res['ims_total_kg_cow_day_theo'] = res['perc_ms_ration_theo'] / 100 * res['imf_theo']
            else:
                res['ims_total_kg_cow_day_theo'] = 0
            if res['imf_real'] != 0:
                res['ims_total_kg_cow_day_real'] = res['perc_ms_ration_real'] / 100 * res['imf_real']
            else:
                res['ims_total_kg_cow_day_real'] = 0
            if res['imf_anal'] != 0:
                res['ims_total_kg_cow_day_anal'] = res['perc_ms_ration_anal'] / 100 * res['imf_anal']
            else:
                res['ims_total_kg_cow_day_anal'] = 0


            if lot.number_milking_cows != 0:
                res['milk_cow_production'] = (lot_detail.tank_liters + lot_detail.retired_liters + lot_detail.liters_on_farm_consumption) / lot.number_milking_cows
            else:
                res['milk_cow_production'] = 0
            if lot_detail.cows_eat_number != 0:
                res['eat_cow_production'] = (lot_detail.tank_liters + lot_detail.retired_liters + lot_detail.liters_on_farm_consumption) / lot_detail.cows_eat_number
            else:
                res['eat_cow_production'] = 0

            if res['ims_total_kg_cow_day_theo'] != 0:
                res['ic_liters_kg_theo'] = res['milk_cow_production'] / res['ims_total_kg_cow_day_theo']
            else:
                res['ic_liters_kg_theo'] = 0
            if res['ims_total_kg_cow_day_real'] != 0:
                res['ic_liters_kg_real'] = res['milk_cow_production'] / res['ims_total_kg_cow_day_real']
            else:
                res['ic_liters_kg_real'] = 0
            if res['ims_total_kg_cow_day_anal'] != 0:
                res['ic_liters_kg_anal'] = res['milk_cow_production'] / res['ims_total_kg_cow_day_anal']
            else:
                res['ic_liters_kg_anal'] = 0

            res['milk_cow_production_corrected'] = (12.82 * res['milk_cow_production'] * (lot.mg / 100)) + (7.13 * res['milk_cow_production'] * (lot.mp / 100) + (0.323 * res['milk_cow_production']))
            res['eat_cow_production_corrected'] = (12.82 * res['eat_cow_production'] * (lot.mg / 100)) + (7.13 * res['eat_cow_production'] * (lot.mp / 100) + (0.323 * res['eat_cow_production']))

            if res['ims_total_kg_cow_day_theo'] != 0:
                res['ic_corrected_liters_kg_theo'] = res['milk_cow_production_corrected'] / res['ims_total_kg_cow_day_theo']
            else:
                res['ic_corrected_liters_kg_theo'] = 0
            if res['ims_total_kg_cow_day_real'] != 0:
                res['ic_corrected_liters_kg_real'] = res['milk_cow_production_corrected'] / res['ims_total_kg_cow_day_real']
            else:
                res['ic_corrected_liters_kg_real'] = 0
            if res['ims_total_kg_cow_day_anal'] != 0:
                res['ic_corrected_liters_kg_anal'] = res['milk_cow_production_corrected'] / res['ims_total_kg_cow_day_anal']
            else:
                res['ic_corrected_liters_kg_anal'] = 0

            r35 = sum([x.theorical_kg_ration * (x.theorical_ms / 100.0) * x.theorical_enl for x in lot_detail.lot_contents])
            q35 = sum([x.theorical_kg_ration * (x.theorical_ms / 100.0) for x in lot_detail.lot_contents])
            if q35 != 0:
                func = '((%s * r35 / q35)-(0.08 * lot.live_weight ** 0.75)) / ((0.0929 * lot.mg) + (0.0547 * lot.mp)+(0.0395 * 4.85))'
                res['milk_prediction_by_enl_theo'] = eval(func % res['ims_total_kg_cow_day_theo'])
                res['milk_prediction_by_enl_real'] = eval(func % res['ims_total_kg_cow_day_real'])
                res['milk_prediction_by_enl_anal'] = eval(func % res['ims_total_kg_cow_day_anal'])
            else:
                res['milk_prediction_by_enl_theo'] = res['milk_prediction_by_enl_real'] = res['milk_prediction_by_enl_anal'] = 0.0

            s35 = sum([x.theorical_kg_ration * (x.theorical_ms / 100.0) * (x.theorical_pb / 100.0) * 1000 for x in lot_detail.lot_contents])
            if q35 != 0:
                s36 = s35 / q35
            else:
                s36 = 0
            res['milk_prediction_by_pb_theo'] = ((res['ims_total_kg_cow_day_theo'] * s36)-450) / 86
            res['milk_prediction_by_pb_real'] = ((res['ims_total_kg_cow_day_real'] * s36)-450) / 86
            res['milk_prediction_by_pb_anal'] = ((res['ims_total_kg_cow_day_anal'] * s36)-450) / 86

            res['real_production_deviation_theo'] = res['milk_prediction_by_enl_theo'] < res['milk_prediction_by_pb_theo'] and res['milk_cow_production_corrected'] - res['milk_prediction_by_enl_theo'] or res['milk_cow_production_corrected'] - res['milk_prediction_by_pb_theo']
            res['real_production_deviation_real'] = res['milk_prediction_by_enl_real'] < res['milk_prediction_by_pb_real'] and res['milk_cow_production_corrected'] - res['milk_prediction_by_enl_real'] or res['milk_cow_production_corrected'] - res['milk_prediction_by_pb_real']
            res['real_production_deviation_anal'] = res['milk_prediction_by_enl_anal'] < res['milk_prediction_by_pb_anal'] and res['milk_cow_production_corrected'] - res['milk_prediction_by_enl_anal'] or res['milk_cow_production_corrected'] - res['milk_prediction_by_pb_anal']

            res['ration_cost_eur_theo'] = sum([x.theorical_kg_ration * x.eur_ton_mf / 1000 for x in lot_detail.lot_contents])
            res['ration_cost_eur_anal'] = res['ration_cost_eur_real'] = sum([x.kg_ration * x.eur_ton_mf / 1000 for x in lot_detail.lot_contents])

            if total_theo_kg_ration != 0:
                res['ration_cost_eur_ton_mf_theo'] = res['ration_cost_eur_theo'] / total_theo_kg_ration * 1000
            else:
                res['ration_cost_eur_ton_mf_theo'] = 0.0
            if total_kg_ration != 0:
                res['ration_cost_eur_ton_mf_real'] = res['ration_cost_eur_real'] / total_kg_ration * 1000
            else:
                res['ration_cost_eur_ton_mf_real'] = 0.0
            if total_kg_ration != 0:
                res['ration_cost_eur_ton_mf_anal'] = res['ration_cost_eur_anal'] / total_kg_ration * 1000
            else:
                res['ration_cost_eur_ton_mf_anal'] = 0.0

            if res['perc_ms_ration_theo'] != 0:
                res['ration_cost_eur_ton_ms_theo'] = res['ration_cost_eur_ton_mf_theo'] / (res['perc_ms_ration_theo'] / 100.0)
            else:
                res['ration_cost_eur_ton_ms_theo'] = 0.0
            if res['perc_ms_ration_real'] != 0:
                res['ration_cost_eur_ton_ms_real'] = res['ration_cost_eur_ton_mf_real'] / (res['perc_ms_ration_real'] / 100.0)
            else:
                res['ration_cost_eur_ton_ms_real'] = 0.0
            if res['perc_ms_ration_anal'] != 0:
                res['ration_cost_eur_ton_ms_anal'] = res['ration_cost_eur_ton_mf_anal'] / (res['perc_ms_ration_anal'] / 100.0)
            else:
                res['ration_cost_eur_ton_ms_anal'] = 0.0

            res['ration_carriage_cost_eur_cow_day_theo'] = (res['ims_total_kg_cow_day_theo'] * res['ration_cost_eur_ton_ms_theo'] / 1000) + lot.carriage_cost_cow_day
            res['ration_carriage_cost_eur_cow_day_real'] = (res['ims_total_kg_cow_day_real'] * res['ration_cost_eur_ton_ms_real'] / 1000) + lot.carriage_cost_cow_day
            res['ration_carriage_cost_eur_cow_day_anal'] = (res['ims_total_kg_cow_day_anal'] * res['ration_cost_eur_ton_ms_anal'] / 1000) + lot.carriage_cost_cow_day

            if res['milk_cow_production'] != 0:
                res['ration_carriage_cost_eur_liter_theo'] = (res['ration_carriage_cost_eur_cow_day_theo'] / res['milk_cow_production']) * 100
                res['ration_carriage_cost_eur_liter_real'] = (res['ration_carriage_cost_eur_cow_day_real'] / res['milk_cow_production']) * 100
                res['ration_carriage_cost_eur_liter_anal'] = (res['ration_carriage_cost_eur_cow_day_anal'] / res['milk_cow_production']) * 100

                res['ration_carriage_cost_corrected_milk_eur_liter_theo'] = (res['ration_carriage_cost_eur_cow_day_theo'] / res['milk_cow_production_corrected']) * 100
                res['ration_carriage_cost_corrected_milk_eur_liter_real'] = (res['ration_carriage_cost_eur_cow_day_real'] / res['milk_cow_production_corrected']) * 100
                res['ration_carriage_cost_corrected_milk_eur_liter_anal'] = (res['ration_carriage_cost_eur_cow_day_anal'] / res['milk_cow_production_corrected']) * 100
            else:
                res['ration_carriage_cost_eur_liter_theo'] = res['ration_carriage_cost_eur_liter_real'] = res['ration_carriage_cost_eur_liter_anal'] = 0.0
                res['ration_carriage_cost_corrected_milk_eur_liter_theo'] = res['ration_carriage_cost_corrected_milk_eur_liter_real'] = res['ration_carriage_cost_corrected_milk_eur_liter_theo'] = 0.0

            res['grs_fat_cow_day'] = res['milk_cow_production'] * lot.mg * 10
            res['grs_protein_cow_day'] = res['milk_cow_production'] * lot.mp * 10

            if lot.number_milking_cows != 0:
                res['ingress_milk_cow_day'] = (lot_detail.tank_liters / lot.number_milking_cows) * lot.milk_price / 1000
            else:
                res['ingress_milk_cow_day'] = 0
            res['feed_cost_cow_day'] = res['ration_carriage_cost_eur_cow_day_real']
            res['diff_ing_cost'] = res['ingress_milk_cow_day'] - res['feed_cost_cow_day']
            if res['ingress_milk_cow_day'] != 0:
                res['perc_feed_milk_ingress'] = res['feed_cost_cow_day'] / res['ingress_milk_cow_day'] * 100
            else:
                res['perc_feed_milk_ingress'] = 0.0

            res['perc_purchased_feed_milk_ingress'] = 0
            y3 = sum([x.kg_ration * x.eur_ton_mf / 1000 for x in lot_detail.lot_contents if x.product_id.concenctrate])
            if res['ingress_milk_cow_day'] != 0:
                res['perc_concentrated_milk_ingress'] = ((y3 * lot_detail.rations_make_number) / lot_detail.cows_eat_number / res['ingress_milk_cow_day']) * 100
            else:
                res['perc_concentrated_milk_ingress'] = 0.0
            i3 = sum([x.kg_ration for x in lot_detail.lot_contents if x.product_id.concenctrate])
            if i3 * lot_detail.rations_make_number != 0:
                res['liters_produced_kg_concentrated_used'] = (lot_detail.tank_liters + lot_detail.retired_liters + lot_detail.liters_on_farm_consumption) / (i3 * lot_detail.rations_make_number)
            else:
                res['liters_produced_kg_concentrated_used'] = 0.0

            if lot.milk_price != 0.0:
                res['lot_threshold_point_slaughterhouse'] = res['ration_carriage_cost_eur_cow_day_real'] / (lot.milk_price / 1000)
                res['lot_threshold_point_dry'] = (res['ration_carriage_cost_eur_cow_day_real'] - lot.dry_cow_ration_cost) / (lot.milk_price / 1000)
            else:
                res['lot_threshold_point_slaughterhouse'] = res['lot_threshold_point_dry'] = 0.0

            for field in res.keys():
                lot_detail[field] = res[field]


class LotContent(models.Model):

    _name = 'lot.content'

    detail_id = fields.Many2one('lot.detail', 'Detail',
                                default=lambda a: datetime.now())
    eur_ton_mf = fields.Integer('€/Tn MF')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    kg_ration = fields.Float('Kg/Ration')
    ms = fields.Float('%MS')
    enl = fields.Float('ENL')
    pb = fields.Float('%PB')
    theorical_kg_ration = fields.Float('Kg/Ration',
                                       compute='_get_theorical_values')
    theorical_ms = fields.Float('%MS', compute='_get_theorical_values')
    theorical_enl = fields.Float('ENL', compute='_get_theorical_values')
    theorical_pb = fields.Float('%PB', compute='_get_theorical_values')

    @api.multi
    @api.depends('product_id', 'detail_id.lot_id')
    def _get_theorical_values(self):
        for content in self:
            if not content.detail_id.lot_id:
                continue
            curr_lot = content.detail_id.lot_id
            last_lot = self.env['lot'].search(
                [('farm_id', '=', curr_lot.farm_id.id),
                 ('id', '!=', curr_lot.id), ('date', '<=', curr_lot.date)],
                order='date desc', limit=1)
            if last_lot:
                detail = self.env['lot.detail'].search(
                    [('lot_id', '=', last_lot.id),
                     ('sequence', '=', content.detail_id.sequence)], limit=1)
                if detail:
                    last_content = self.env['lot.content'].search(
                        [('detail_id', '=', detail.id),
                         ('product_id', '=', content.product_id.id)])
                    if last_content:
                        content.theorical_kg_ration = last_content.kg_ration
                        content.theorical_ms = last_content.ms
                        content.theorical_enl = last_content.enl
                        content.theorical_pb = last_content.pb
