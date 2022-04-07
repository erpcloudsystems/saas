// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site', {
	refresh: function(frm) {
		frm.add_custom_button(__('Create site'), function(){
			frm.trigger("create_site")
			// frm.trigger("set_config_site")

		});
		
		frm.add_custom_button(__('Delete Site'), function(){
			frm.trigger("delete_site")

		});

		frm.add_custom_button(__('Notify Client'), function(){
			frm.trigger("notify_client")

		});

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
	notify_client: function(frm){
		frappe.call({
			method:"saas.api.notify_client",
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
				name: frm.doc.name
			},
			callback: function(r){
				console.log(String(r))
			}
		})
	},
	set_config_site: function(frm) {
		frappe.call({
			method: "saas.api.set_config_site",
			args: {
				site: frm.doc.name
			},
			callback: function(r){
				console.log(String(r))

			}
		})
},
});
