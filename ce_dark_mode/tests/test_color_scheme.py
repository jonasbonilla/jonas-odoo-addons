from odoo.tests import HttpCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestColorScheme(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(cls.env, login="ce_dark_mode_user")

    def _open_webclient(self):
        self.env.flush_all()
        response = self.url_open("/odoo")
        self.assertEqual(response.status_code, 200)
        return response

    def test_user_writes_own_color_scheme(self):
        self.assertEqual(self.user.color_scheme, "light")
        self.user.with_user(self.user).write({"color_scheme": "dark"})
        self.assertEqual(self.user.color_scheme, "dark")

    def test_webclient_follows_user_preference(self):
        self.user.color_scheme = "dark"
        self.authenticate(self.user.login, self.user.login)
        response = self._open_webclient()
        self.assertIn("web.assets_web_dark", response.text)
        self.assertEqual(self.opener.cookies.get("color_scheme"), "dark")

        # The preference wins over a stale cookie (changed in another tab or
        # left by another user).
        self.user.color_scheme = "light"
        response = self._open_webclient()
        self.assertNotIn("web.assets_web_dark", response.text)
        self.assertEqual(self.opener.cookies.get("color_scheme"), "light")

    def test_logout_drops_cookie(self):
        self.user.color_scheme = "dark"
        self.authenticate(self.user.login, self.user.login)
        self._open_webclient()
        self.assertEqual(self.opener.cookies.get("color_scheme"), "dark")

        self.url_open(
            "/web/session/logout",
            method="POST",
            data={"csrf_token": self.csrf_token()},
        )
        self.assertIsNone(self.opener.cookies.get("color_scheme"))
