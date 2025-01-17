# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import math
import datetime
import erpnext
from frappe import msgprint
from frappe.utils import money_in_words, flt
from frappe.utils import cstr, getdate, date_diff
from frappe.utils import formatdate, encode
## from erpnext.setup.utils import get_company_currency
from erpnext.hr.doctype.process_payroll.process_payroll import get_month_details
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from num2words import num2words

#from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.accounts.utils import get_fiscal_year

global diaspagamento, totaldiastrabalho, horasextra, trabalhouferiado 

def validate(doc,method):
#	get_edc(doc, method)
	gross_pay = 0
	net_pay = 0
	tot_ded = 0
	tot_cont = 0
	#dias_pagamento = 0


	if type(doc.start_date) == unicode:
		mes_startdate = datetime.datetime.strptime(doc.start_date,'%Y-%m-%d')
	else:
		mes_startdate = doc.start_date

	#Salva Payment Days e recalcula o IRT, INSS
	print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

	print doc.name , " + ", doc.employee, " + ", doc.start_date
	print 'Dias de pagamento e Working Days'
	print doc.payment_days, " + ", doc.total_working_days
	print doc.company.encode('utf-8')

#	if not doc.salary_slip_based_on_timesheet:

	#Falta Injustificada
	j= frappe.db.sql(""" SELECT count(status) from `tabAttendance` where employee = %s and status = 'Absent' and tipo_de_faltas = 'Falta Injustificada' and month(attendance_date) = %s and processar_mes_seguinte = 0 and year(attendance_date) = %s and docstatus=1 and company = %s """,(doc.employee,mes_startdate.month,mes_startdate.year,doc.company), as_dict=True)

	#Falta Justificada c/salario
	ja= frappe.db.sql(""" SELECT count(status) from `tabAttendance` where employee = %s and status = 'Absent' and tipo_de_faltas = 'Falta Justificada C/Salario' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 and company = %s """,(doc.employee,mes_startdate.month,mes_startdate.year,doc.company), as_dict=True)

	j1= frappe.db.sql(""" SELECT count(status) from `tabAttendance` where employee = %s and status = 'On leave' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 and company = %s """,(doc.employee,mes_startdate.month,mes_startdate.year, doc.company), as_dict=True)

	j2= frappe.db.sql(""" SELECT sum(numero_de_horas) as horas from `tabAttendance` where employee = %s and status = 'Present' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 and company = %s """,(doc.employee,mes_startdate.month,mes_startdate.year,doc.company), as_dict=True)

	#Half day Injustificada
	j3= frappe.db.sql(""" SELECT count(status) from `tabAttendance` where employee = %s and status = 'Half Day' and tipo_de_faltas = 'Falta Injustificada' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 and processar_mes_seguinte = 0 and company = %s """,(doc.employee,mes_startdate.month,mes_startdate.year,doc.company), as_dict=True)

	#Still need to COUNT for Present during Holiday
	fiscal_year = get_fiscal_year(doc.start_date, company=doc.company)[0]
	month = "%02d" % getdate(doc.start_date).month
	m = get_month_details(fiscal_year, month)


	#m = get_month_details(mes_startdate.year, mes_startdate.month)
	msd = m.month_start_date
	med = m.month_end_date
	print 'Mes start ', msd
	print 'Mes END ', med

	#Gets Faltas do previous month
	print month
	print int(month)-1
	prev_m = get_month_details(fiscal_year, int(month)-1)
	prev_msd = prev_m.month_start_date
	prev_med = prev_m.month_end_date

	print prev_msd
	print prev_med
	print mes_startdate.month

	j4= frappe.db.sql(""" SELECT count(status) from `tabAttendance` where employee = %s and (status = 'Half Day' or status = 'Absent') and tipo_de_faltas = 'Falta Injustificada' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 and processar_mes_seguinte = 1 and company = %s """,(doc.employee,int(month)-1,mes_startdate.year,doc.company), as_dict=True)
	
	print 'Faltas no mes anterior ', j4	

	holiday_list = get_holiday_list_for_employee(doc.employee)
	holidays = frappe.db.sql_list('''select holiday_date from `tabHoliday`
		where
			parent=%(holiday_list)s
			and holiday_date >= %(start_date)s
			and holiday_date <= %(end_date)s''', {
				"holiday_list": holiday_list,
				"start_date": msd,
				"end_date": med
			})

	holidays = [cstr(i) for i in holidays]

	trabalhouferiado = 0

	for h in holidays:
		print h
		hh = frappe.db.sql(""" select attendance_date,status,company,employee from `tabAttendance` where docstatus = 1 and status = 'Present' and attendance_date = %s and employee = %s and company = %s """,(h,doc.employee, doc.company), as_dict = True)
		print hh
		if hh:
			print "TRABALHOU !!!!"
			trabalhouferiado += 1

	doc.total_working_days = doc.total_working_days + trabalhouferiado
	doc.numero_de_faltas = flt(j[0]['count(status)']) + (flt(j3[0]['count(status)'])/2) + flt(j4[0]['count(status)'])
	doc.payment_days = (doc.payment_days + trabalhouferiado) - j[0]['count(status)'] - j1[0]['count(status)'] - j4[0]['count(status)']
	diaspagamento = doc.payment_days
	totaldiastrabalho = doc.total_working_days
	horasextra = j2[0]['horas']
	print 'ATTENDANCE ABSENT e ON LEAVE'
	print 'ATTENDANCE ABSENT e ON LEAVE'
	print 'ATTENDANCE ABSENT e ON LEAVE'
	print j[0]['count(status)'], j3[0]['count(status)'], j1[0]['count(status)']
	print j[0]['count(status)'], j3[0]['count(status)'], j1[0]['count(status)']
	print (flt(j[0]['count(status)']) + flt(j3[0]['count(status)']))
	print 'Horas Extra ', j2[0]['horas']

	print 'diastrab+feriado ', totaldiastrabalho + trabalhouferiado

#	print doc.name , " + ", doc.employee
#	print doc.payment_days - j[0]['count(status)']
	

#	for desconto in frappe.db.sql(""" SELECT * from `tabSalary Detail` where parent = %s """,doc.name, as_dict=True):
#		dd = frappe.get_doc("Salary Detail",desconto.name)
#	print "valor ", dd.amount
#	print "default ", dd.default_amount
#		dd.amount = desconto.default_amount
#		dd.save()

#	if not (len(doc.get("earnings")) or len(doc.get("deductions"))):
		# get details from salary structure
#		print "BUSCA SALARY STRUCTURE"
#		doc.get_emp_and_leave_details()
#	else:
#		print "BUSCA SALARY STRUCTURE com LEAVE"
#		doc.get_leave_details(lwp = doc.leave_without_pay)


	print "MEU TESTE"
	print "MEU TESTE"
	print "MEU TESTE"
	print "MEU TESTE"
	print "MEU TESTE"
	print "MEU TESTE"
	print "VALOR POR EXTENSO"

	company_currency = erpnext.get_company_currency(doc.company)
	print company_currency
	if (company_currency =='KZ'):
		doc.total_in_words = num2words(doc.rounded_total, lang='pt_BR').title() + ' Kwanzas.'
	else:
		doc.total_in_words = money_in_words(doc.rounded_total, company_currency)

	print "MEU TESTE"
	print "MEU TESTE"
	print "MEU TESTE"
	print "VALIDAR SUBSIDIO DE FERIAS"

	valida_sub_ferias(doc,diaspagamento,totaldiastrabalho)

	return

	m = get_month_details(mes_startdate.year, mes_startdate.month)
	msd = m.month_start_date
	med = m.month_end_date
	emp = frappe.get_doc("Employee", doc.employee)
	
	tdim, twd = get_total_days(doc,method, emp, msd, med, m)
	
	get_loan_deduction(doc,method, msd, med)
	get_expense_claim(doc,method)
	holidays = get_holidays(doc, method, msd, med, emp)
	
	lwp, plw = get_leaves(doc, method, msd, med, emp)
	
	doc.leave_without_pay = lwp
		
	doc.posting_date = m.month_end_date
	wd = twd - holidays #total working days
	doc.total_days_in_month = tdim
	att = frappe.db.sql("""SELECT sum(overtime), count(name) FROM `tabAttendance` 
		WHERE employee = '%s' AND attendance_date >= '%s' AND attendance_date <= '%s' 
		AND status = 'Present' AND docstatus=1""" \
		%(doc.employee, msd, med),as_list=1)

	half_day = frappe.db.sql("""SELECT count(name) FROM `tabAttendance` 
		WHERE employee = '%s' AND attendance_date >= '%s' AND attendance_date <= '%s' 
		AND status = 'Half Day' AND docstatus=1""" \
		%(doc.employee, msd, med),as_list=1)
	
	t_hd = flt(half_day[0][0])
	t_ot = flt(att[0][0])
	doc.total_overtime = t_ot
	tpres = flt(att[0][1])

	ual = twd - tpres - lwp - holidays - plw - (t_hd/2)
	
	if ual < 0:
		frappe.throw(("Unauthorized Leave cannot be Negative for Employee {0}").\
			format(doc.employee_name))
	
	paydays = tpres + (t_hd/2) + plw + math.ceil((tpres+(t_hd/2))/wd * holidays)
	pd_ded = flt(doc.payment_days_for_deductions)
	doc.payment_days = paydays
	
#	if doc.change_deductions == 0:
#		doc.payment_days_for_deductions = doc.payment_days
	
#	doc.unauthorized_leaves = ual 
	
	ot_ded = round(8*ual,1)
	if ot_ded > t_ot:
		ot_ded = (int(t_ot/8))*8
	doc.overtime_deducted = ot_ded
	d_ual = int(ot_ded/8)
	
	#Calculate Earnings
	chk_ot = 0 #Check if there is an Overtime Rate
	for d in doc.earnings:
		if d.salary_component == "Overtime Rate":
			chk_ot = 1
			
	for d in doc.earnings:
		earn = frappe.get_doc("Salary Component", d.salary_component)
		if earn.depends_on_lwp == 1:
			d.depends_on_lwp = 1
		else:
			d.depends_on_lwp = 0
		
		if earn.based_on_earning:
			for d2 in doc.earnings:
				#Calculate Overtime Value
				if earn.earning == d2.salary_component:
					d.default_amount = flt(d2.amount) * t_ot
					d.amount = flt(d2.amount) * (t_ot - ot_ded)
		else:
			if d.depends_on_lwp == 1 and earn.books == 0:
				if chk_ot == 1:
					d.amount = round(flt(d.default_amount) * (paydays+d_ual)/tdim,0)
				else:
					d.amount = round(flt(d.default_amount) * (paydays)/tdim,0)
			elif d.depends_on_lwp == 1 and earn.books == 1:
				d.amount = round(flt(d.default_amount) * flt(doc.payment_days_for_deductions)/ tdim,0)
			else:
				d.amount = d.default_amount
		
		if earn.only_for_deductions <> 1:
			gross_pay += flt(d.amount)

	if gross_pay < 0:
		doc.arrear_amount = -1 * gross_pay
	gross_pay += flt(doc.arrear_amount) + flt(doc.leave_encashment_amount)
	
	#Calculate Deductions
	for d in doc.deductions:
		#Check if deduction is in any earning's formula
		chk = 0
		for e in doc.earnings:
			earn = frappe.get_doc("Salary Component", e.salary_component)
			for form in earn.deduction_contribution_formula:
				if d.salary_component == form.salary_component:
					chk = 1
					d.amount = 0
		if chk == 1:
			for e in doc.earnings:
				earn = frappe.get_doc("Salary Component", e.salary_component)
				for form in earn.deduction_contribution_formula:
					if d.salary_component == form.salary_component:
						d.default_amount = flt(e.default_amount) * flt(form.percentage)/100
						d.amount += flt(e.amount) * flt(form.percentage)/100
			d.amount = round(d.amount,0)
			d.default_amount = round(d.default_amount,0)
		elif d.salary_component <> 'Loan Deduction':
			str = frappe.get_doc("Salary Structure", doc.salary_structure)
			for x in str.deductions:
				if x.salary_component == d.salary_component:
					d.default_amount = x.amount
					d.amount = d.default_amount

		tot_ded +=d.amount
	
	#Calculate Contributions
	for c in doc.contributions:
		#Check if contribution is in any earning's formula
		chk = 0
		for e in doc.earnings:
			earn = frappe.get_doc("Salary Component", e.salary_component)
			for form in earn.deduction_contribution_formula:
				if c.salary_component == form.salary_component:
					chk = 1
		if chk == 1:
			c.amount = round((flt(c.default_amount) * flt(doc.payment_days_for_deductions)/tdim),0)
		tot_cont += c.amount
	
	doc.gross_pay = gross_pay
	doc.total_deduction = tot_ded
	doc.net_pay = doc.gross_pay - doc.total_deduction
	doc.rounded_total = myround(doc.net_pay, 10)
		
	company_currency = erpnext.get_company_currency(doc.company)
	doc.total_in_words = money_in_words(doc.rounded_total, company_currency)
	doc.total_ctc = doc.gross_pay + tot_cont




def get_total_days(doc,method, emp, msd, med, month):
	tdim = month["month_days"] #total days in a month
	if emp.relieving_date is None:
		relieving_date = datetime.date(2099, 12, 31)
	else:
		relieving_date = emp.relieving_date

	if emp.date_of_joining >= msd:
		twd = (med - emp.date_of_joining).days + 1 #Joining DATE IS THE First WORKING DAY
	elif relieving_date <= med:
		twd = (emp.relieving_date - msd).days + 1 #RELIEVING DATE IS THE LAST WORKING DAY
	else:
		twd = month["month_days"] #total days in a month
	return tdim, twd
	
def get_leaves(doc, method, start_date, end_date, emp):
	#Find out the number of leaves applied by the employee only working days
	lwp = 0 #Leaves without pay
	plw = 0 #paid leaves
	diff = (end_date - start_date).days + 1
	for day in range(0, diff):
		date = start_date + datetime.timedelta(days=day)
		auth_leaves = frappe.db.sql("""SELECT la.name FROM `tabLeave Application` la
			WHERE la.status = 'Approved' AND la.docstatus = 1 AND la.employee = '%s'
			AND la.from_date <= '%s' AND la.to_date >= '%s'""" % (doc.employee, date, date), as_list=1)
		if auth_leaves:
			auth_leaves = auth_leaves[0][0]
			lap = frappe.get_doc("Leave Application", auth_leaves)
			ltype = frappe.get_doc("Leave Type", lap.leave_type)
			hol = get_holidays(doc,method, date, date, emp)
			if hol:
				pass
			else:
				if ltype.is_lwp == 1:
					lwp += 1
				else:
					plw += 1
	lwp = flt(lwp)
	plw = flt(plw)
	return lwp,plw
		
def get_holidays(doc,method, start_date, end_date,emp):
	if emp.relieving_date is None:
		relieving_date = datetime.date(2099, 12, 31)
	else:
		relieving_date = emp.relieving_date
	
	if emp.date_of_joining > start_date:
		start_date = emp.date_of_joining
	
	if relieving_date < end_date:
		end_date = relieving_date
	
	holiday_list = get_holiday_list_for_employee(doc.employee)
	holidays = frappe.db.sql("""SELECT count(name) FROM `tabHoliday` WHERE parent = '%s' AND 
		holiday_date >= '%s' AND holiday_date <= '%s'""" %(holiday_list, \
			start_date, end_date), as_list=1)
	
	holidays = flt(holidays[0][0]) #no of holidays in a month from the holiday list
	return holidays
	
def get_loan_deduction(doc,method, msd, med):
	existing_loan = []
	for d in doc.deductions:
		existing_loan.append(d.employee_loan)
		
	#get total loan due for employee
	query = """SELECT el.name, eld.name, eld.emi, el.deduction_type, eld.loan_amount
		FROM 
			`tabEmployee Loan` el, `tabEmployee Loan Detail` eld
		WHERE
			eld.parent = el.name AND
			el.docstatus = 1 AND el.posting_date <= '%s' AND
			eld.employee = '%s'""" %(med, doc.employee)
		
	loan_list = frappe.db.sql(query, as_list=1)

	for i in loan_list:
		emi = i[2]
		total_loan = i[4]
		if i[0] not in existing_loan:
			#Check if the loan has already been deducted
			query = """SELECT SUM(ssd.amount) 
				FROM `tabSalary Detail` ssd, `tabSalary Slip` ss
				WHERE ss.docstatus = 1 AND
					ssd.parent = ss.name AND
					ssd.employee_loan = '%s' and ss.employee = '%s'""" %(i[0], doc.employee)
			deducted_amount = frappe.db.sql(query, as_list=1)

			if total_loan > deducted_amount[0][0]:
				#Add deduction for each loan separately
				#Check if EMI is less than balance
				balance = flt(total_loan) - flt(deducted_amount[0][0])
				if balance > emi:
					doc.append("deductions", {
						"idx": len(doc.deductions)+1, "depends_on_lwp": 0, "default_amount": emi, \
						"employee_loan": i[0], "salary_component": i[3], "amount": emi
					})
				else:
					doc.append("deductions", {
						"idx": len(doc.deductions)+1, "d_depends_on_lwp": 0, "default_amount": balance, \
						"employee_loan": i[0], "salary_component": i[3], "amount": balance
					})
	for d in doc.deductions:
		if d.employee_loan:
			total_given = frappe.db.sql("""SELECT eld.loan_amount 
				FROM `tabEmployee Loan` el, `tabEmployee Loan Detail` eld
				WHERE eld.parent = el.name AND eld.employee = '%s' 
				AND el.name = '%s'"""%(doc.employee, d.employee_loan), as_list=1)
			
			deducted = frappe.db.sql("""SELECT SUM(ssd.amount) 
				FROM `tabSalary Detail` ssd, `tabSalary Slip` ss
				WHERE ss.docstatus = 1 AND ssd.parent = ss.name 
				AND ssd.employee_loan = '%s' and ss.employee = '%s'"""%(d.employee_loan, doc.employee), as_list=1)
			balance = flt(total_given[0][0]) - flt(deducted[0][0])
			if balance < d.amount:
				frappe.throw(("Max deduction allowed {0} for Loan Deduction {1} \
				check row # {2} in Deduction Table").format(balance, d.employee_loan, d.idx))

def get_expense_claim(doc,method):
	m = get_month_details(doc.fiscal_year, doc.month)
	#Get total Expense Claims Due for an Employee
	query = """SELECT ec.name, ec.employee, ec.total_sanctioned_amount, ec.total_amount_reimbursed
		FROM `tabExpense Claim` ec
		WHERE ec.docstatus = 1 AND ec.approval_status = 'Approved' AND
			ec.total_amount_reimbursed < ec.total_sanctioned_amount AND
			ec.posting_date <= '%s' AND ec.employee = '%s'""" %(m.month_end_date, doc.employee)
	
	
	ec_list = frappe.db.sql(query, as_list=1)
	for i in ec_list:
		existing_ec = []
		for e in doc.earnings:
			existing_ec.append(e.expense_claim)
		
		if i[0] not in existing_ec:
			#Add earning claim for each EC separately:
			doc.append("earnings", {
				"idx": len(doc.earnings)+1, "depends_on_lwp": 0, "default_amount": (i[2]-i[3]), \
				"expense_claim": i[0], "salary_component": "Expense Claim", "amount": (i[2]- i[3])
			})

def get_edc(doc,method):
	#Earning Table should be replaced if there is any change in the Earning Composition
	#Change can be of 3 types in the earning table
	#1. If a user removes a type of earning
	#2. If a user adds a type of earning
	#3. If a user deletes and adds a type of another earning
	#Function to get the Earnings, Deductions and Contributions (E,D,C)

	m = get_month_details(doc.fiscal_year, doc.month)
	emp = frappe.get_doc("Employee", doc.employee)
	joining_date = emp.date_of_joining
	if emp.relieving_date:
		relieving_date = emp.relieving_date
	else:
		relieving_date = '2099-12-31'
	
	struct = frappe.db.sql("""SELECT name FROM `tabSalary Structure Employee` WHERE employee = %s AND
		is_active = 'Yes' AND (from_date <= %s OR from_date <= %s) AND
		(to_date IS NULL OR to_date >= %s OR to_date >= %s)""", 
		(doc.employee, m.month_start_date, joining_date, m.month_end_date, relieving_date))
	if struct:
		sstr = frappe.get_doc("Salary Structure", struct[0][0])
		print struct[0][0]
	else:
		frappe.throw("No active Salary Structure for this period")
		
	contri_amount = 0

	existing_ded = []
	
	dict = {}	
	for d in doc.deductions:
		dict['salary_component'] = d.salary_component
		dict['idx'] = d.idx
		dict['default_amount'] = d.default_amount
		existing_ded.append(dict.copy())
	
	doc.contributions = []
	doc.earnings = []
	
	earn = 0
	#Update Earning Table if the Earning table is empty
	if doc.earnings:
		pass
	else:
		earn = 1
	
	chk = 0
	for e in  sstr.earnings:
		for ern in doc.earnings:
			if e.salary_component == ern.salary_component and e.idx == ern.idx:
				chk = 1
		if chk == 0:
			doc.earnings = []
			get_from_str(doc, method)
			
	
	if earn == 1:
		doc.earnings = []
		for e in sstr.earnings:
			doc.append("earnings",{
				"salary_component": e.salary_component,
				"default_amount": e.amount,
				"amount": e.amount,
				"idx": e.idx
			})
			
	ded = 0
	if doc.deductions:
		pass
	else:
		ded = 1

	for d in doc.deductions:
		found = 0
		for dss in sstr.deductions:
			if d.salary_component == dss.salary_component and d.idx == dss.idx and found == 0:
				found = 1
		if found == 0 and ded == 0:
			if d.salary_component <> "Loan Deduction":
				ded = 1
				
	if ded == 1:
		doc.deductions = []
		for d in sstr.deductions:
			doc.append("deductions",{
				"salary_component": d.salary_component,
				"default_amount": d.amount,
				"amount": d.amount,
				"d.idx": d.idx
			})
	
	for c in sstr.contributions:
		contri = frappe.get_doc("Salary Component", c.salary_component)
		for e in doc.earnings:
			earn = frappe.get_doc("Salary Component", e.salary_component)
			for cont in earn.deduction_contribution_formula:
				if c.salary_component == cont.salary_component:
					contri_amount += round(cont.percentage * e.amount/100,0)
			
		doc.append("contributions",{
			"salary_component": c.salary_component,
			"default_amount": c.amount,
			"amount": contri_amount
			})

def get_from_str(doc,method):
	pass	
def myround(x, base=5):
    return int(base * round(float(x)/base))



def unlink_ref_doc_from_salary_slip(ref_no):
	linked_ss = frappe.db.sql_list("""select name from `tabSalary Slip`
	where journal_entry=%s and docstatus < 2""", (ref_no))
	if linked_ss:
		for ss in linked_ss:
			ss_doc = frappe.get_doc("Salary Slip", ss)
			frappe.db.set_value("Salary Slip", ss_doc.name, "status", "Submitted")
			frappe.db.set_value("Salary Slip", ss_doc.name, "journal_entry", "")


def valida_sub_ferias(doc,dias_pagamento,total_dias_trabalho):

	emp = frappe.get_doc("Employee", doc.employee)
	for d in doc.earnings:
		#print d.salary_component 
		print frappe.db.get_value("Salary Component", d.salary_component, "salary_component_abbr")
		print 'Formula ', d.formula
		qry_cmpnt = frappe.db.sql(""" select sd.formula from `tabSalary Structure Employee` as se 
		join `tabSalary Detail` as sd on sd.parent = se.parent where se.employee = %s and sd.abbr = %s """,(emp.name,d.abbr),as_dict=True)
		qry_result=''
		
		if (qry_cmpnt):
			if qry_cmpnt[0].formula !='': 
				print '1 ',qry_cmpnt[0].formula
				qry_result = qry_cmpnt[0].formula

		if frappe.db.get_value("Salary Component", d.salary_component, "salary_component_abbr") == "SB":
			#Salary Base
			salariobase = d.amount
		if (d.salary_component == "Subsidio de Ferias") or (d.abbr == "SF"):
			
			print emp.date_of_joining
			print datetime.date(datetime.datetime.today().year,12,31) - emp.date_of_joining 		
			print (datetime.date(datetime.datetime.today().year,12,31) - emp.date_of_joining).days
 			print "anos ", divmod((datetime.date(datetime.datetime.today().year,12,31) - emp.date_of_joining).days,365)
			anos,meses =divmod((datetime.date(datetime.datetime.today().year,12,31) - emp.date_of_joining).days,365)
			print anos
			print meses
			if anos >0:
				print "Tem mais que 1 ano"
				pass
			elif meses / 30 < 12:
				print "Menos que 12 meses!!!!"
				print "rever a formula !!!", d.amount
				print date_diff(frappe.utils.nowdate(),emp.date_of_joining)

				salariohora = ((salariobase*12)/(52*40)) # em vez de 40horas devem ser 44horas
				print "Salario Hora ", salariohora

				meses1 = date_diff(frappe.utils.nowdate(),emp.date_of_joining)/30
				print "Meses ", meses1

				diasTrab = meses1 * 2
				print "dias Trab ", diasTrab

				salariodia = salariohora * 8
				print "salario Dia ", salariodia

				subferias = (salariodia*diasTrab)*0.50
				print "salario Ferias ", subferias

				d.amount = subferias
		
		print 'SALARY SLIpppppppppppppppppppp'
		print qry_result

		if qry_result != None: 
			print 'payment_days' in qry_result
			if (qry_result.find('payment_days') !=-1 and dias_pagamento != total_dias_trabalho ):
				#found
				print total_dias_trabalho
				print dias_pagamento
				print 'strip ',qry_result.strip()
				ff = qry_result.replace('payment_days',str(dias_pagamento))
				print qry_result.replace('payment_days',str(dias_pagamento))
				qry_result =ff
				if (qry_result.find('total_working_days') !=-1):	
					ff = qry_result.replace('total_working_days',str(total_dias_trabalho))
					qry_result =ff
				print frappe.safe_eval(qry_result,None,None)

				d.amount = frappe.safe_eval(qry_result,None,None) #eval(qry_result)

			if (qry_result.find('total_working_days') !=-1  and dias_pagamento != total_dias_trabalho):	
				ff = qry_result.replace('total_working_days',str(total_dias_trabalho))
				qry_result =ff
				d.amount = frappe.safe_eval(qry_result,None,None)

		
				#print frappe.safe_eval(ff,None,None)

		qry_result=''
			#if (datetime.date(datetime.datetime.today().year,12,31) - emp.date_of_joining) < 12:
			#	print "A Menos de um Ano na Empresa"

@frappe.whitelist()
def proc_salario_iliquido(mes,ano,empresa):

	print "Processa o Salario Iliquido ..."
	print "Processa o Salario Iliquido ..."
	print "Processa o Salario Iliquido ..."
	print "Processa o Salario Iliquido ..."
	print "Processa o Salario Iliquido ..."
	salario_iliquido =0;
	print mes, ano, empresa.encode('utf-8')
	#Processa o Salario Iliquido ...
	#for salslip in frappe.db.sql(""" select name from `tabSalary Slip` where 
	for salslip in frappe.db.sql(""" SELECT name,status from `tabSalary Slip` where month(start_date) = %s and year(start_date) = %s and  company = %s """,(mes,ano,empresa), as_dict=True):
		#SI = (SB + HE - PA + PP) - (FTJSS - FI )
		print salslip
		salario_iliquido =0;
		tab_detalhes = frappe.db.sql(""" select parent,abbr,amount from `tabSalary Detail` where abbr in ('SB','HE','PA','PP','FTJSS','FI','IH','SDF','DU','ST','ABF','SA','PAT','SN') and parent= %s""",(salslip.name),as_dict=True)

#(SB + HE + PA + PP + IH + SDF + DU + ST) - (FTJSS - FTI1)

		#print tab_detalhes

		for r in tab_detalhes:
			if (r.abbr == 'SB') or (r.abbr == 'HE') or  (r.abbr == 'PA') or (r.abbr == 'PP') or (r.abbr == 'IH') or (r.abbr == 'SDF') or (r.abbr == 'DU') or (r.abbr == 'ST') or (r.abbr == 'PAT') or (r.abbr == 'SN'):
				salario_iliquido = salario_iliquido + flt(r.amount)
#			elif (r.abbr == 'SA') or (r.abbr == 'ABF'):
#				salario_iliquido = salario_iliquido - flt(r.amount)

			elif (r.abbr == 'FTJSS') or (r.abbr == 'FI'):
				salario_iliquido = salario_iliquido - flt(r.amount)

			print "iliquido"
			print salario_iliquido
		ss_doc1 = frappe.get_doc("Salary Slip", salslip)
		print ss_doc1

		frappe.db.set_value("Salary Slip", ss_doc1.name, "salario_iliquido", salario_iliquido)

