# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt
from frappe import _
import frappe


def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
    conditions = []

    if filters.get('volunteer'):
        conditions.append(f"volunteer = '{filters.get('volunteer')}'")
    if filters.get('gender'):
        conditions.append(f"gender = '{filters.get('gender')}'")
    if filters.get('club_type'):
        conditions.append(f"club_type = '{filters.get('club_type')}'")
    if filters.get('position'):
        conditions.append(f"club_position = '{filters.get('position')}'")
    if filters.get('activity_supported'):
        conditions.append(f"activity_supported = '{filters.get('activity_supported')}'")
    if filters.get('district_supported'):
        conditions.append(f"district_supported = '{filters.get('district_supported')}'")

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = "WHERE " + conditions_sql

    query = f"""SELECT volunteer, district_supported,
                activity_supported, gender, nrcid, club_type, 
                club_position, days_of_voluntary_session, time_spent 
                FROM `tabVolunteer Log` {conditions_sql}"""

    # print(query)  # Uncomment for debugging purposes
    data = frappe.db.sql(query)
    return data



def get_columns():
	return [
		"Volunteer:Link/Volunteer Log:100",
		"District Supported:Data:100",
		"Activity Supported:Data:100",
		"Gender:Data:100",
		"NRC/ID:Data:120",
		"Club Type:Data:100",
		"Club Position:Data:100",
		"Days Spent:Float:100",
		"Total Hours:Duration:100",
	]
