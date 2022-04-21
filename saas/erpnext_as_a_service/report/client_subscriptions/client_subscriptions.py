# Copyright (c) 2022, Africlouds Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": _("Customer Name"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 160
		},
		{
			"label": _("Copmany"),
			"fieldname": "copmany",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Email"),
			"fieldname": "email_address",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Mobile Number"),
			"fieldname": "mobile_number",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Subscrption Package"),
			"fieldname": "subscrption_package",
			"fieldtype": "Link",
			"options": "Subscrption Package",
			"width": 180
		},
		{
			"label": _("Start Date"),
			"fieldname": "subscription_start_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("End Date"),
			"fieldname": "subscription_end_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("Remaining Days"),
			"fieldname": "remaining_days",
			"fieldtype": "Int",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		}
	]
	return columns

def get_data(filters):

	conds = "1=1"
	if filters.get("customer"):
		conds = f"""customer='{filters.get("customer")}'"""

	sql =frappe.db.sql(""" 
				SELECT customer, company, email_address, mobile_number, subscrption_package, 
					subscription_start_date, subscription_end_date,
					IF(DATEDIFF(subscription_end_date, subscription_start_date) <=0, 0, DATEDIFF(subscription_end_date, subscription_start_date)) as remaining_days, status
				FROM tabSite
				WHERE {} AND subscription_start_date>=%s AND subscription_end_date<=%s
				""".format(conds), (filters.get("from_date"), filters.get("to_date")))
	return sql
# 