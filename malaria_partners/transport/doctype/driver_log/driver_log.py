# Copyright (c) 2025, Fabric and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class DriverLog(Document):
	def validate(self):
		if flt(self.odometer) < flt(self.last_odometer):
			frappe.throw(
				_("Current Odometer Value should be greater than Last Odometer Value {0}").format(
					self.last_odometer
				)
			)

	def on_submit(self):
		frappe.db.set_value("Vehicle", self.license_plate, "last_odometer", self.odometer)

	def on_cancel(self):
		distance_travelled = self.odometer - self.last_odometer
		if distance_travelled > 0:
			updated_odometer_value = (
				int(frappe.db.get_value("Vehicle", self.license_plate, "last_odometer")) - distance_travelled
			)
			frappe.db.set_value("Vehicle", self.license_plate, "last_odometer", updated_odometer_value)


@frappe.whitelist()
def get_defaults():
	employee_name = get_employee_from_user_id()
	last_log = frappe.get_last_doc("Driver Log")
	last_vehicle = False
	last_odometer = 0
	last_location = Falses

	if last_log:
		last_vehicle = last_log.license_plate
		last_odometer = last_log.odometer
		if last_plc_list := frappe.get_all("Places", filters={"parent": last_log.name, "parentfield": "to"}, fields=["*"], limit=1, order_by="creation desc" ):
			last_location = last_plc_list[0].places
			
	return {
		"employee_name": employee_name,
		"last_vehicle": last_vehicle,
		"last_odometer": last_odometer,
		"last_location": last_location,
	}



def get_employee_from_user_id(user_id=frappe.session.user):
	employee_list = frappe.db.sql("""
		select name from `tabEmployee`
		where user_id = %s
		OR personal_email = %s
		OR company_email = %s
	""", (user_id, user_id, user_id), as_dict=1)

	if not employee_list:
		return False
	return employee_list[0].name



@frappe.whitelist()
def make_expense_claim(docname):
	expense_claim = frappe.db.exists("Expense Claim", {"vehicle_log": docname})
	if expense_claim:
		frappe.throw(_("Expense Claim {0} already exists for the Vehicle Log").format(expense_claim))

	vehicle_log = frappe.get_doc("Driver Log", docname)
	service_expense = sum([flt(d.expense_amount) for d in vehicle_log.service_detail])

	claim_amount = service_expense + (flt(vehicle_log.price) * flt(vehicle_log.fuel_qty) or 1)
	if not claim_amount:
		frappe.throw(_("No additional expenses has been added"))

	exp_claim = frappe.new_doc("Expense Claim")
	exp_claim.employee = vehicle_log.employee
	exp_claim.vehicle_log = vehicle_log.name
	exp_claim.remark = _("Expense Claim for Vehicle Log {0}").format(vehicle_log.name)
	exp_claim.append(
		"expenses",
		{"expense_date": vehicle_log.date, "description": _("Vehicle Expenses"), "amount": claim_amount},
	)
	return exp_claim.as_dict()