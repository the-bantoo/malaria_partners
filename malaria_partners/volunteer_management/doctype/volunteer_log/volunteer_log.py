# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days, date_diff


class VolunteerLog(Document):
    def validate(self):
        if self.days_spent < 1:
            frappe.throw("The number of <strong>Days Spent</strong> cannot be less than 1 day")
        if self.start_date > self.end_date:
            frappe.throw("The <strong>End Date</strong> cannot be before the <strong>Start Date</strong>")
    def before_save(self):
        self.calculate_time_spent()
        
    @frappe.whitelist()
    def set_end_date(self):
        if self.start_date and self.days_spent:
            # Calculate end_date based on start_date and days_spent
            self.end_date = add_days(self.start_date, self.days_spent - 1)

    @frappe.whitelist()
    def set_days_spent(self):
        if self.start_date and self.end_date:
            # Calculate days_spent based on start_date and end_date
            days_spent = date_diff(self.end_date, self.start_date) + 1
            if days_spent < 1:
                frappe.throw("The number of <strong>Days Spent</strong> cannot be less than 1 day")
                self.days_spent = 0
            self.days_spent = days_spent

    @frappe.whitelist()
    def calculate_time_spent(self):
        if self.manually_set_time_spent == 1:
            return
        if self.days_spent:
            settings = frappe.get_doc("Volunteer Settings", "Volunteer Settings")     
            calculate_days_spent = self.days_spent * settings.standard_work_hours * 60 * 60 # in seconds

            if self.days_spent != calculate_days_spent:
                self.time_spent = calculate_days_spent
