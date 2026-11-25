from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _post_logout(cls):
        """Drop the cookie so the next user never inherits the previous
        user's scheme; it is rewritten from their preference on login."""
        res = super()._post_logout()
        request.future_response.set_cookie("color_scheme", max_age=0)
        return res

    def color_scheme(self):
        """Use the user's preference and keep the ``color_scheme`` cookie in
        sync, since the JS side (lazy bundles, charts, mail...) reads it.

        Only called by the web client route, which always has a request and
        a logged-in user."""
        scheme = self.env.user.color_scheme or "light"
        if request.cookies.get("color_scheme") != scheme:
            request.future_response.set_cookie("color_scheme", scheme)
        return scheme
