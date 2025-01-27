# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VolunteerProfile(Document):
	def validate(self):
		if not self.full_name:
			if f"{self.first_name} {self.last_name}" != self.full_name:
				self.full_name = f"{self.first_name} {self.last_name}"
