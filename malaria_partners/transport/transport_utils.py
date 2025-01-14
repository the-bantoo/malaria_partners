import frappe

@frappe.whitelist()
def updated_odometer_value(vehical, new_odometer_value):
    check_permissions()
    frappe.db.set_value('Vehicle', vehical, 'last_odometer', new_odometer_value)

def check_permissions():
    if not frappe.has_permission('Vehicle', 'write'):
        frappe.throw('You do not have permission to update the odometer.')