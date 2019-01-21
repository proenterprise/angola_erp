// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Ficha Tecnica da Viatura'] = {
	add_fields: ["status_viatura","entrada_ou_saida_viatura","docstatus"],

	get_indicator: function(doc) {

		if (doc.entrada_ou_saida_viatura == "Entrada" ) {
			return [__(doc.entrada_ou_saida_viatura ), "green"]
		} else if (doc.entrada_ou_saida_viatura == "Saida" ) {
			return [__(doc.status_viatura ), "red"]
		} else if (doc.entrada_ou_saida_viatura== "Stand-by" ) {
			return [__(doc.entrada_ou_saida_viatura ), "orange"]
		
		}
	},
	colwidths: {"subject": 1, "indicator": 1.1},


};


