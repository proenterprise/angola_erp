# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

import angola_erp
from angola_erp.util.cambios import cambios
from angola_erp.util.angola import get_lista_retencoes
from angola_erp.util.angola import get_taxa_retencao
from angola_erp.util.angola import get_taxa_ipc
from angola_erp.util.angola import get_taxa_iva

import erpnext

from frappe.utils import money_in_words, flt, cint
from frappe.utils import cstr, getdate, date_diff
## from erpnext.setup.utils import get_company_currency
from num2words import num2words

from erpnext.stock.get_item_details import get_batch_qty

import os 
from datetime import datetime

from subprocess import Popen, PIPE

import angola_erp.util.saft_ao

####
# Helkyd modified 24-04-2019
####

ultimoreghash = None

def validate(doc,method):
	
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"

	taxavenda= cambios("BNA")
	lista_retencoes = get_lista_retencoes()
	lista_retencao = get_taxa_retencao()
	lista_impostos = get_taxa_ipc()

	lista_iva = get_taxa_iva()

	temretencao = False 
	temimpostoconsumo = False 
	retencaofonte =0
	retencaopercentagem =0
	totalpararetencao = 0
	totalgeralimpostoconsumo = 0
	totalgeralretencaofonte = 0
	totalbaseretencaofonte = 0
	retencaofonteDESC = ""
	totalservicos_retencaofonte =0
	totaldespesas_noretencaofonte =0
	totaldescontos_linha = 0

	impostoselotransit = []
	totalimpostoselotrans = 0
	impostoselotranspercentagem = 0
	metadedovalor = False

	percentagem = 0
	
	percentagemiva = 0
	totalgeraliva = 0
	
	ii=0

	numISelo = 0	#contador Imposto de Selo

	for x in lista_retencoes:
		if x.descricao.upper() =='Retencao na Fonte'.upper():
			print ('pertagem ', x.percentagem)
			retencaopercentagem = x.percentagem
		elif (x.descricao.upper() =='IPC'.upper()) or (x.descricao.upper() =='Imposto de Consumo'.upper()):
			print ('IPC % ', x.percentagem)
			percentagem = x.percentagem
		elif ('Imposto de Selo'.upper() in x.descricao.upper()):

			print ('Imposto de Selo % ', x.percentagem)
			print (x.descricao)
			print ('metade '), x.metade_do_valor
			impostoselotransit.append([x.descricao, x.percentagem, x.metade_do_valor])

			#impostoselotranspercentagem = x.percentagem
			#if (x.metade_do_valor):
			#	metadedovalor = True	

		elif (x.descricao.upper() =='IVA'.upper()) or ("Imposto Valor Acrescentado".upper() == x.descricao.upper() or 'Acrescentado'.upper() in x.descricao.upper()):
			print ('IVA % ', x.percentagem)
			percentagemiva = x.percentagem




	for i in doc.get("items"):			
		if i.item_code != None:
			prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte,imposto_de_selo,que_imposto_de_selo FROM `tabItem` WHERE item_code = %s """, i.item_code , as_dict=True)
			if prod[0].imposto_de_consumo ==1:
				print ("IMPOSTO CONSUMO")
				if percentagem == 0:
					i.imposto_de_consumo = (i.amount * 5) / 100
				else:
					i.imposto_de_consumo = (i.amount * percentagem) / 100
				
			if prod[0].retencao_na_fonte ==1:
				print ("RETENCAO FONTE")
				i.retencao_na_fonte = (i.amount * retencaopercentagem) / 100
				totalbaseretencaofonte += i.amount
				totalservicos_retencaofonte += totalbaseretencaofonte
			else:
				totaldespesas_noretencaofonte += i.amount		

			if prod[0].imposto_de_selo ==1:
				print ("IMPOSTO DE SELO TRANS")
				print ("IMPOSTO DE SELO TRANS")
				for x1 in impostoselotransit:
					print 'loop no imposto selo'
					print x1
					print x1[0]
					print x1[1]
					print x1[2]
					if x1[0] == prod[0].que_imposto_de_selo:
						print 'Imposto CORRETO!!!!!'
						print 'Imposto CORRETO!!!!!'
						print 'Imposto CORRETO!!!!!'

						if x1[2] == 1:	#metade do valor TRUE
							print 'METADE DO VALOR!!!'
							metadedovalor = True
						else:
							metadedovalor = False

						impostoselotranspercentagem = x1[1]
						
						print (flt(i.amount) * x1[1])
						print ('Selo % ',((i.amount * impostoselotranspercentagem) / 100))
						break
				print 'continua....'
				print metadedovalor
				#i.retencao_na_fonte = (i.amount * retencaopercentagem) / 100
				if (metadedovalor):
					totalimpostoselotrans += ((i.amount/2) * impostoselotranspercentagem) / 100
					i.imposto_de_selo_trans = ((i.amount/2) * impostoselotranspercentagem) / 100
				else:
					totalimpostoselotrans += (i.amount * impostoselotranspercentagem) / 100
					i.imposto_de_selo_trans = (i.amount * impostoselotranspercentagem) / 100
				print totalimpostoselotrans

			if prod[0].iva_isencao == 0:	#TEM IVA	
				print "IVA IVA"
				print "IVA IVA"
				

			totalgeralimpostoconsumo += i.imposto_de_consumo					
			totalgeralretencaofonte +=  i.retencao_na_fonte

			#BATCH Qty 
			if i.warehouse and i.item_code and i.batch_no:
				print 'BATCH NO verifica a QTD'
				print i.batch_no
				print i.warehouse
				print i.item_code
				print ('qtd atual ', i.actual_qty)
				print get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']
				#print get_batch_qty(i.warehouse,i.item_code)['actual_batch_qty']
				#for xx in get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']:
				#	print "LISTA BATCHES....."
				#	print xx

				i.actual_batch_qty = get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']
				if i.actual_qty == 0:
					print 'ACTUAL QTY ZEROOOOOOOO'
					#i.actual_qty = get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']

	
			#Total Desconto Linha
			if i.margin_type == "Percentage":
				totaldescontos_linha += i.amount

	#Save retencao na INVoice 
	doc.total_retencao_na_fonte = totalgeralretencaofonte
	doc.base_retencao_fonte = totalbaseretencaofonte

	#Save Descontos linha
	doc.total_desconto_linha = totaldescontos_linha

	#Save Imposto de Selo Trans
	doc.total_imposto_selo_trans = totalimpostoselotrans

	#Calcula_despesas Ticked
	
	iii=0
	print ("Despesas")
	for ai in doc.get("taxes"):
		if ai.parent == doc.name and ai.charge_type !="":
			if ai.calcula_despesas:
				totalgeralimpostoconsumo = 0
				if totaldespesas_noretencaofonte ==0:
					#recalcula
					print ("RECALCULA")
					print ("RECALCULA")
					print ("RECALCULA")
					if (ai.rate == 0) and (percentagem == 0) :
						percentagem = 5
					else:
						percentagem = ai.rate

					for aii in doc.get("items"):
						if aii.parent == doc.name:
							prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, aii.item_code , as_dict=True)					

							#if (iii==0){iii=0}
							
							if prod[0].imposto_de_consumo == 1:

								if aii.imposto_de_consumo == 0:
									print ""
								
								if aii.retencao_na_fonte == 1:
										
									totalgeralretencaofonte +=  (aii.amount * retencaopercentagem) / 100
									totalbaseretencaofonte += aii.amount
									totalservicos_retencaofonte += totalbaseretencaofonte

								totalgeralimpostoconsumo += aii.imposto_de_consumo					


								despesas = (percentagem * totaldespesas_noretencaofonte)/100
								print percentagem
								print totaldespesas_noretencaofonte
								print despesas
								print totalgeralimpostoconsumo
								print ai.account_head

								ai.charge_type="Actual"
								#ai.tax_amount=despesas
								ai.tax_amount = despesas #totalgeralimpostoconsumo 
							else:
								ai.tax_amount = 0




				else:
					print ("CALCULA DESPESAS")
					print ("CALCULA DESPESAS")
					print ("CALCULA DESPESAS")
					if (ai.rate == 0) and (percentagem == 0) :
						percentagem = 5
					else:
						percentagem = ai.rate

					despesas = (ai.rate * totaldespesas_noretencaofonte)/100

					print percentagem
					print totaldespesas_noretencaofonte
					print despesas

					print totalgeralimpostoconsumo
					if despesas != totalgeralimpostoconsumo:

						ai.charge_type = "Actual"
						ai.tax_amount = totalgeralimpostoconsumo

					else:
						ai.charge_type = "Actual"
						ai.tax_amount = despesas
			elif "34220000" in ai.account_head: #IVA
				print "TEM IVA......"
				print "TEM IVA......"
				print "TEM IVA......"
				print "TEM IVA......"

				for aii in doc.get("items"):
					if aii.parent == doc.name:
						prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte,iva_isencao FROM `tabItem` WHERE item_code = %s """, aii.item_code , as_dict=True)					

						#if (iii==0){iii=0}
						'''
						if prod[0].iva_isencao == 0:	#Has IVA

							if aii.imposto_de_consumo == 0:
								print ""
							'''
						#	if aii.retencao_na_fonte == 1:
									
						#		totalgeralretencaofonte +=  (aii.amount * retencaopercentagem) / 100
						#		totalbaseretencaofonte += aii.amount
						#		totalservicos_retencaofonte += totalbaseretencaofonte
						'''
						totalgeralimpostoconsumo += aii.imposto_de_consumo					


						despesas = (percentagem * totaldespesas_noretencaofonte)/100
						print percentagem
						print totaldespesas_noretencaofonte
						print despesas
						print totalgeralimpostoconsumo
						print ai.account_head

						ai.charge_type="Actual"
						#ai.tax_amount=despesas
						ai.tax_amount = despesas #totalgeralimpostoconsumo 
						'''
						if prod[0].iva_isencao == 1:	#NO NO IVA
							print "sem iva ", prod[0].item_code
							ai.charge_type="Actual"
							ai.tax_amount = totalgeraliva
							ai.total = totalgeraliva + doc.net_total

						elif prod[0].iva_isencao == 0:	#IVA
							print "IVA"
							print "IVA ", aii.item_code
							print aii.amount
							print percentagemiva
							totalgeraliva += (aii.amount * percentagemiva)/100
							if ai.charge_type == "Actual":
								ai.tax_amount = totalgeraliva
								ai.total = totalgeraliva + doc.net_total
				
						else:
							ai.tax_amount = 0


			else:
				print "SEM DESPESAS MAS CALCULA IPC"
				print "SEM DESPESAS MAS CALCULA IPC"
				ai.charge_type = "Actual"
				ai.tax_amount = totalgeralimpostoconsumo
				ai.total = totalgeralimpostoconsumo + doc.net_total




	print "VALOR POR EXTENSO"

	print totalgeralimpostoconsumo

	#Save Total Taxes and Charges if IPC exists
	if totalgeralimpostoconsumo:
		if doc.currency == "KZ":
			doc.base_total_taxes_and_charges = totalgeralimpostoconsumo
			doc.total_taxes_and_charges = totalgeralimpostoconsumo
		if not doc.additional_discount_percentage:	
			doc.grand_total = totalgeralimpostoconsumo + doc.net_total
			doc.rounded_total = doc.grand_total
			doc.base_grand_total = doc.grand_total
			doc.base_rounded_total = doc.grand_total
			doc.outstanding_amount = doc.grand_total
	elif totalgeraliva:
		#IVA
		print "iva nos TOTAIS"
		if doc.currency == "KZ":
			doc.base_total_taxes_and_charges = totalgeraliva
			doc.total_taxes_and_charges = totalgeraliva
			print 'totalgeraliva ', totalgeraliva
		if not doc.additional_discount_percentage:
			doc.grand_total = totalgeraliva + doc.net_total
			print 'totalgeraliva + net total ', totalgeraliva + doc.net_total
			doc.rounded_total = doc.grand_total
			print 'Grand total ', doc.grand_total
			doc.base_grand_total = doc.grand_total
			doc.base_rounded_total = doc.grand_total
			doc.outstanding_amount = doc.grand_total
		

		print "Rouding ....."
		print "Rouding ....."
		print doc.base_rounding_adjustment
		#print 'tem centimos ',str(doc.base_rounding_adjustment).find('.')
		#if str(doc.base_rounding_adjustment).find('.'):
		#	doc.base_rounding_adjustment = round(doc.base_rounding_adjustment)

	company_currency = erpnext.get_company_currency(doc.company)
	print company_currency
	if (company_currency =='KZ'):
		doc.in_words = num2words(doc.rounded_total, lang='pt_BR').title() + ' Kwanzas.'
	else:
		doc.in_words = money_in_words(doc.rounded_total, company_currency)

	
	ultimodoc = frappe.db.sql(""" select max(name),creation,docstatus,hash_erp,hashcontrol_erp from `tabSales Invoice` where (docstatus = 1 or docstatus = 2)  and hash_erp <> '' """,as_dict=True)
	print 'VALIDARrrrrrrrrrrrrrrrrrr'
	print ultimodoc
	global ultimoreghash
	ultimoreghash = ultimodoc

def before_submit(doc,method):

	#Fees to be paid by Sales Invoice
	for prop_ in doc.get("propina"):
		frappe.db.set_value("Fees",prop_.propina, "sales_invoice", doc.name)
		#frappe.db.set_value("Fees",prop_.propina, "outstanding_amount", 0)
		frappe.db.commit()

	if doc.po_no:
		if len(doc.po_no) > 140:
			print("RETIRA As PO aqui ....")
			doc.po_no = ""


	#HASH and HASH CONTROL...
	fileregisto = "registo"
	fileregistocontador = 1	#sera sempre aqui 

	#get the last doc generated 
	print 'verifica se ja tem o registo'
	print 'verifica se ja tem o registo' 
	print ultimoreghash

	if ultimoreghash:
		ultimodoc = ultimoreghash
	else:
		#ultimodoc = frappe.db.sql(""" select max(name),creation,modified,posting_date,hash_erp,hashcontrol_erp from `tabSales Invoice` """,as_dict=True)
		ultimodoc = frappe.db.sql(""" select name,creation,modified,posting_date,hash_erp,hashcontrol_erp from `tabSales Invoice` where creation = (select max(creation) from `tabSales Invoice`) """,as_dict=True)
		


	criado = datetime.strptime(doc.creation,'%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%dT%H:%M:%S") 
	
	print 'ULTIMO HASH.....'
	print ultimodoc
#	print ultimodoc[0].hash_erp
	if ultimodoc[0].hash_erp == "" or ultimodoc[0].hash_erp == None:
		#1st record
		print 'primeiro registo HASH'
		#print doc.posting_date.strftime("%Y-%m-%d")

		print doc.creation	
		print criado
		hashinfo = str(doc.posting_date) + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";"
	else:
		print 'segundo registo'
		#print chaveanterior
		hashinfo = str(doc.posting_date)  + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";" + str(ultimodoc[0].hash_erp)


#	hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
#	hashfile.write(hashinfo)

	#to generate the HASH
#	angola_erp.util.saft_ao.assinar_ssl()
	print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
#	os.system("/usr/bin/python /tmp/angolaerp.cert2/assinar_ssl.py")	
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	#print angola_erp.util.saft_ao.assinar_ssl1(hashinfo)
	 

#	p = Popen(["/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	p = Popen(["exec ~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	output, errors = p.communicate()
#	p.wait()
	print 'Openssl Signing...'
#	print output
#	print errors

#	hashfile.close()

	#Reads the file to save the HASH....
#	hashcriado = open('/tmp/registo1.b64','rb')	#open the file created to HASH
#	print 'Hash criado'
#	chaveanterior = str(hashcriado.read())	#para usar no next record...

	doc.hash_erp = str(angola_erp.util.saft_ao.assinar_ssl1(hashinfo))	#Hash created
	
#	hashcriado.close()
	
	#Deve no fim apagar todos os regis* criados ....
#	os.system("rm /tmp/registo* ")	#execute
	
def before_save(doc,method):
	#check if PO_NO lenght more than 140 chars
	if doc.po_no:
		if len(doc.po_no) > 140:
			print("RETIRA As PO aqui ....")
			doc.po_no = ""



def on_submit(doc,method):
	#check if PO_NO lenght more than 140 chars
	if doc.po_no:
		if len(doc.po_no) > 140:
			print("RETIRA As PO aqui ....")
			doc.po_no = ""


	#Imposto de Selo
	if doc.is_pos:
		print "Pagamento do IS no POS"
		print "Pagamento do IS no POS"
		print "Pagamento do IS no POS"
		print "Pagamento do IS no POS"
		print "Pagamento do IS no POS"

		global is_temp

		is_temp = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '7531%%'  """,(doc.company), as_dict=True)

		global is_

		is_ = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3471%%'  """,(doc.company), as_dict=True)

		global retencoes_is

		retencoes_is = frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor, isencao from `tabRetencoes` where name like 'imposto de selo' """,as_dict=True)

		centro_custo = frappe.get_value("Company",doc.company,"cost_center")


		gl_entries = []

		#for payment_mode in doc.payments:
		#	if payment_mode.amount:

		# POS, make payment entries
		print "Pagamento....CREDITO"
		print "Pagamento....CREDITO"
		print "Pagamento....CREDITO"

		gl_entries.append(
			doc.get_gl_dict({
				"account": is_[0].name,
				"against": is_temp[0].name,
				"credit": (doc.rounded_total * retencoes_is[0].percentagem) / 100,
				"credit_in_account_currency": (doc.rounded_total * retencoes_is[0].percentagem) / 100, 
				"cost_center": centro_custo,

				#"party_type": "Customer",
				#"party": self.customer,
				#"against": payment_mode.account,
				#"credit": payment_mode.base_amount,
				#"credit_in_account_currency": payment_mode.base_amount \
				#	if self.party_account_currency==self.company_currency \
				#	else payment_mode.amount,
				#"against_voucher": self.return_against if cint(self.is_return) else self.name,
				#"against_voucher_type": self.doctype,

			}, doc.party_account_currency)
		)

		#payment_mode_account_currency = get_account_currency(payment_mode.account)
		gl_entries.append(
			doc.get_gl_dict({

				"account": is_temp[0].name,
				"account_currency": is_temp[0].account_currency,
				"against": is_[0].name,
				"debit_in_account_currency": (doc.rounded_total * retencoes_is[0].percentagem) / 100,
				"debit": (doc.rounded_total * retencoes_is[0].percentagem) / 100,
				"cost_center": centro_custo,

				#"account": payment_mode.account,
				#"against": self.customer,
				#"debit": payment_mode.base_amount,
				#"debit_in_account_currency": payment_mode.base_amount \
				#	if payment_mode_account_currency==self.company_currency \
				#	else payment_mode.amount
			}, doc.party_account_currency)
		)

		if gl_entries:
			from erpnext.accounts.general_ledger import make_gl_entries

			# if POS and amount is written off, updating outstanding amt after posting all gl entries
			update_outstanding = "No" if (cint(doc.is_pos) or doc.write_off_account) else "Yes"

			make_gl_entries(gl_entries, cancel=(doc.docstatus == 2),
				update_outstanding=update_outstanding, merge_entries=False)

			#make_gl_entries(gl_entries, cancel=cancel, adv_adj=0)


	


