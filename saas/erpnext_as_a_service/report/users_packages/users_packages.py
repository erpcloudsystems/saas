# Copyright (c) 2013, Africlouds Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from multiprocessing import Condition


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("User"),
            "options": "Customer",
            "fieldname": "user",
            "fieldtype": "Link",
            "width": 140
        },
        {
            "label": _("Package"),
            "options": "Subscrption Package",
            "fieldname": "package",
            "fieldtype": "Link",
            "width": 160
        }
    ]

    return columns

def get_data(filters):
    conditions = get_conditions(filters)

    result = frappe.db.sql("""
        SELECT 
            si.customer as user, si.subscrption_package as package
        FROM 
            `tabSite` as si
        WHERE
            {}
    """.format(conditions), as_dict=True)

    return result

    

def get_conditions(filters):
    conditions = "1=1"
    
    if filters.get("user"):
        conditions += " and si.customer = '{}'".format(filters.get("user"))
    
    if filters.get("package"):
        conditions += " and si.subscrption_package = '{}'".format(filters.get("package"))

    return conditions