import frappe

def execute():
    frappe.reload_doc("malaria_partners", "doctype", "volunteer_log") # Reload DocType definition

    frappe.msgprint("Starting conversion of 'time_spent' to hours for Volunteer Logs...")

    # Fetch all Volunteer Log documents
    # Only fetch if time_spent is not None and not 0, to avoid unnecessary updates
    # Or just fetch all and let calculate_time_spent handle the logic
    volunteer_logs = frappe.get_list("Volunteer Log", fields=["name", "days_spent", "manually_set_time_spent"])
    settings = frappe.get_cached_doc("Volunteer Settings", "Volunteer Settings")  
    daily_std_hrs = settings.standard_work_hours   


    for log_name in [d.name for d in volunteer_logs]:
        try:
            doc = frappe.get_doc("Volunteer Log", log_name)
            
            # Use the existing calculate_time_spent method defined in your DocType
            # This handles the 'manually_set_time_spent' logic too.
            if doc.time_spent:
                doc.volunteer_time = seconds_to_hours(doc.time_spent)
            else:
                doc.volunteer_time = calculate_time_spent(doc, daily_std_hrs)

            doc.db_update()
            print(f"Updated Volunteer Log {doc.name}: 'time_spent' calculated as {doc.time_spent} hours.")

        except Exception as e:
            print(f"Error updating Volunteer Log {log_name}: {e}", "Volunteer Log Hours Conversion Patch Error")
            # Decide if you want to re-raise to stop the migration or continue.
            # For data integrity, stopping is often safer.
            raise
        # break

    print("Volunteer Log 'time_spent' conversion to hours complete!")


def calculate_time_spent(doc, daily_std_hrs):
    if doc.days_spent:
        return doc.days_spent * daily_std_hrs
        print("daily_std_hrs", daily_std_hrs)
    else:
        return daily_std_hrs

def seconds_to_hours(seconds):
    """
    Converts a duration in seconds to hours (float).

    Args:
    seconds: The number of seconds (can be an integer or float).

    Returns:
    The duration in hours as a float.
    """
    if seconds is None:
        return 0.0 # Or raise an error, depending on desired behavior for None input
    return float(seconds) / 3600.0