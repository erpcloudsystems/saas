import frappe

def _socketio_connector(doc, method):
    users = 12
    companies = 2
    
    frappe.publish_realtime("_socketio_connector", "{'message':'test','custom_app'}")