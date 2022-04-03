import frappe
from frappe import _
import string
import random
from frappe.utils.background_jobs import enqueue
import subprocess

def id_generator(size=50, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def delete_account(doc, method):
    site = frappe.get_doc("Site", doc.name)
    enqueue(delete_site, site=site)

@frappe.whitelist()
def create_site(site):
    site = frappe.get_doc("Site", site)
    cmd = ["bench", "new-site", "--db-name", site.name, "--mariadb-root-username", "root", "--mariadb-root-password", '123', "--admin-password", "logic", "--install-app", "erpnext", site.title]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        # cwd="/home/frappe/frappe-bench"
                                        cwd="/home/kamal/work/v13/saas")
    out,err = p.communicate()
    if not err:
        """Create an orientation meeting when a new User is added"""
        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": site.title,
            "email_id": site.email,
            "status": "Lead"
        })
        # the System Manager might not have permission to create a Meeting
        lead.flags.ignore_permissions = True
        lead.insert()

@frappe.whitelist()
def notify_client(site):
    site = frappe.get_doc("Site", site)
    frappe.sendmail(
    recipients = [site.email],
    sender="arwema@gmail.com",
    subject="Your ERP Account",
    message = "Dear Customer, your account has been create and accessible from: http://%s:8000" % (site.title),
    reference_doctype=site.doctype,
    reference_name=site.name
    )

@frappe.whitelist()
def delete_site(name):
    site = frappe.get_doc("Site", name)
    cmd = ["bench", "drop-site","--root-password", '123', site.title]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        cwd="/home/kamal/work/v13/saas")
    out,err = p.communicate()
    if not err:
        lead = frappe.get_doc("Lead", site.title)
        lead.flags.ignore_permissions = True
        lead.status = "Do Not Contact"
        lead.save()