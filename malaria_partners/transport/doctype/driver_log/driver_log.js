// Copyright (c) 2025, Fabric and contributors
// For license information, please see license.txt

frappe.ui.form.on("Driver Log", {
    setup(frm){
        
    },
    validate(frm){
        if (frm.doc.from[0].places === frm.doc.to[0].places){
            // let to_places = frm.doc.to.map((row) => row.places);
            //  || to_places.includes(frm.doc.from.places
            frappe.throw({
                message: `The <strong>From</strong> location and the <strong>To</strong> location cannot be the same`, 
                indicator: 'red'
            });
        }
    },
    from(frm){
        if (frm.doc.from.length > 1){
            frm.set_value("from", [{places: frm.doc.from[0].places}]);
            frm.refresh_field("from");
            frappe.show_alert({
                message: `Only <strong>${frm.doc.from[0].places}</strong> has been used as <strong>From</strong> location`, 
                indicator: 'yellow'
            }, 3)
        }
    },
	refresh: function (frm) {
		if (frm.doc.docstatus == 0 && frm.is_new()) {
            // if(!frm.doc.employee){
                frappe.call({
                    method: "malaria_partners.transport.doctype.driver_log.driver_log.get_defaults",
                    callback: function(r){
                        console.log('result', r, r.message['employee_name'])
                        if (r.message){
                            if (r.message['employee_name'] && !frm.doc.employee){
                                frm.set_value("employee", r.message.employee_name);
                                frm.refresh_field("employee");
                            }
                            if (r.message['last_vehicle']){
                                frm.set_value("license_plate", r.message.last_vehicle);
                                frm.refresh_field("license_plate");
                            }
                            if (r.message['last_location']){
                                frm.set_value("from", [{places: r.message.last_location}]);
                                frm.refresh_field("from");
                            }
                        }
                    }
                });
            // }
		}
	},
    fuel_qty: function (frm) {
        calc_amt(frm);
    },
    price: function (frm) {
        calc_amt(frm);
    }
});

function calc_amt(frm){
    frm.set_value("total_amount", parseFloat(frm.doc.fuel_qty) * parseFloat(frm.doc.price));
    frm.refresh_field("total_amount");
}
