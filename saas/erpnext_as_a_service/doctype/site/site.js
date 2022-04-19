// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site', {
	refresh: function(frm) {
		frm.add_custom_button(__('Create site'), function(){
			frm.events.create_site(frm).then(data => {
				frm.trigger("set_config_site")
			})
		});
		if(frm.doc.site_created == 1){
			frm.remove_custom_button('Create site');
			frm.add_custom_button(__('Delete Site'), function(){
				frm.trigger("delete_site")
			});
		}
		if(frm.doc.site_deleted == 1){
			cur_frm.remove_custom_button('Delete Site');
		}
		frm.add_custom_button(__('Notify Client'), function(){
			frm.trigger("notify_client")
		});

	},
	create_site: function(frm){
		return frappe.call({
			method:"saas.api.create_site",
			args: {
				site: frm.doc.name
			},
			callback: function(r){
				frappe.msgprint(__("create site done"))
				location.reload()
			},
			freeze: true,
			freeze_message: __("start create site")
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
				location.reload()
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
