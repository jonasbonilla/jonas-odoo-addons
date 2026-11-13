import {ORM} from "@web/core/orm_plugin";
import {_t} from "@web/core/l10n/translation";
import {browser} from "@web/core/browser/browser";
import {cookie} from "@web/core/browser/cookie";
import {registry} from "@web/core/registry";
import {usePlugin} from "@odoo/owl";
import {user} from "@web/core/user";

export function colorSchemeSwitchItem() {
  const orm = usePlugin(ORM);
  const isDark = cookie.get("color_scheme") === "dark";
  return {
    type: "switch",
    id: "color_scheme.switch",
    description: _t("Dark Mode"),
    isChecked: isDark,
    callback: async () => {
      const scheme = isDark ? "light" : "dark";
      await orm.write("res.users", [user.userId], {color_scheme: scheme});
      cookie.set("color_scheme", scheme);
      browser.location.reload();
    },
    sequence: 35,
  };
}

registry.category("user_menuitems").add("color_scheme_switch", colorSchemeSwitchItem);
