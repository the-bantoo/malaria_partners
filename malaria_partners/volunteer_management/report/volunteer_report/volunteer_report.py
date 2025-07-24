# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt
from frappe import _
import frappe


def execute(filters=None):
	return get_columns(filters), get_data(filters)
	
def get_data(filters):
	conditions = []

	if filters.get('from_date'):
		conditions.append(f"vl.start_date >= '{filters.get('from_date')}'")
	if filters.get('to_date'):
		conditions.append(f"vl.end_date <= '{filters.get('to_date')}'")

	params = {} # Dictionary to store parameters for the query

	# Define a mapping for filters to SQL columns
	filter_map = {
		'volunteer': 'vl.volunteer',
		'gender': 'v.gender',
		'club_type': 'vl.club_type',
		'position': 'vl.club_position',
		'activity_supported': 'vl.activity_supported',
		'district_supported': 'vl.district_supported'
	}

	for filter_key, sql_column in filter_map.items():
		if filters.get(filter_key):
			# Use placeholder for parameterized query
			conditions.append(f"{sql_column} = %({filter_key})s")
			params[filter_key] = filters.get(filter_key)

	conditions_sql = " AND ".join(conditions)
	# Always include docstatus=1 as a base condition
	if conditions_sql:
		conditions_sql = f"WHERE {conditions_sql} AND vl.docstatus=1"
	else:
		conditions_sql = "WHERE vl.docstatus=1"

	group_by_field = filters.get('group_by')
	group_by_sql = ""
	
	# Base selection for no grouping
	select_fields = [
		"vl.start_date as start_date",
		"vl.full_name as volunteer",
		"v.gender as gender",
		"vl.nrcid as nrcid",
		"act.subject as activity",
		"vl.district_supported as district",
		"vl.club_position as club_position",
		"vl.club_type as club_type",
		"vl.club as club",
		"vl.days_spent AS days_spent",
		"vl.volunteer_time as total_hours"
	]

	# Grouping logic
	if group_by_field:
		# Use a dictionary to map group_by_field to SQL parts for cleaner code
		group_by_map = {
			"Volunteer": {"group": "vl.volunteer", "select": "vl.full_name as volunteer"},
			"Gender": {"group": "v.gender", "select": "v.gender as gender"},
			"Club": {"group": "vl.club", "select": "vl.club as club"},
			"Club Type": {"group": "vl.club_type", "select": "vl.club_type as club_type"},
			"Activity": {"group": "vl.activity_supported", "select": "act.subject as activity"},
			"District": {"group": "vl.district_supported", "select": "vl.district_supported as district"}
		}
		
		if group_by_field in group_by_map:
			group_info = group_by_map[group_by_field]
			group_by_sql = f"GROUP BY {group_info['group']}"
			select_fields = [
				group_info['select'],
				"sum(vl.days_spent) as days_spent",
				"GROUP_CONCAT(DISTINCT TRIM(act.subject) SEPARATOR ', ') as activities",
				"sum(vl.volunteer_time) as total_hours"
			]
		# else: handle invalid group_by_field if necessary

	select_fields_sql = ", ".join(select_fields)

	query = f"""
		SELECT {select_fields_sql}
		FROM `tabVolunteer Log` as vl
		JOIN `tabVolunteer Profile` AS v ON vl.volunteer = v.name
		LEFT JOIN `tabTask` AS act ON vl.activity_supported = act.name
		{conditions_sql}
		{group_by_sql}
		ORDER BY vl.start_date
	"""
	
	# frappe.errprint(query) # For debugging, useful to see the constructed query
	
	# Pass parameters to frappe.db.sql
	data = frappe.db.sql(query, values=params, as_dict=1)

	return data

def get_columns(filters):
	group_by_field = filters.get('group_by')
	columns = [
			{"label": _("Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 110},
			{"label": _("Volunteer"), "fieldname": "volunteer", "fieldtype": "Data", "width": 180},
			{"label": _("Sex"), "fieldname": "gender", "fieldtype": "Data", "width": 60},
			#{"label": _("NRC/ID"), "fieldname": "nrcid", "fieldtype": "Data", "width": 120},
			{"label": _("Activity"), "fieldname": "activity", "fieldtype": "Data", "width": 300},
			{"label": _("District"), "fieldname": "district", "fieldtype": "Data", "width": 100},
			{"label": _("Position"), "fieldname": "club_position", "fieldtype": "Data", "width": 90},
			{"label": _("Club"), "fieldname": "club", "fieldtype": "Data", "width": 230},
			{"label": _("Days"), "fieldname": "days_spent", "fieldtype": "Data", "width": 60},
			{"label": _("Hours"), "fieldname": "total_hours", "fieldtype": "Int", "width": 70},
		]
	
	if group_by_field:
		if group_by_field == "Volunteer":
			columns = [
				{"label": _("Volunteer"), "fieldname": "volunteer", "fieldtype": "Link", "options": "Volunteer Profile", "width": 250},
				{"label": _("Activities"), "fieldname": "activities", "fieldtype": "Data", "width": 760},
			]
		elif group_by_field == "Gender":
			columns = [
				{"label": _("Gender"), "fieldname": "gender", "fieldtype": "Data", "width": 1010}
			]
		elif group_by_field == "Club":
			columns = [
				{"label": _("Club"), "fieldname": "club", "fieldtype": "Data", "width": 250},
				{"label": _("Activities"), "fieldname": "activities", "fieldtype": "Data", "width": 760},
			]
		elif group_by_field == "Club Type":
			columns = [
				{"label": _("Club Type"), "fieldname": "club_type", "fieldtype": "Data", "width": 1010}
			]
		elif group_by_field == "Activity":
			columns = [
				{"label": _("Activity"), "fieldname": "activity", "fieldtype": "Data", "width": 1010}
			]
		elif group_by_field == "District":
			columns = [
				{"label": _("District"), "fieldname": "district", "fieldtype": "Data", "width": 300},
				{"label": _("Activities"), "fieldname": "activities", "fieldtype": "Data", "width": 710}
			]
		columns = columns + [
			{"label": _("Days"), "fieldname": "days_spent", "fieldtype": "Data", "width": 100},
			{"label": _("Hours"), "fieldname": "total_hours", "fieldtype": "Int", "width": 100}
		]

	return columns