// Copyright (c) 2025, Fabric and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fleet Settings", {
	refresh(frm) {
        let workspace = 'Transport';
            
        frappe.breadcrumbs.all[frappe.get_route_str()] = {
            workspace: workspace,
            doctype: frm.doctype,
            type: 'Form'
        };
        frappe.breadcrumbs.update();
	},
});
