# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VolunteerSettings(Document):
    def validate(self):
        if self.standard_work_hours < 1:
            frappe.throw("<strong>Standard Work Hours</strong> cannot be less than 1 hour")
        if self.standard_work_hours > 23:
            frappe.throw("<strong>Standard Work Hours</strong> cannot be more than 23 hours")