// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

var contracto_
var contractoS_ = cur_frm.call({method:"angola_erp.util.angola.get_all_contracto_numero",args:{}})

frappe.ui.form.on('Ficha Tecnica da Viatura', {

	onload: function(frm) {
		cur_frm.fields_dict['matricula_veiculo'].get_query = function(doc){
			return{
				filters:{
					"veiculo_alugado":1,
					"entrada_ou_saida":"Stand-by",
				},
				
			}
		}	

	},
	refresh: function(frm) {
		if (contracto_ != undefined){
			console.log('para analisar se ainda preicsa...')
			if (contracto_.statusCode == 'Ok'){
				if (contracto_.responseJSON.message != undefined){
					cur_frm.doc.contracto_numero = contracto_.responseJSON.message.contracto_numero
					cur_frm.doc.estacao_viatura = contracto_.responseJSON.message.local_de_saida
					cur_frm.doc.data_entrada_estacao = contracto_.responseJSON.message.devolucao_prevista
					cur_frm.doc.data_saida_estacao = contracto_.responseJSON.message.data_de_saida			
					cur_frm.refresh_fields('contracto_numero')
				}
			}
		}

	},



});

frappe.ui.form.on('Ficha Tecnica da Viatura','matricula_veiculo',function(frm,cdt,cdn){

	if (cur_frm.doc.matricula_veiculo != undefined) {
		cur_frm.toggle_enable("operador",false)
		frappe.model.set_value(cdt,cdn,'operador',frappe.session.user)

		contracto_ = cur_frm.call({method:"angola_erp.util.angola.get_contracto_numero",args:{"matricula":cur_frm.doc.matricula_veiculo}})
		veiculos_('Vehicle',cur_frm.doc.matricula_veiculo)
	
		if (contractoS_ != undefined){

			for (x in contractoS_.responseJSON.message) {
				if (contractoS_.responseJSON.message[x].matricula == cur_frm.doc.matricula_veiculo) {
					console.log("ENCONTROU A MATRICULA")
					cur_frm.doc.contracto_numero = contractoS_.responseJSON.message[x].contracto_numero
					cur_frm.doc.estacao_viatura = contractoS_.responseJSON.message[x].local_de_saida
					cur_frm.doc.data_entrada_estacao = contractoS_.responseJSON.message[x].devolucao_prevista
					cur_frm.doc.data_saida_estacao = contractoS_.responseJSON.message[x].data_de_saida
					cur_frm.doc.kms_saida = contractoS_.responseJSON.message[x].kms_out
					cur_frm.doc.combustivel_saida = contractoS_.responseJSON.message[x].deposito_out
					cur_frm.doc.tipo_combustivel = contractoS_.responseJSON.message[x].combustivel
					cur_frm.refresh_fields('contracto_numero')

				}
			}
		}

		cur_frm.refresh_fields('marca_veiculo');
		cur_frm.trigger('entrada_ou_saida_viatura')
	}
});


frappe.ui.form.on('Ficha Tecnica da Viatura','entrada_ou_saida_viatura',function(frm,cdt,cdn){
	//if saida all checked 1 otherwise 0

	if (cur_frm.doc.entrada_ou_saida_viatura == 'Saida'){
		frappe.model.set_value(cdt,cdn,'documentos_viatura',1)
		frappe.model.set_value(cdt,cdn,'radio_viatura',1)
		frappe.model.set_value(cdt,cdn,'antena_viatura',1)
		frappe.model.set_value(cdt,cdn,'isqueiro_viatura',1)
		frappe.model.set_value(cdt,cdn,'cinzeiro_viatura',1)
		frappe.model.set_value(cdt,cdn,'vidros_viatura',1)
		frappe.model.set_value(cdt,cdn,'triangulo_viatura',1)
		frappe.model.set_value(cdt,cdn,'penu_suplente',1)
		frappe.model.set_value(cdt,cdn,'tapetes_viatura',1)
		frappe.model.set_value(cdt,cdn,'tampoes_viatura',1)
		frappe.model.set_value(cdt,cdn,'pneus_viatura',1)
		frappe.model.set_value(cdt,cdn,'pintura_viatura',1)
		frappe.model.set_value(cdt,cdn,'chapa_viatura',1)
		frappe.model.set_value(cdt,cdn,'estofo_manchado',1)
		frappe.model.set_value(cdt,cdn,'estofo_queimado',1)


	}else {
		//entrada
		frappe.model.set_value(cdt,cdn,'documentos_viatura',0)
		frappe.model.set_value(cdt,cdn,'radio_viatura',0)
		frappe.model.set_value(cdt,cdn,'antena_viatura',0)
		frappe.model.set_value(cdt,cdn,'isqueiro_viatura',0)
		frappe.model.set_value(cdt,cdn,'cinzeiro_viatura',0)
		frappe.model.set_value(cdt,cdn,'vidros_viatura',0)
		frappe.model.set_value(cdt,cdn,'triangulo_viatura',0)
		frappe.model.set_value(cdt,cdn,'penu_suplente',0)
		frappe.model.set_value(cdt,cdn,'tapetes_viatura',0)
		frappe.model.set_value(cdt,cdn,'tampoes_viatura',0)
		frappe.model.set_value(cdt,cdn,'pneus_viatura',0)
		frappe.model.set_value(cdt,cdn,'pintura_viatura',0)
		frappe.model.set_value(cdt,cdn,'chapa_viatura',0)
		frappe.model.set_value(cdt,cdn,'estofo_manchado',0)
		frappe.model.set_value(cdt,cdn,'estofo_queimado',0)

	}

});



var veiculos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var carro = frappe.model.get_doc(frm,cdt)
		if (carro){
			cur_frm.doc.marca_veiculo = carro.make
			cur_frm.doc.modelo_veiculo = carro.model
			cur_frm.doc.cor_veiculo = carro.color
			//cur_frm.doc.combustivel = carro.fuel_type

		}
		
		cur_frm.refresh_fields();

	});


}

