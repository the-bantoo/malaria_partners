// Copyright (c) 2024, Fabric and contributors
// For license information, please see license.txt


frappe.ui.form.on("Volunteer Log", {
	refresh(frm) {

	},
    days_spent(frm){
        set_end_date(frm);
    },
    end_date(frm) {
        set_days_spent(frm);
    },
    start_date(frm){
        if (frm.doc.end_date || frm.doc.days_spent){             
            set_days_spent(frm);
        }
    }
});

function auto_calculate_time_spent(frm) {
    if (frm.doc.manually_set_time_spent === 1) {
        return;
    }
    frappe.call({
        method: "calculate_time_spent",
        doc: frm.doc,
        callback: function (r) {
            frm.refresh_field("volunteer_time");
        }
    })
}

function set_end_date(frm){
    frappe.call({
        method: "set_end_date",
        doc: frm.doc,
        callback: function (r) {
            frm.refresh_field("end_date");
            auto_calculate_time_spent(frm);
        }
    });
}

function set_days_spent(frm){
    frappe.call({
        method: "set_days_spent",
        doc: frm.doc,
        callback: function (r) {
            frm.refresh_field("days_spent");
            auto_calculate_time_spent(frm);
        }
    });
}
