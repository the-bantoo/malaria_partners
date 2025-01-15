// Copyright (c) 2025, Fabric and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Usage Report"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "license_plate",
            label: __("Vehicle"),
            fieldtype: "Link",
            options: "Vehicle"
        },
        {
            fieldname: "employee",
            label: __("Employee"),
            fieldtype: "Link",
            options: "Employee",
            get_query: function() {
                return {
                    filters: {
                        'status': 'Active'
                    }
                };
            }
        },
        {
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project",
            get_query: function() {
                return {
                    filters: {
                        'status': 'Open'
                    }
                };
            }
        },
        {
            fieldname: "group_by",
            label: __("Group By"),
            fieldtype: "Select",
            options: [
                { value: "", label: __("") },
                { value: "license_plate", label: __("Vehicle") },
                { value: "employee", label: __("Employee") },
                { value: "project", label: __("Project") }
            ],
            default: ""
        },
        // {
        //     fieldname: "show_chart_data",
        //     label: __("Show Charts"),
        //     fieldtype: "Check",
        //     default: 1
        // }
    ],

    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // if (column.fieldname == "fuel_efficiency" && data.fuel_efficiency < 5) {
        //     value = `<span style="color: red">${value}</span>`;
        // }
        if ( data && column.fieldname == "distance") {
			if (data.distance > 500) {
            	value = `<span style="color: orange">${value}</span>`;
			}
        }

        return value;
    },

    // get_datatable_options(options) {
    //     return Object.assign(options, {
    //         scrollY: '500px',
    //         scrollX: true,
    //         scrollCollapse: true,
    //         fixedColumns: {
    //             leftColumns: 2
    //         }
    //     });
    // },

    // after_datatable_render: function(datatable_obj) {
    //     // Add any custom logic after the datatable is rendered
    //     $(datatable_obj.wrapper).find('.dt-scrollable').css('height', '500px');
    // },

    // refresh: function(frm) {
    //     // Add any custom refresh logic
    //     frm.trigger('update_totals');
    // },

    // update_totals: function(frm) {
    //     // Calculate and update totals in the footer
    //     if (frm.data && frm.data.length) {
    //         let totals = {
    //             distance: 0,
    //             fuel_qty: 0,
    //             total_amount: 0
    //         };

    //         frm.data.forEach(row => {
    //             totals.distance += flt(row.distance);
    //             totals.fuel_qty += flt(row.fuel_qty);
    //             totals.total_amount += flt(row.total_amount);
    //         });

    //         // Update footer rows
    //         frm.datatable.updateRow(frm.datatable.getRowCount() - 1, {
    //             distance: totals.distance,
    //             fuel_qty: totals.fuel_qty,
    //             total_amount: totals.total_amount
    //         });
    //     }
    // }
};