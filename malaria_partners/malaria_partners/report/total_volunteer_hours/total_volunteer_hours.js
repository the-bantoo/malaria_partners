// Copyright (c) 2024, Fabric and contributors
// For license information, please see license.txt

frappe.query_reports["Total Volunteer Hours"] = {
	"filters": [
		{
			"fieldname": "volunteer",
			"label": "Member",
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
			"label": "Membership Type",
			"fieldtype": "Link",
			"options": "Club Type",
			"width": "100",
		},
		{
			"fieldname": "position",
			"label": "Club Position",
			"fieldtype": "Link",
			"options": "Volunteer Position Type",
			"width": "100",
		},
		{
			"fieldname": "activity_supported",
			"label": "Voluntary Activity",
			"fieldtype": "Link",
			"options": "Project",
			"width": "100",
		},
		{
			"fieldname": "district_supported",
			"label": "District",
			"fieldtype": "Link",
			"options": "Activity District",
			"width": "100",
		}

	]
};
