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

    # TODO: Need to handle query params like /gin?=search?=abc
    if path and frappe.db.exists("hurllink", {"shortlink": path}):
        short_link = frappe.db.get_value("hurllink", {"shortlink": path}, ["target", "name"],
                                         as_dict=True)

        logger.info(frappe.local.request.headers)

        click = frappe.new_doc("starlinkclick")
        click.ip = frappe.local.request_ip
        click.link = short_link.target
        click.useragent = frappe.local.request.headers["User-Agent"]
        # click.referrer = frappe.local.request.headers["Referer"]
        click.name = short_link.name

        click.insert().submit()
        frappe.db.commit()
        logger.info(f"click IP: {click.ip}, click Link: {click.link}")
        if short_link:
            logger.info(f"Redirecting '{path}' → {short_link}")
            frappe.local.response.update({
                "type": "redirect",
                "location": short_link.target
            })
            raise frappe.Redirect

    return original_resolve_path(path)
