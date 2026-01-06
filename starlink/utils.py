import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path


def path_mapper(path: str):
    """
    Custom path mapper that handles hurllink redirects while allowing normal routes.
    """

    # Clean the path by removing leading/trailing slashes and spaces
    cleaned_path = path.strip("/ ")

    # Check if this is a hurllink shortlink
    if cleaned_path and frappe.db.exists("hurllink", {"shortlink": cleaned_path}):
        # Get the target URL from the database
        target = frappe.db.get_value("hurllink", {"shortlink": cleaned_path}, "target")

        if target:
            frappe.logger().info(f"Redirecting shortlink '{cleaned_path}' to: {target}")

            # Perform HTTP redirect
            frappe.local.response.update({
                "type": "redirect",
                "location": target
            })
            raise frappe.Redirect

    # For all other paths, let Frappe handle them normally
    frappe.logger().debug(f"Processing normal path: {path}")
    return original_resolve_path(path)
