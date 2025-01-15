import frappe
from frappe import _
from frappe.utils import flt, getdate, date_diff

def execute(filters=None):
	if not filters:
		filters = {}
	
	columns = get_columns(filters)
	data, chart_data = get_report_data(filters)
	
	return columns, data, None, chart_data


def get_columns(filters):
	"""Define the columns for the report based on grouping"""
	group_by = filters.get('group_by')
	
	if group_by == 'license_plate':
		return [
			{
				"fieldname": "license_plate",
				"label": _("Vehicle"),
				"fieldtype": "Link",
				"options": "Vehicle",
				"width": 110
			},
			{
				"fieldname": "total_trips",
				"label": _("Total Trips"),
				"fieldtype": "Int",
				"width": 100
			},
			{
				"fieldname": "total_distance",
				"label": _("Total Distance (km)"),
				"fieldtype": "Float",
				"width": 150
			},
			{
				"fieldname": "total_fuel",
				"label": _("Total Fuel (L)"),
				"fieldtype": "Float",
				"width": 130
			}
		]
	elif group_by == 'employee':
		return [
			{
				"fieldname": "employee_name",
				"label": _("Driver"),
				"fieldtype": "Data",
				"width": 150
			},
			{
				"fieldname": "total_trips",
				"label": _("Total Trips"),
				"fieldtype": "Int",
				"width": 100
			},
			{
				"fieldname": "total_distance",
				"label": _("Total Distance (km)"),
				"fieldtype": "Float",
				"width": 150
			},
			{
				"fieldname": "total_fuel",
				"label": _("Total Fuel (L)"),
				"fieldtype": "Float",
				"width": 130
			}
		]
	elif group_by == 'project':
		return [
			{
				"fieldname": "project_name",
				"label": _("Project"),
				"fieldtype": "Data",
				"width": 150
			},
			{
				"fieldname": "total_trips",
				"label": _("Total Trips"),
				"fieldtype": "Int",
				"width": 100
			},
			{
				"fieldname": "total_distance",
				"label": _("Total Distance (km)"),
				"fieldtype": "Float",
				"width": 150
			},
			{
				"fieldname": "total_fuel",
				"label": _("Total Fuel (L)"),
				"fieldtype": "Float",
				"width": 130
			}
		]
	else:
		# Return original columns for no grouping
		return [
			{
				"fieldname": "date",
				"label": _("Date"),
				"fieldtype": "Date",
				"width": 110
			},
			{
				"fieldname": "license_plate",
				"label": _("Vehicle"),
				"fieldtype": "Link",
				"options": "Vehicle",
				"width": 110
			},
			{
				"fieldname": "employee_name",
				"label": _("Driver"),
				"fieldtype": "Data",
				"width": 150
			},
			{
				"fieldname": "from_location",
				"label": _("From"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "to_location",
				"label": _("To"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "distance",
				"label": _("Distance (km)"),
				"fieldtype": "Float",
				"width": 100
			},
			{
				"fieldname": "fuel_qty",
				"label": _("Fuel Loaded (L)"),
				"fieldtype": "Float",
				"width": 140
			},
			{
				"fieldname": "project_name",
				"label": _("Project"),
				"fieldtype": "Data",
				"width": 150
			},
			{
				"fieldname": "log",
				"label": _("Driver Log"),
				"fieldtype": "Link",
				"options": "Driver Log",
				"width": 200
			}
		]

def get_filters():
	"""Define report filters"""
	return [
		{
			"fieldname": "from_date",
			"label": _("From Date"),
			"fieldtype": "Date",
			"default": frappe.utils.add_months(frappe.utils.nowdate(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": _("To Date"),
			"fieldtype": "Date",
			"default": frappe.utils.nowdate(),
			"reqd": 1
		},
		{
			"fieldname": "license_plate",
			"label": _("Vehicle"),
			"fieldtype": "Link",
			"options": "Vehicle"
		},
		{
			"fieldname": "employee",
			"label": _("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "Project"
		}
	]

def get_report_data(filters):
	conditions = get_conditions(filters)
	
	if filters.get('group_by'):
		data = get_grouped_data(conditions, filters)
	else:
		data = get_driver_logs(conditions, filters)
	
	summary_data = process_summary_data(data)
	chart_data = generate_chart_data(summary_data)
	
	return data, chart_data

def get_grouped_data(conditions, filters):
	group_by = filters.get('group_by')
	
	group_fields = {
		'license_plate': 'dl.license_plate',
		'employee': 'e.employee_name',
		'project': 'p.project_name'
	}
	
	group_field = group_fields.get(group_by)
	
	query = """
		SELECT
			{group_field} as group_field,
			COUNT(DISTINCT dl.name) as total_trips,
			SUM(CASE 
				WHEN dl.odometer IS NULL OR dl.last_odometer IS NULL THEN 0
				WHEN dl.odometer >= dl.last_odometer THEN (dl.odometer - dl.last_odometer)
				ELSE 0
			END) as total_distance,
			SUM(dl.fuel_qty) as total_fuel
		FROM 
			`tabDriver Log` dl
		LEFT JOIN `tabEmployee` e ON dl.employee = e.name
		LEFT JOIN `tabProject` p ON dl.project = p.name
		WHERE
			dl.docstatus = 1
			{conditions}
		GROUP BY
			{group_field}
		ORDER BY 
			total_distance DESC
	""".format(
		group_field=group_field,
		conditions=conditions and "AND " + conditions or ""
	)
	
	data = frappe.db.sql(query, filters, as_dict=1)
	
	# Map the group_field back to the appropriate field name
	for row in data:
		if group_by == 'license_plate':
			row['license_plate'] = row.pop('group_field')
		elif group_by == 'employee':
			row['employee_name'] = row.pop('group_field')
		elif group_by == 'project':
			row['project_name'] = row.pop('group_field') or "Other/Non Project"
	
	return data

def get_conditions(filters):
	"""Build conditions for SQL query based on filters"""
	conditions = []
	
	if filters.get("from_date"):
		conditions.append("date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("date <= %(to_date)s")
	if filters.get("license_plate"):
		conditions.append("license_plate = %(license_plate)s")
	if filters.get("employee"):
		conditions.append("dl.employee = %(employee)s")
	if filters.get("project"):
		conditions.append("dl.project = %(project)s")
	
	return " AND ".join(conditions)

def get_driver_logs(conditions, filters):
	"""Fetch driver logs from database"""
	query = """
		SELECT
			dl.name as log,
			e.employee_name as employee_name,
			dl.date,
			dl.license_plate,
			dl.employee,
			p.project_name as project_name,
			(SELECT places
				FROM `tabPlaces` plc
				WHERE plc.parent = dl.name
				AND plc.parentfield = 'from'
				ORDER BY plc.creation DESC
				LIMIT 1) as from_location,
			(SELECT GROUP_CONCAT(plc.places SEPARATOR ', ')
				FROM `tabPlaces` plc
				WHERE plc.parent = dl.name
				AND plc.parentfield = 'to'
				ORDER BY plc.creation DESC) as to_location,
			CASE 
				WHEN dl.odometer IS NULL OR dl.last_odometer IS NULL THEN 0
				WHEN dl.odometer >= dl.last_odometer THEN (dl.odometer - dl.last_odometer)
				ELSE 0
			END as distance,
			dl.fuel_qty,
			dl.project
		FROM 
			`tabDriver Log` dl
		LEFT JOIN `tabEmployee` e ON dl.employee = e.name
		LEFT JOIN `tabProject` p ON dl.project = p.name
		WHERE
			dl.docstatus = 1
			{conditions}
		ORDER BY 
			dl.date DESC
	""".format(conditions=conditions and "AND " + conditions or "")

	data = frappe.db.sql(query, (filters), as_dict=1)
	return data

def process_summary_data(data):
	"""Process raw data into summary metrics"""
	summary = {
		"vehicles": {},
		"total_distance": 0,
		"total_fuel": 0,
		"total_cost": 0,
		"routes": {}
	}
	
	for row in data:
		vehicle = row.license_plate
		if vehicle not in summary["vehicles"]:
			summary["vehicles"][vehicle] = {
				"distance": 0,
				"fuel": 0,
				"cost": 0,
				"trips": 0
			}
		
		# Update vehicle metrics
		summary["vehicles"][vehicle]["distance"] += flt(row.distance)
		summary["vehicles"][vehicle]["fuel"] += flt(row.fuel_qty)
		summary["vehicles"][vehicle]["cost"] += flt(row.total_amount)
		summary["vehicles"][vehicle]["trips"] += 1
		
		# Update total metrics
		summary["total_distance"] += flt(row.distance)
		summary["total_fuel"] += flt(row.fuel_qty)
		summary["total_cost"] += flt(row.total_amount)
		
		# Track routes
		route = f"{row.from_location} -> {row.to_location}"
		summary["routes"][route] = summary["routes"].get(route, 0) + 1
	
	return summary

def generate_chart_data(summary_data):
	"""Generate chart data for visualizations"""
	charts = {
		"distance_chart": {
			"data": {
				"labels": list(summary_data["vehicles"].keys()),
				"datasets": [{
					"name": _("Distance Traveled"),
					"values": [v["distance"] for v in summary_data["vehicles"].values()]
				}]
			},
			"type": "bar",
			"height": 300
		},
		"fuel_consumption_chart": {
			"data": {
				"labels": list(summary_data["vehicles"].keys()),
				"datasets": [{
					"name": _("Fuel Consumed"),
					"values": [v["fuel"] for v in summary_data["vehicles"].values()]
				}]
			},
			"type": "bar",
			"height": 300
		},
		"cost_distribution_chart": {
			"data": {
				"labels": list(summary_data["vehicles"].keys()),
				"datasets": [{
					"name": _("Fuel Cost"),
					"values": [v["cost"] for v in summary_data["vehicles"].values()]
				}]
			},
			"type": "pie",
			"height": 300
		}
	}
	
	return charts