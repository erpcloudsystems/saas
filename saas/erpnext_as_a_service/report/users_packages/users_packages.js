// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Users Packages"] = {
	"filters": [
		{
			"fieldname": "user",
			"label": __("User"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "package",
			"label": __("Package"),
			"fieldtype": "Link",
			"options":"Subscrption Package"
		},
	]
};
