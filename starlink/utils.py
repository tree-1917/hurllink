import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path

def path_mapper(path: str) -> str:
    """Mapper function that logs all hurllink records and processes path."""
    # Fetch and log all hurllink records
    try:
        # hurllink_records = frappe.db.sql("""
        #     SELECT name, shortlink, target
        #     FROM `tabhurllink`  -- Corrected to match your exact DocType name
        # """)
        hurllink_records = frappe.db.sql("""
			SELECT name, shortlink, target
			FROM `tabhurllink`
        """)
        print(
            f"Hurllink Records:\n{'\n'.join(f'{r[0]}: {r[1]} → {r[2]}' for r in hurllink_records)}",
            "PathMapper"
        )
    except Exception as e:
        print(f"Error fetching hurllink records: {str(e)}", "PathMapper")

    print(f"Processing path: {path}", "PathMapper")
    return original_resolve_path(path)
