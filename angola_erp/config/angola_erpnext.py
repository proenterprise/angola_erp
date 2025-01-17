from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Configuracao"),
			"items": [
				 {
				   "description": "INSS", 
				   "name": "INSS", 
				   "type": "doctype"
				  }, 

				{
				   "type": "doctype", 
				   "description": "IRT", 
				   "name": "IRT", 
				  },

				{
				   "type": "doctype", 
				   "description": "Subsidios", 
				   "name": "Subsidios", 
				  },
				{
				   "type": "doctype", 
				   "description": "Retencoes", 
				   "name": "Retencoes", 
				  },
				{
				   "type": "doctype", 
				   "description": "IVA Isencoes", 
				   "name": "Isencoes", 
				  },


			]
		},
		{
			"label": _("Configuracao"),
			"items": [
				 {
				   "description": "App Theme", 
				   "name": "App Theme", 
				   "type": "doctype"
				  }, 
				{
				   "type": "doctype", 
				   "description": "Atualizacao Cambios", 
				   "name": "Atualizacao Cambios", 
				  },


			]
		},

		{
			"label": _("Seguradoras - Saude - Clinicas"),
			"items": [
				 {
				   "description": "Lista de Seguradoras", 
				   "name": "Seguradoras", 
				   "type": "doctype"
				  }, 
				{
				   "type": "doctype", 
				   "description": "Planos das Seguradoras", 
				   "name": "Seguradora Planos", 
				  },


			]
		},


		{
			"label": _("Relatorios RH"),
			"items": [
				 {
				   "description": "Folha de Pagamento Banco", 
				   "name": "Folha de Pagamento Banco", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Folha de Salario I", 
				   "name": "Folha de Salario I", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Folha de Salarios", 
				   "name": "Folha de Salarios", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "INSS", 
				   "name": "Salary INSS", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "INSS by Salary Structure", 
				   "name": "Salary INSS by Salary Structure", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "IRT", 
				   "name": "Salary IRT", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Salary Review", 
				   "name": "Salary Review", 
				   "doctype": "Salary Slip",
				   "type": "report",
				   "is_query_report": True
				  }, 


			]
		},

		{
			"label": _("Relatorio Vendas"),
			"items": [
				 {
				   "description": "Imposto de Consumo", 
				   "name": "Imposto de Consumo", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Imposto de Selo", 
				   "name": "Imposto de Selo", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Imposto de Selo Detalhe", 
				   "name": "Imposto de Selo Detalhe", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Imposto Industrial", 
				   "name": "Imposto Industrial", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Imposto Industrial Detalhe", 
				   "name": "Imposto Industrial Detalhe", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Registo de Vendas", 
				   "name": "Registo de Vendas", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Registo de Vendas Somas", 
				   "name": "Registo de Vendas Somas", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Registo de Vendas (Somas Diaria)", 
				   "name": "Registo de Vendas (Somas Diaria)", 
				   "doctype": "Sales Invoice",
				   "type": "report",
				   "is_query_report": True
				  }, 



			]
		},


		{
			"label": _("Relatorio Stocks/Inventario"),
			"items": [

				 {
				   "description": "Lotes data de Expiracao", 
				   "name": "Lotes data de Expiracao", 
				   "doctype": "Stock Ledger Entry",
				   "type": "report",
				   "is_query_report": True
				  }, 


			]
		},

		{
			"label": _("Ficheiro SAFT-AO"),
			"items": [

				 {
				   "description": "Download do Ficheiro SAFT-AO", 
				   "name": "saft-ao", 
				   "label": "SAFT-AO", 					
				   "type": "page"
				  }, 


			]
		},
	]
