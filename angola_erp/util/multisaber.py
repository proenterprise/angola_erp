# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

#Date Changed: 24/05/2019

#Para corrigir os lancamentos...

from __future__ import unicode_literals

#from __future__ import unicode_literals
import sys
reload (sys)
sys.setdefaultencoding("utf-8")


from frappe.model.document import Document
import frappe.model
import frappe
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe import throw, _
from frappe.utils import formatdate, encode
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc

from frappe.email.doctype.email_group.email_group import add_subscribers

from frappe.contacts.doctype.address.address import get_company_address # for make_facturas_venda
from frappe.model.utils import get_fetch_values

import re

@frappe.whitelist()
def corrigir_jv_party():
	#Para corrigir as JVs que tem os Party Errados...

	Jvs = frappe.db.sql(""" SELECT name, parent, account, party from `tabJournal Entry Account` where account like '311%' """,as_dict=True)

	for jv in Jvs:
#		if "3112100341" in jv.account:
#			print jv.party[0:4]	
#			print jv.party[0:jv.party.find(" ")]
#			print jv.account

		if not "31121000" in jv.account:
#		print 'aa',jv.party.strip()[0:4]
			print jv.party
			print jv.name
#			print jv.party[0:jv.party.find(" ")]
			print jv.account

#		if re.search(" ", str(jv.party)):
#			  print "several words"

			nome = jv.party[0:jv.party.find(" ")]	
	#		print 'nome+', '*' + nome.strip()
			if not nome.upper() in jv.account.upper():
				print jv.parent + " - " + jv.account
				print jv.party
				print 'Nome'
				print jv.account[jv.account.find('-')+2:jv.account.rfind('-')-1]
				print jv.account.rfind('-')
				#Search on customer the parent name 
				clie = jv.account[jv.account.find('-')+2:jv.account.rfind('-')-1]
				cliente = frappe.db.sql(""" SELECT name from `tabCustomer` where name like %s """,(clie),as_dict=True)
				if cliente:
					print cliente
					print "Nome Cliente ", cliente[0].name
					cliente_party = frappe.db.sql(""" SELECT account, parent from `tabParty Account` where parent like %s """,(cliente[0].name),as_dict=True)

					print cliente_party[0].parent
					frappe.db.set_value('Journal Entry Account',jv.name,'party',cliente_party[0].parent)
					frappe.db.commit()
					print "ATUALIZADO !!!!"

					frappe.db.set_value('Journal Entry',jv.parent,'title',cliente_party[0].parent)
					frappe.db.set_value('Journal Entry',jv.parent,'pay_to_recd_from',cliente_party[0].parent)
					frappe.db.commit()
					print "JV ATUALIZADO !!!!"
			
					print jv.parent
					print jv.account
					gl = frappe.db.sql(""" SELECT name, voucher_no, account from `tabGL Entry` where voucher_no = %s and account = %s """,(jv.parent,jv.account),as_dict=True)

					print 'GL '
					print gl
					frappe.db.set_value('GL Entry',gl[0].name,'party',cliente_party[0].parent)
					frappe.db.commit()
					print "GL ATUALIZADO !!!!"

					gls = frappe.db.sql(""" SELECT name, voucher_no, account, against, credit, debit, party, party_type from `tabGL Entry` where voucher_no = %s """,(jv.parent),as_dict=True)
					#conta_against = ''
					for gl in gls:
						print 'AGAINST I'
						print gl.against
					
						#if gl.against and gl.credit and not gl.party:
						#	conta_against = gl.against.replace(jv.party,cliente[0].parent)
						if gl.against and gl.debit and not gl.party_type: 
							frappe.db.set_value('GL Entry',gl.name,'against',gl.against.replace(jv.party,cliente_party[0].parent))
							frappe.db.commit()
						elif gl.against and gl.credit: 
							print 'TEM NUMERO I'
							print 'TEM NUMERO I'
							print 'TEM NUMERO I'
							print 'TEM NUMERO I'

							print gl.against[0:1].isnumeric()
							if (gl.against[0:1].isnumeric() == False): 
								frappe.db.set_value('GL Entry',gl.name,'against',cliente_party[0].parent)
								frappe.db.commit()
						

				else:
					print "Nao encontrou...procura mais.."
					print "verifica a ficha do cliente com esta conta ..."
					cliente = frappe.db.sql(""" SELECT account, parent from `tabParty Account` where account like %s """,(jv.account),as_dict=True)
					if cliente:
						print "Encontrou a Conta na ficha do Cliente...."
						print cliente[0].parent
						frappe.db.set_value('Journal Entry Account',jv.name,'party',cliente[0].parent)
						frappe.db.commit()
						print "ATUALIZADO !!!!"

						frappe.db.set_value('Journal Entry',jv.parent,'title',cliente[0].parent)
						frappe.db.set_value('Journal Entry',jv.parent,'pay_to_recd_from',cliente[0].parent)
						frappe.db.commit()
						print "JV ATUALIZADO !!!!"
				
						print jv.parent
						print jv.account
						gl = frappe.db.sql(""" SELECT name, voucher_no, account from `tabGL Entry` where voucher_no = %s and account = %s """,(jv.parent,jv.account),as_dict=True)

						print 'GL '
						print gl
						frappe.db.set_value('GL Entry',gl[0].name,'party',cliente[0].parent)
						frappe.db.commit()
						print "GL ATUALIZADO !!!!"

						gls = frappe.db.sql(""" SELECT name, voucher_no, account, against, credit, debit, party, party_type from `tabGL Entry` where voucher_no = %s """,(jv.parent),as_dict=True)
						#conta_against = ''
						for gl in gls:
							print 'AGAINST'
							print gl.against
						
							#if gl.against and gl.credit and not gl.party:
							#	conta_against = gl.against.replace(jv.party,cliente[0].parent)
							if gl.against and gl.debit and not gl.party_type: 
								frappe.db.set_value('GL Entry',gl.name,'against',gl.against.replace(jv.party,cliente[0].parent))
								frappe.db.commit()
							elif gl.against and gl.credit: 
								print 'TEM NUMERO'
								print 'TEM NUMERO'
								print 'TEM NUMERO'
								print 'TEM NUMERO'

								print gl.against[0:1].isnumeric()
								if (gl.against[0:1].isnumeric() == False): 
									frappe.db.set_value('GL Entry',gl.name,'against',cliente[0].parent)
									frappe.db.commit()
							

					else:
						print "Nao encontrou...procura mais.."				

		#if "3112100341" in jv.account:
		#	return
