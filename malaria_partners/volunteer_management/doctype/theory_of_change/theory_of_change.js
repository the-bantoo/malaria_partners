// Copyright (c) 2024, Fabric and contributors
// For license information, please see license.txt

frappe.ui.form.on("Theory of Change", {
	refresh(frm) {
        frm.set_value("project_number", frm.doc.project_name);
	},

});
