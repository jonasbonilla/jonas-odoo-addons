from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _post_logout(cls):
        """Drop the cookie so the next user never inherits the previous
        user's scheme; it is rewritten from their preference on login."""
        super()._post_logout()
        request.future_response.set_cookie("color_scheme", max_age=0)
        return True

    def color_scheme(self):
        """Use the user's preference and keep the ``color_scheme`` cookie in
        sync, since the JS side (lazy bundles, charts, mail...) reads it."""
        scheme = super().color_scheme()
        if not request:
            return scheme
        cookie_scheme = request.cookies.get("color_scheme")
        if request.session.uid:
            scheme = self.env.user.color_scheme or "light"
            if cookie_scheme != scheme:
                request.future_response.set_cookie("color_scheme", scheme)
        elif cookie_scheme in ("light", "dark"):
            scheme = cookie_scheme
        return scheme
