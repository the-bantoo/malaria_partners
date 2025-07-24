// Copyright (c) 2024, Fabric and contributors
// For license information, please see license.txt

frappe.query_reports["Volunteer Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
			"width": "100"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "100"
		},
		{
			"fieldname": "volunteer",
			"label": "Volunteer",
			"fieldtype": "Link",
			"options": "Volunteer Profile",
			"width": "100",
		},
		{
			"fieldname": "gender",
			"label": "Gender",
			"fieldtype": "Select",
			"options": ["", "Male", "Female"],
			"width": "100",
		},
		{
			"fieldname": "club_type",
			"label": "Club Type",
			"fieldtype": "Link",
			"options": "Club Type",
			"width": "100",
		},
		{
			"fieldname": "activity_supported",
			"label": "Activity",
			"fieldtype": "Link",
			"options": "Task",
			"width": "100",
		},
		{
			"fieldname": "district_supported",
			"label": "District",
			"fieldtype": "Link",
			"options": "Activity District",
			"width": "100",
		},
		{
			"fieldname": "group_by",
			"label": "Group By",
			"fieldtype": "Select",
			"options": ["", "Volunteer", "Gender", "Club", "Club Type", "Activity", "District"],
			"width": "100",
		}
	]
};
