# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt
from frappe import _
import frappe


def execute(filters=None):
    return get_columns(filters), get_data(filters)
def get_data(filters):
    conditions = []

    if filters.get('volunteer'):
        conditions.append(f"vl.volunteer = '{filters.get('volunteer')}'")
    if filters.get('gender'):
        conditions.append(f"v.gender = '{filters.get('gender')}'")
    if filters.get('club_type'):
        conditions.append(f"vl.club_type = '{filters.get('club_type')}'")
    if filters.get('position'):
        conditions.append(f"vl.club_position = '{filters.get('position')}'")
    if filters.get('activity_supported'):
        conditions.append(f"vl.activity_supported = '{filters.get('activity_supported')}'")
    if filters.get('district_supported'):
        conditions.append(f"vl.district_supported = '{filters.get('district_supported')}'")
        
    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = "WHERE " + conditions_sql

    group_by_field = filters.get('group_by')
    group_by_sql = ""
    select_fields = ["vl.start_date as start_date",
                    "vl.full_name as volunteer", "v.gender as gender", "vl.nrcid as nrcid", "act.subject as activity", "vl.district_supported as district", 
                    "vl.club_position as club_position", "vl.club_type as club_type", "vl.club as club", 
                    "vl.days_spent AS days_spent", "vl.time_spent as total_hours"]

    if group_by_field:
        if group_by_field == "Volunteer":
            group_by_sql = "GROUP BY vl.volunteer"
            select_fields = ["vl.full_name as volunteer", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
        elif group_by_field == "Gender":
            group_by_sql = "GROUP BY v.gender"
            select_fields = ["v.gender as gender", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
        elif group_by_field == "Club":
            group_by_sql = "GROUP BY vl.club"
            select_fields = ["vl.club as club", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
        elif group_by_field == "Club Type":
            group_by_sql = "GROUP BY vl.club_type"
            select_fields = ["vl.club_type as club_type", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
        elif group_by_field == "Activity":
            group_by_sql = "GROUP BY vl.activity_supported"
            select_fields = ["act.subject as activity", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
        elif group_by_field == "District":
            group_by_sql = "GROUP BY vl.district_supported"
            select_fields = ["vl.district_supported as district", "sum(vl.days_spent) as days_spent", "sum(vl.time_spent) as total_hours"]
    
    select_fields_sql = ", ".join(select_fields)

    query = f"""SELECT {select_fields_sql}
                FROM `tabVolunteer Log` as vl
                JOIN `tabVolunteer Profile` AS v 
                ON vl.volunteer = v.name
                LEFT JOIN `tabTask` AS act 
                ON vl.activity_supported = act.name
                {conditions_sql}
                {group_by_sql}
                ORDER BY vl.start_date
            """
    
    frappe.errprint(query)
    data = frappe.db.sql(query, as_dict=1)

    return data

def get_columns(filters):
    group_by_field = filters.get('group_by')
    columns = [
            {"label": _("Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
			{"label": _("Volunteer"), "fieldname": "volunteer", "fieldtype": "Data", "width": 200},
			{"label": _("Sex"), "fieldname": "gender", "fieldtype": "Data", "width": 70},
			{"label": _("NRC/ID"), "fieldname": "nrcid", "fieldtype": "Data", "width": 120},
			{"label": _("Activity"), "fieldname": "activity", "fieldtype": "Data", "width": 300},
			{"label": _("District"), "fieldname": "district", "fieldtype": "Data", "width": 120},
            {"label": _("Position"), "fieldname": "club_position", "fieldtype": "Data", "width": 90},
			{"label": _("Club"), "fieldname": "club", "fieldtype": "Data", "width": 230},
			{"label": _("Days Spent"), "fieldname": "days_spent", "fieldtype": "Data", "width": 70},
			{"label": _("Hours"), "fieldname": "total_hours", "fieldtype": "Duration", "width": 100},
		]
    
    if group_by_field:
        if group_by_field == "Volunteer":
            columns = [
			    {"label": _("Volunteer"), "fieldname": "volunteer", "fieldtype": "Link", "options": "Volunteer Profile", "width": 300}
            ]
        elif group_by_field == "Gender":
            columns = [
			    {"label": _("Gender"), "fieldname": "gender", "fieldtype": "Data", "width": 300}
            ]
        elif group_by_field == "Club":
            columns = [
			    {"label": _("Club"), "fieldname": "club", "fieldtype": "Data", "width": 300}
            ]
        elif group_by_field == "Club Type":
            columns = [
			    {"label": _("Club Type"), "fieldname": "club_type", "fieldtype": "Data", "width": 300}
            ]
        elif group_by_field == "Activity":
            columns = [
			    {"label": _("Activity"), "fieldname": "activity", "fieldtype": "Data", "width": 300}
            ]
        elif group_by_field == "District":
            columns = [
			    {"label": _("District"), "fieldname": "district", "fieldtype": "Data", "width": 300}
            ]
        columns = columns + [
            {"label": _("Days Spent"), "fieldname": "days_spent", "fieldtype": "Data", "width": 200},
            {"label": _("Total Hours Spent"), "fieldname": "total_hours", "fieldtype": "Duration", "width": 200}
        ]

    return columns