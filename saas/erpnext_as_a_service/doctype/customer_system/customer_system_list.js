// Copyright (c) 2016, Africlouds Ltd and contributors
// For license information, please see license.txt
let imports_in_progress = [];

frappe.listview_settings['Customer System'] = {
	onload(listview) {},
	get_indicator: function(doc) {
		var colors = {
			'Pending': 'blue',

			'Creation In Process': 'orange',
			'Deletion In Process': 'orange',
			'Stoping In Process': 'orange',

			'Created': 'green',
			
			'Creation Error': 'red',
			'Deletion Error': 'red',

			'Deleted': 'pink',
			'Suspended': 'pink'
		};
		let status = doc.status;
		return [__(status), colors[status], 'status,=,' + doc.status];
	},
	hide_name_column: true
};
