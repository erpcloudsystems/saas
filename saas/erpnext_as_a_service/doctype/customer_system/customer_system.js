// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer System', {
    setup: function (frm) {
        if (!frm.doc.subscription_start_date) {
            frm.set_value('subscription_start_date', frappe.datetime.nowdate());
        }
    },
    refresh: function (frm) {
        frm.trigger('set_label')
        if (frm.doc.docstatus == 1) {
            if (["Pending Approval", "Email Sent", "Site Verified"].includes(frm.doc.status)) {
                frm.add_custom_button(__('Create site'), function () { frm.trigger("create_site") });
            }
            if(["Deletion Error"].includes(frm.doc.status)){
                frm.add_custom_button(__('Re-Delete site'), function () { frm.trigger("delete_site") });
            }
            if(["Creation Error"].includes(frm.doc.status)){
                frm.add_custom_button(__('Re-Create site'), function () { frm.trigger("create_site") });
                frm.add_custom_button(__('Delete site'), function () { frm.trigger("delete_site") });
            }
            if (frm.doc.status == "Pending Approval") {
                frm.add_custom_button(__('Notify Client'), function () { frm.trigger("notify_client") });
            }

            if (["Created"].includes(frm.doc.status)) {
                frm.add_custom_button(__('Delete site'), function () { frm.trigger("delete_site") });
                frm.add_custom_button(__('Suspend site'), function () { frm.trigger("suspend_site") });
            }
        }
    },
    create_site: function (frm) {
        let d = new frappe.ui.Dialog({
            title: __(`Create Site ${frm.doc.title}`),
            fields: [
                {
                    label: __('Database Password'),
                    fieldname: 'db_pass',
                    fieldtype: 'Password',
                    reqd: 1
                },
                {
                    label: __('Administrator Password (You can use another password)'),
                    fieldname: 'admin_pass',
                    fieldtype: 'Data',
                    reqd: 1,
                    default: generatePassword(),
                }
            ],
            primary_action_label: __(`Create`),
            primary_action(values) {
                if(values && values.db_pass && values.admin_pass){
                    cur_frm.events.call_api(frm, 'create_site', values, "start create site", "site created successfully")
                }
                d.hide();
            }
        });
        
        d.show();
    },
    notify_client: function (frm) {
        cur_frm.events.call_api(frm, 'notify_client', "send email to client", "client notified successfully")
    },
    delete_site: function (frm) {
        let d = new frappe.ui.Dialog({
            title: __(`Delete Site ${frm.doc.title}`),
            fields: [
                {
                    label: __('Database Password'),
                    fieldname: 'db_pass',
                    fieldtype: 'Password',
                    reqd: 1
                },
                {
                    label: __('User Password'),
                    fieldname: 'admin_pass',
                    fieldtype: 'Password',
                    reqd: 1,
                },
                {
                    label: __(`To confirm deletion, type <i>delete ${frm.doc.title}</i> in the field.`),
                    fieldname: 'confirm_msg',
                    fieldtype: 'Data',
                    reqd: 1,
                }
            ],
            primary_action_label: __(`Delete`),
            primary_action(values) {
                if(values && values.db_pass && values.admin_pass && values.confirm_msg){
                    cur_frm.events.call_api(frm, 'delete_site', values, "start delete site", "site deleted successfully")
                }
                d.hide();
            }
        });
        
        d.show();
    },
    // set_config_site: function (frm) {
    // 	frappe.call({
    // 		method: "saas.api.set_config_site",
    // 		args: {
    // 			site: frm.doc.name
    // 		},
    // 		callback: function (r) {
    // 			console.log(String(r))

    // 		}
    // 	})
    // },
    call_api: function(frm, api_method, args, freeze_msg, end_msg){
        if(!end_msg){
            end_msg = freeze_msg
        }
        return frappe.call({
            method: `${api_method}`,
            doc: frm.doc,
            args: args,
            // args: { site: frm.doc.name },
            callback: function (r) {
                // frappe.msgprint(__(end_msg))
                console.log(r)
                frm.reload_doc()
            },
            freeze: true,
            freeze_message: __(freeze_msg)
        })
    },
    customer_or_lead: function (frm) { frm.trigger('set_label') },
    set_label: function (frm) { cur_frm.set_df_property('customer_lead', 'label', __(frm.doc.customer_or_lead)) }
});

function generatePassword() {
    var length = 12,
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        retVal = "";
    for (var i = 0, n = charset.length; i < length; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
    }
    return retVal;
}