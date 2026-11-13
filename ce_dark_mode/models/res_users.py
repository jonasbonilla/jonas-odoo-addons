from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    color_scheme = fields.Selection(
        selection=[("light", "Light"), ("dark", "Dark")],
        default="light",
        required=True,
        user_writeable=True,
        help="Color scheme of the web client. Reload the page to apply it.",
    )
