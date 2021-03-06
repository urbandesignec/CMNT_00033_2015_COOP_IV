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

{
    'name': 'Custom menu',
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Comunitea',
    'website': '',
    "depends": ['base',
                'calendar',
                'account',
                'product',
                'acc_analytic_acc_distribution_between',
                'stock_account',
                'res_partner_farm_data',
                'farm_notebook',
                'auditlog',
                'document',
                'knowledge',
                'mail',
                'custom_groups',
                'custom_project',
                'account_analytic_report',
                'quality_simulator'],
    "data": ['security/group.xml', 'security/ir_rule.xml', 'security/ir.model.access.csv', 'custom_menu.xml'],
    "installable": True
}
