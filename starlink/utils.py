import logging

import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path


def get_logger():
    logger = frappe.logger("starlinkLog", allow_site=True)
    logger.setLevel(logging.INFO)
    return logger


def path_mapper(path: str):
    logger = get_logger()
    logger.info(f"Incoming path: {path}")

    if path and frappe.db.exists("hurllink", {"shortlink": path}):
        target = frappe.db.get_value("hurllink", {"shortlink": path}, "target")
        if target:
            logger.info(f"Redirecting '{path}' → {target}")
            frappe.local.response.update({
                "type": "redirect",
                "location": target
            })
            raise frappe.Redirect

    return original_resolve_path(path)
