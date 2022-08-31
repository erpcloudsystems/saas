import frappe
from frappe import _
import string
import random
from frappe.utils.background_jobs import enqueue
import subprocess
import os
import json
from frappe.installer import update_site_config
from frappe.model.document import Document
from frappe.utils import getdate, get_bench_path

def id_generator(size=50, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def delete_account(doc, method):
    site = frappe.get_doc("Site", doc.name)
    enqueue(delete_site, site=site)

@frappe.whitelist()
def create_site(site):
    cmd = ["bench", "new-site", "--db-name", self.title, "--mariadb-root-username", "root", "--mariadb-root-password", 'password', "--admin-password", "logic", "--install-app", "erpnext", self.title]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        cwd=get_bench_path())
    out,err = p.communicate()
    set_config_site(site.name)
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
    site.site_created = 1
    site.save()

@frappe.whitelist()
def notify_client(site):
    site = frappe.get_doc("Site", site)
    frappe.sendmail(
    recipients = [site.email_address],
    sender="arwema@gmail.com",
    subject="Your ERP Account",
    message = "Dear Customer, your account has been create and accessible from: http://%s:8000" % (site.title),
    reference_doctype=site.doctype,
    reference_name=site.name
    )

@frappe.whitelist()
def delete_site(name):
    site = frappe.get_doc("Site", name)
    cmd = ["bench", "drop-site","--root-password", 'password', site.title]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        cwd=get_bench_path())
    out,err = p.communicate()
    if not err:
        frappe.sendmail(
            recipients = [site.email],
            sender="arwema@gmail.com",
            subject="Your ERP Account Terminated",
            message = "Dear Customer, your account has been terminated",
            reference_doctype=site.doctype,
            reference_name=site.name
        )
        lead = frappe.get_doc("Lead", site.title)
        lead.flags.ignore_permissions = True
        lead.status = "Do Not Contact"
        lead.save()
    site.site_deleted = 1
    site.save()

@frappe.whitelist()
def set_config_site(site):
    site = frappe.get_doc("Site", site)
    subscrption_package = frappe.get_doc("Subscrption Package", site.subscrption_package)
    sites_path = os.getcwd()
    site_config_path = os.path.join(sites_path, f'{site.title}/site_config.json')
    update_site_config('package_title',subscrption_package.package_title,site_config_path = site_config_path)
    update_site_config('package_type',subscrption_package.package_type,site_config_path = site_config_path)
    update_site_config('definition_departments',subscrption_package.definition_departments,site_config_path = site_config_path)
    update_site_config('definition_branches',subscrption_package.definition_branches,site_config_path = site_config_path)
    update_site_config('possibility_adding',subscrption_package.possibility_adding,site_config_path = site_config_path)
    update_site_config('employees_personal_data',subscrption_package.employees_personal_data,site_config_path = site_config_path)
    update_site_config('define_limitations',subscrption_package.define_limitations,site_config_path = site_config_path)
    update_site_config('vacations',subscrption_package.vacations,site_config_path = site_config_path)
    update_site_config('social_insurance',subscrption_package.social_insurance,site_config_path = site_config_path)
    update_site_config('payroll_management',subscrption_package.payroll_management,site_config_path = site_config_path)
    update_site_config('attendance_departure',subscrption_package.attendance_departure,site_config_path = site_config_path)
    update_site_config('managing_custody',subscrption_package.managing_custody,site_config_path = site_config_path)
    update_site_config('payment_service',subscrption_package.payment_service,site_config_path = site_config_path)
    update_site_config('archiving_management',subscrption_package.archiving_management,site_config_path = site_config_path)
    update_site_config('reports',subscrption_package.reports,site_config_path = site_config_path)
    update_site_config('speeches',subscrption_package.speeches,site_config_path = site_config_path)
    update_site_config('report_generator',subscrption_package.report_generator,site_config_path = site_config_path)
    update_site_config('self_service',subscrption_package.self_service,site_config_path = site_config_path)
    update_site_config('electronic_forms',subscrption_package.electronic_forms,site_config_path = site_config_path)
    update_site_config('vehicle_management',subscrption_package.vehicle_management,site_config_path = site_config_path)
    update_site_config('employment_department',subscrption_package.employment_department,site_config_path = site_config_path)
    update_site_config('manage_control',subscrption_package.manage_control,site_config_path = site_config_path)
    update_site_config('possibility_add_users',subscrption_package.possibility_add_users,site_config_path = site_config_path)
    update_site_config('possibility_add_space',subscrption_package.possibility_add_space,site_config_path = site_config_path)
    update_site_config('technical_support',subscrption_package.technical_support,site_config_path = site_config_path)
    update_site_config('staff_evaluation',subscrption_package.staff_evaluation,site_config_path = site_config_path)
    update_site_config('user_activity_log',subscrption_package.user_activity_log,site_config_path = site_config_path)
    update_site_config('subscription_start_date',str(site.subscription_start_date),site_config_path = site_config_path)
    update_site_config('subscription_end_date',str(site.subscription_end_date),site_config_path = site_config_path)
    update_site_config('activate_fingerprint_devices',site.activate_fingerprint_devices,site_config_path = site_config_path)
    update_site_config('number_of_available_attendance_devices',site.number_devices,site_config_path = site_config_path)
    update_site_config('storage_space',site.storage_space,site_config_path = site_config_path)
    update_site_config('used_file_space',0,site_config_path = site_config_path)
    update_site_config('available_users',site.number_users,site_config_path = site_config_path)
    update_site_config('company',site.company,site_config_path = site_config_path)
    update_site_config('company_limit',site.number_companies,site_config_path = site_config_path)
    update_site_config("skip_setup_wizard",1,site_config_path = site_config_path)


@frappe.whitelist(allow_guest=True)
def open_client_issue(*args, **kwargs):
    if len(args) == 1: data = args[0]
    elif kwargs: data = kwargs
    fields = ('subject', 'issue_type', 'issue_date', 'company_name', 'user_name', 'user_email', 'description', 'name', 'ticket_url')
    new_issue = frappe.new_doc('Client Issue')
    for k, v in data.items():
        if k in fields:
            if k == 'name':
                k = 'tech_support_name'
            new_issue.update({
                k: v or ''
            })
    new_issue.flags.ignore_mandatory = True
    new_issue.save(ignore_permissions=True)
    new_issue.submit()
    frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def create_client_issue(*args, **kwargs):
    if len(args) == 1: data = args[0]
    elif kwargs: data = kwargs
    fields = ['subject', 'issue_type', 'issue_date', 'company_name', 'user_name', 'user_email', 'description', 'name', 'ticket_url']
    new_issue = frappe.new_doc('Client Issue')
    for k, v in data.items():
        if k in fields:
            if k == 'name':
                k = 'tech_support_name'
            new_issue.update({
                k: v or ''
            })
    new_issue.flags.ignore_mandatory = True
    new_issue.save(ignore_permissions=True)
    new_issue.submit()
    frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def complete_client_issue(*args, **kwargs):
    
    name = kwargs.get('name', False)
    if not name: return
    for ci in frappe.get_list('Client Issue', filters={'status': 'Open', 'docstatus': 1, 'tech_support_name': name}):
        ci = frappe.get_doc('Client Issue', ci.name)
        ci.mark_complete(check_user=False)
