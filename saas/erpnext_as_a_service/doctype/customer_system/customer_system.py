# -*- coding: utf-8 -*-
# Copyright (c) 2015, Africlouds Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from codecs import ignore_errors
import subprocess
import os
import shutil

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt, cint, get_bench_path
from frappe.utils.background_jobs import enqueue

from saas.api import write_site_config
from frappe.installer import update_site_config

class CustomerSystem(Document):
    def validate(self):
        self.validate_system_attributes()
        self.validate_subscription_package()

    def validate_system_attributes(self):
        if cint(self.available_companies) == 1:
            self.available_companies = 1

        if cint(self.available_users) == 1:
            self.available_users = 1

        if self.activate_fingerprint in ['Yes', 'نعم']:
            self.available_devices = 1

    def validate_subscription_package(self):
        subscrption_package = frappe.get_doc("Subscription Package" ,self.subscription_package)
        if flt(self.storage_space) == 0 or flt(self.storage_space) < flt(subscrption_package.default_storage_space):
            frappe.throw(_("Storage Space must be at least {}".format(subscrption_package.default_storage_space)))

        if cint(self.available_users) == 0 or cint(self.available_users) < cint(subscrption_package.available_users):
            frappe.throw(_("Number of available users must be at least {} user(s)".format(subscrption_package.available_users)))

    @frappe.whitelist()
    def create_site(self, db_pass, admin_pass, user_pass):
        if not isinstance(db_pass ,str): db_pass=""
        if not isinstance(admin_pass ,str): admin_pass=""
        if not isinstance(user_pass ,str): user_pass=""
        if len(admin_pass) == 0 or len(db_pass) == 0 or len(user_pass) == 0:
            frappe.throw(_("Can not create site without Database/Administrator passwords"))
            return
        
        if self.docstatus != 1:
            frappe.throw(_("Submite the form before create customer site"))
            return

        if self.status not in ['Pending', 'Email Sent', 'Site Verified', 'Creation Error']:
            frappe.throw(_("Can not create site for {} site".format(self.status)))
            return

        # check sites in the system
        used_sites_names = list(filter(lambda x: x not in ['apps.txt', 'currentsite.txt', 'common_site_config.json'], os.listdir(get_bench_path()+'/sites')))
        if self.title in used_sites_names:
            frappe.throw(_('Site {} already exists'.format(self.title)))
            return
        
        self.db_set('status', 'Creation In Process', update_modified=False)
        config = self.get_config_site()
        config.update({
            'admin_user_pass': "{}".format(user_pass),
            "support_pass": "{}".format(admin_pass)
        })
        enqueue(create_site_job, site_doc=self, site_name=self.title, db_user='root', db_pass=db_pass, admin_pass=admin_pass, config=config)
        return 'In Process'

    @frappe.whitelist()
    def delete_site(self, db_pass, admin_pass, confirm_msg, force=False):
        if self.status not in ['Pending', 'Created', 'Suspended', 'Email Sent', 'Site Verified']:
            frappe.throw(_("can not delete site for {} site".format(self.status)))
            return

        from frappe.utils.password import check_password
        try:
            user = check_password(frappe.session.user, admin_pass)
        except:
            frappe.throw(_("Incorrect user / database password"))
            return
        default_conf = "delete {}".format(self.title)
        if confirm_msg != default_conf:
            frappe.throw(_("To confirm deletion, type <i>{}</i> in the confirmation message".format(default_conf)))
        
        self.db_set('status', 'Deletion In Process', update_modified=False)
        enqueue(delete_site_job, site_doc=self, site_name=self.title, db_user='root', db_pass=db_pass)
        return "Delete"
    
    @frappe.whitelist()
    def suspend_site(self, confirm_msg, admin_pass, logout_all_users=True):
        from frappe.utils.password import check_password
        try:
            user = check_password(frappe.session.user, admin_pass)
        except:
            frappe.throw(_("Incorrect user password"))
            return
        default_conf = "suspend {}".format(self.title)
        if confirm_msg != default_conf:
            frappe.throw(_("To confirm deletion, type <i>{}</i> in the confirmation message".format(default_conf)))
            return
        
        self.db_set('status', 'Stoping In Process', update_modified=False)
        enqueue(stoping_site_job, site_doc=self, site_name=self.title)
        return "Stoping"
    
    @frappe.whitelist()
    def resume_site(self, admin_pass, logout_all_users=True):
        from frappe.utils.password import check_password
        try:
            user = check_password(frappe.session.user, admin_pass)
        except:
            frappe.throw(_("Incorrect user password"))
            return
        self.db_set('status', 'Resuming In Process', update_modified=False)
        enqueue(resume_site_job, site_doc=self, site_name=self.title)
        return "Resuming"
        
    def restart_site(self, confirm_msg, from_date, to_date):
        pass
    
    def get_config_site(self):
        sp = frappe.get_doc("Subscription Package", self.subscription_package)
        config = {}
        config.update({
            'package_type': sp.package_type,
            'default_storage_space': sp.default_storage_space,
            'allow_to_update_storage': sp.allow_to_update_storage,
            'available_users': sp.available_users,
            'allow_to_add_users': sp.allow_to_add_users,
            'manage_more_than_one_company': sp.manage_more_than_one_company,
            'archive_and_document_management': sp.archive_and_document_management,
            'reports': sp.reports,
            'enable_saas': 1,
            'custody_management': sp.custody_management,
            'letters': sp.letters,
            'define_departments': sp.define_departments,
            'define_branches': sp.define_branches,
            'contract_managements': sp.contract_managements,
            'vehicle_management': sp.vehicle_management,
            'training_management': sp.training_management,
            'define_employees_and_personal_details': sp.define_employees_and_personal_details,
            'social_insurance': sp.social_insurance,
            'employment_management': sp.employment_management,
            'self_service': sp.self_service,
            'employee_performance_evaluation': sp.employee_performance_evaluation,
            'payroll_management': sp.payroll_management,
            'end_of_service_and_dues': sp.end_of_service_and_dues,
            'leaves_management': sp.leaves_management,
            'attendance_departure': sp.attendance_departure,
            'role_and_permissions_management': sp.role_and_permissions_management,
            'user_logs': sp.user_logs,
            'report_generator': sp.report_generator,
            'electronic_forms': sp.electronic_forms,
            'company': self.company,
            'mobile_number': self.mobile_number,
            'email_address': self.email_address,
            'subscription_start_date': self.subscription_start_date,
            'subscription_end_date': self.subscription_end_date,
            'storage_space': self.storage_space,
            'activate_fingerprint': self.activate_fingerprint,
            'available_devices': self.available_devices,
            'actual_available_users': self.available_users,
            'available_companies': self.available_companies,
            'maintenance_mode': 0,
            'is_suspended': 0,
            'abbr': self.abbr,
            'country': self.country,
            'currency': self.currency,
            'customer': self.customer_lead,
        })
        return config

def create_site_job(site_doc, site_name, db_user, db_pass, admin_pass, config):
    for k, v in config.items():
        write_site_config(site_name, f'{k}', v,)
    admin_pass = f"{admin_pass}"
    cmd = [
        "bench", "new-site",
        "--db-name", site_name,
        "--mariadb-root-username", db_user,
        "--mariadb-root-password", db_pass,
        "--admin-password", admin_pass,
        "--install-app", "erpnext",
        "--install-app", "mosyr",
        "--install-app", "saas_manager",
        "--install-app", "mosyr_theme",
        site_name
    ]
    
    try:
        p = subprocess.run(cmd,
            capture_output=True,
            cwd=get_bench_path()
        )
        if p.returncode != 0:
            raise Exception("Faild To Create Site {}\n\n{}".format(site_name, p.stderr))
    except Exception as e:
        site_doc.db_set('status', 'Creation Error', update_modified=False)
        frappe.log_error(e, "Faild To Create Site")
        clean_failed_site_creation(site_name, db_pass)
    else:
        # Everything works as expected
        site_doc.db_set('status', 'Created', update_modified=False)
        create_logs(site_doc.name, 'Create')
        config_path = os.path.join(get_bench_path(), 'sites', site_doc.title, "site_config.json")
        for k, v in config.items():
            if k in ['admin_user_pass', 'support_pass']: continue
            update_site_config(f'{k}', v, site_config_path=config_path)
        delete_saas_config(site_name)

def delete_site_job(site_doc, site_name, db_user, db_pass):
    cmd = ["bench", "drop-site","--root-password", db_pass, "--force", site_name]
    try:
        p = subprocess.run(cmd,
            capture_output=True,
            cwd=get_bench_path()
        )
        # if p.returncode != 0:
        #     raise Exception("Faild To Delete Site {}\n\n{}".format(site_name, p.stderr))
    except frappe.exceptions.IncorrectSitePath:
        site_doc.db_set('status', 'Deleted', update_modified=False)
        create_logs(site_doc.name, 'Delete')
    except Exception as e:
        site_doc.db_set('status', 'Deletion Error', update_modified=False)
        frappe.log_error(e, "Faild To Delete Site")
    else:
        # Everything works as expected
        site_doc.db_set('status', 'Deleted', update_modified=False)
        create_logs(site_doc.name, 'Delete')

def clean_failed_site_creation(site_name, db_pass):
    cmd = ["bench", "drop-site","--root-password", db_pass, site_name]
    try:
        # Try to delete from database
        p = subprocess.run(cmd,
            capture_output=True,
            cwd=get_bench_path()
        )
        delete_saas_config(site_name)
    except Exception as e:
        delete_saas_config(site_name)

    site_path = os.path.join(get_bench_path(), 'sites', site_name)
    try:
        # Try to delete site folder
        shutil.rmtree(site_path)
    except: pass

def stoping_site_job(site_doc, site_name):
    try:
        config_path = os.path.join(get_bench_path(), 'sites', site_name, "site_config.json")
        update_site_config('is_suspended', 1, site_config_path=config_path)
        # write_site_config(site_name, 'is_suspended', 1)
    except: pass
    site_doc.db_set('status', 'Suspended', update_modified=False)
    create_logs(site_doc.name, 'Stop')

def resume_site_job(site_doc, site_name):
    try:
        config_path = os.path.join(get_bench_path(), 'sites', site_name, "site_config.json")
        update_site_config('is_suspended', 0, site_config_path=config_path)
        # write_site_config(site_name, 'is_suspended', 0)
    except: pass
    site_doc.db_set('status', 'Created', update_modified=False)
    create_logs(site_doc.name, 'Resume')

def create_logs(site_doc_name, action):
    logs = frappe.new_doc('Customer System Log')
    logs.customer_system = site_doc_name
    logs.action = action
    logs.user = frappe.session.user
    logs.action_date = frappe.utils.now_datetime()
    logs.save(ignore_permissions=True)
    logs.submit()
    frappe.db.commit()

def delete_saas_config(site_name):
    """delete temp config"""
    import os
    from pathlib import Path
    site_config_path = os.path.join(get_bench_path(), 'sites', f"{site_name}.config.json")
    Path(site_config_path).unlink()
