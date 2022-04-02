// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site', {
	refresh: function(frm) {
		frm.add_custom_button(__('Send confirmation email'), function(){
			frm.trigger("send_confirmation_email")

		}, __("Actions"));
		frm.add_custom_button(__('Create site'), function(){
			frm.trigger("create_site")

		}, __("Actions"));
		frm.add_custom_button(__('Delete Site'), function(){
			frm.trigger("delete_site")

		}, __("Actions"));
		frm.add_custom_button(__('Verify account'), function(){
			console.log("SSsss	")
			frm.trigger("verify_account")

		}, __("Actions"));

	},
	send_confirmation_email: function(frm) {
		if (frm.doc.status==="Pending Approval"){
			frappe.call({
				method: "saas.api.send_invitation_emails",
				args: {
					site: frm.doc.name
				},
				callback: function(r){
					console.log(String(r))

				}
			})
		}
	},
	create_site: function(frm){
		frappe.call({
			method:"saas.api.create_site",
			args: {
				site: frm.doc.name
			},
			callback: function(r){
				console.log(String(r))
			}
		})
	},
	delete_site: function(frm){
		frappe.call({
			method:"saas.api.delete_site",
			args: {
				site: frm.doc.name
			},
			callback: function(r){
				console.log(String(r))
			}
		})
	},

	verify_account: function(frm){
		frappe.call({
			method:"saas.api.verify_account",
			args: {
				name: frm.doc.name,
				code : frm.doc.email_verification_code
			},
			callback: function(r){
				console.log(String(r))
			}
		})
	},
});
