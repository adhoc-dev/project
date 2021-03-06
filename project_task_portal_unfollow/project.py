# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields


class project(models.Model):
    _inherit = 'project.project'

    unfollow_portal_users = fields.Boolean(
        'Unfollow Portal Users',
        help='Unfollow Portal Users from new tasks?',
        )


class project_task(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        task = super(project_task, self).create(vals)
        if not task.project_id.unfollow_portal_users:
            return task
        partner_to_unfollow_ids = []
        for follower in task.message_follower_ids:
            if follower.user_ids:
                for user in follower.user_ids:
                    if not user.sudo(user).user_has_groups('base.group_user'):
                        partner_to_unfollow_ids.append(user.partner_id.id)
                        continue
            else:
                partner_to_unfollow_ids.append(user.partner_id.id)
        task.message_unsubscribe(partner_to_unfollow_ids)
        return task

    @api.one
    def write(self, vals):
        res = super(project_task, self).write(vals)
        if not self.project_id.unfollow_portal_users:
            return res
        partner_to_unfollow_ids = []
        for follower in self.message_follower_ids:
            if follower.user_ids:
                for user in follower.user_ids:
                    if not user.sudo(user).user_has_groups('base.group_user'):
                        partner_to_unfollow_ids.append(user.partner_id.id)
                        continue
            else:
                partner_to_unfollow_ids.append(user.partner_id.id)
        self.message_unsubscribe(partner_to_unfollow_ids)
        return res
