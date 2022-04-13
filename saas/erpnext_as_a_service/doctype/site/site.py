# -*- coding: utf-8 -*-
# Copyright (c) 2015, Africlouds Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
class Site(Document):
	def validate(self):
		subscrption_package = frappe.get_doc("Subscrption Package" ,self.subscrption_package)
		if self.storage_space < subscrption_package.default_storage_space:
			frappe.throw(f"Storage Space must be at least {subscrption_package.default_storage_space}")

		if self.number_users < subscrption_package.number_users:
			frappe.throw(f"Number of available users must be at least {subscrption_package.number_users}")