{
    "name": "Dark Mode (Community)",
    "summary": "Per-user dark mode for the backend web client (Community only)",
    "version": "20.0.1.0.0",
    "category": "Tools/UI",
    "license": "LGPL-3",
    "author": "Jonas Bonilla",
    "website": "https://github.com/jonasbonilla/jonas-odoo-addons",
    "depends": ["web"],
    # Enterprise provides its own dark mode.
    "excludes": ["web_enterprise"],
    "data": [
        "views/res_users_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ce_dark_mode/static/src/webclient/**/*.js",
        ],
        "web.assets_web_dark": [
            (
                "before",
                "web/static/src/scss/primary_variables.scss",
                "ce_dark_mode/static/src/scss/primary_variables.dark.scss",
            ),
            (
                "before",
                "web/static/src/scss/bootstrap_overridden.scss",
                "ce_dark_mode/static/src/scss/bootstrap_overridden.dark.scss",
            ),
            "ce_dark_mode/static/src/overrides/**/*.dark.scss",
        ],
        # Lazy loaded views (graph, pivot...) are compiled in their own bundle.
        "web.assets_backend_lazy_dark": [
            (
                "before",
                "web/static/src/scss/primary_variables.scss",
                "ce_dark_mode/static/src/scss/primary_variables.dark.scss",
            ),
            (
                "before",
                "web/static/src/scss/bootstrap_overridden.scss",
                "ce_dark_mode/static/src/scss/bootstrap_overridden.dark.scss",
            ),
        ],
    },
    "installable": True,
    "application": False,
}
