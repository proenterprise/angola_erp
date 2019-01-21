// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Contractos Rent'] = {
	add_fields: ["status_contracto"],

	get_indicator: function(doc) {

		if (doc.status_contracto == "Activo" ) {
			return [__(doc.status_contracto ), "green"]
		} else if (doc.status_contracto == "Terminou" ) {
			return [__(doc.status_contracto ), "orage"]
		}
	},
	colwidths: {"subject": 1, "indicator": 1.1},



	
};


