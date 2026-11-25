import {Plugin, useListener, usePlugin} from "@odoo/owl";
import {ORM} from "@web/core/orm_plugin";
import {_t} from "@web/core/l10n/translation";
import {cookie} from "@web/core/browser/cookie";
import {location} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {services} from "@web/core/services";
import {user} from "@web/core/user";

// Scheme this page was rendered with: the server sets the cookie on the web
// client response, before any script runs. Another tab may change the cookie
// later, so never read it again to know how this page looks.
const pageColorScheme = cookie.get("color_scheme") === "dark" ? "dark" : "light";

/**
 * The cookie is shared by every tab, but read by the code of each one (lazy
 * bundles of graph/pivot views, charts, editor...). When a tab comes back to
 * the foreground, give the cookie back the scheme of its page, so that a tab
 * still rendered in the other scheme does not load the wrong assets.
 */
export class ColorSchemeSyncPlugin extends Plugin {
  setup() {
    useListener(document, "visibilitychange", () => {
      if (
        document.visibilityState === "visible" &&
        cookie.get("color_scheme") !== pageColorScheme
      ) {
        cookie.set("color_scheme", pageColorScheme);
      }
    });
  }
}

services.add(ColorSchemeSyncPlugin);

export function colorSchemeSwitchItem() {
  const orm = usePlugin(ORM);
  const isDark = pageColorScheme === "dark";
  return {
    type: "switch",
    id: "color_scheme.switch",
    description: _t("Dark Mode"),
    isChecked: isDark,
    callback: async () => {
      const scheme = isDark ? "light" : "dark";
      await orm.write("res.users", [user.userId], {color_scheme: scheme});
      cookie.set("color_scheme", scheme);
      location.reload();
    },
    sequence: 35,
  };
}

registry.category("user_menuitems").add("color_scheme_switch", colorSchemeSwitchItem);
