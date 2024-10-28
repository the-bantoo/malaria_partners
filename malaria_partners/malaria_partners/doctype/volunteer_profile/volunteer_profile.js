// Copyright (c) 2024, Fabric and contributors
// For license information, please see license.txt

frappe.ui.form.on("Volunteer Profile", {
	refresh(frm) {

	},
    validate(frm) {
        frm.doc.full_name = frm.doc.first_name + " " + frm.doc.last_name;
        console.log('namef', frm.doc.full_name);
    }
});
