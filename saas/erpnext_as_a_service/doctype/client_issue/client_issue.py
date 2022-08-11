# Copyright (c) 2022, AnvilERP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClientIssue(Document):
	def validate(self):
		if self.docstatus == 0: self.subject_title = self.subject
	def on_cancel(self):
		self.db_set('status', 'Cancelled')
	def on_submit(self):
		self.db_set('status', 'Open')

	def mark_complete(self, check_user=True):
		if check_user:
			u = frappe.get_doc('User', frappe.session.user)
			if 'Complete Tech Support' not in [r.role for r in u.roles]:
				frappe.msgprint(frappe._("Not allowed to complete Technical Support"))
				return

		if self.docstatus == 1 and self.status == "Open":
			self.db_set('status', 'Completed')
			return "Completed"
