import frappe

# def daily():
#     expireds = frappe.get_list(
#         'Customer System',
#         filters={
#             'status': ['<>', 'Expired'],
#             'subscription_end_date': ['>', frappe.utils.nowdate()]
#         })