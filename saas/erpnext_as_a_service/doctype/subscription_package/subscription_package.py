# Copyright (c) 2022, Africlouds Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt

class SubscriptionPackage(Document):
	def validate(self):
		if flt(self.default_storage_space) == 0:
			frappe.throw(_("Default Storage Space is mandatory for Subscrption Package"), frappe.MandatoryError, title=_("Missing Fields"))
		
		if flt(self.available_users) == 0:
			frappe.throw(_("Available Users is mandatory for Subscrption Package"), frappe.MandatoryError, title=_("Missing Fields"))
		
		self.check_allowed_modules_in_package()
	
	def check_allowed_modules_in_package(self):
		pass
		
