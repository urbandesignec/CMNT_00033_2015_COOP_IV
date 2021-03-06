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
from openerp import models, api, fields, exceptions, _


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.multi
    def write(self, vals):
        for user in self:
            if user.id == 1 and self.env.user.id != 1:
                raise exceptions.Warning(
                    _('Write error'),
                    _('Only %s can edit his user') % user.name)
        return super(ResUsers, self).write(vals)

    @api.multi
    def unlink(self):
        partners = self.env["res.partner"]
        for user in self:
            if user.partner_id:
                partners += user.partner_id
        res = super(ResUsers, self).unlink()
        partners.unlink()
        return res

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        if res.company_id.cooperative_company.group_id:
            res.company_id.cooperative_company.group_id.message_subscribe_users(user_ids=[res.id])
        return res

class ResGroup(models.Model):

    _inherit = 'res.groups'

    default_event_categories = fields.Many2many(
        'calendar.event.type')
