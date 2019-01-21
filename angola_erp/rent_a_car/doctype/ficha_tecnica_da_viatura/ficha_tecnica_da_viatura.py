# -*- coding: utf-8 -*-
# Copyright (c) 2019, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import throw
from frappe.utils import formatdate, encode
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str

class FichaTecnicadaViatura(Document):

	def autoname(self):

		self.ficha_numero = make_autoname(self.naming_series)
		self.name = self.ficha_numero
		self.docstatus = 0
		frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Stand-by")
		frappe.db.commit()



	def validate(self):
		#validar 
		#tem que verificar se o vehicle esta em Stand-by... caso nao alguem ja alugou...
		is_free = frappe.get_doc("Vehicle",self.matricula_veiculo)
		if not is_free.entrada_ou_saida == "Stand-by":
			frappe.throw(_("Esta viatura já está alugada, não é possivel continuar!!!"))
			validated = False	

	def on_submit(self):

		self.docstatus = 1

		
	def on_cancel(self):
		#set the car leased on Vehicle so no one can rent....
		frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Entrada")
		frappe.db.commit()

		self.docstatus = 2	#cancela o submeter


	def before_submit(self):
		#set carro as Saida
		frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Saida")
		frappe.db.commit()

