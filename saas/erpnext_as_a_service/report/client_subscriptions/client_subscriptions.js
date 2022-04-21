// Copyright (c) 2022, Africlouds Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Client Subscriptions"] = {
	"filters": [
		{
			"label": __("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"label": __("From Date"),
			"fieldname":"from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
    	{
			"label": __("To Date"),
			"fieldname":"to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), 1)
		},
	]
};
