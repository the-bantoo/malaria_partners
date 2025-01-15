// Copyright (c) 2025, Fabric and contributors
// For license information, please see license.txt

frappe.listview_settings["Driver Log"] = {
    onload: function(listview) {
        // Get current workspace
        let workspace = 'Transport';
        
        frappe.breadcrumbs.all[frappe.get_route_str()] = {
            workspace: workspace,
            doctype: listview.doctype,
            type: 'List'
        };
        
        frappe.breadcrumbs.update();
    }
};