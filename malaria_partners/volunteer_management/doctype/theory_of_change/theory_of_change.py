# Copyright (c) 2024, Fabric and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TheoryofChange(Document):
	def before_insert(self):
		self.remove_totals_row()
	def validate(self):
		self.remove_totals_row()
		def get_column_total(col_name):
			return sum(getattr(row, col_name, 0) for row in self.budget)
		
	# check if totals row is present
		def totals_exists():
			return any(row.output_number == "Totals" for row in self.budget)

		if not totals_exists():
			self.append("budget", {
			"output_number": "Totals",
			"amended_budget": get_column_total("amended_budget"),
			"approved_annual_budget": get_column_total( "approved_annual_budget"),
			"carryf_yr1": get_column_total("carryf_yr1"),
			"total_budget": get_column_total("total_budget"),
			"actual_expenditure": get_column_total("actual_expenditure"),
			"budget_balance": get_column_total("budget_balance"),
			"additional_budget": get_column_total("additional_budget"),
			"actual_balance": get_column_total("actual_balance"),
			"ammended_budget": get_column_total("ammended_budget"),
		})
			
	def remove_totals_row(self):
	# Find and remove the "Totals" row if it exists
		self.budget = [row for row in self.budget if row.output_number != "Totals"]
