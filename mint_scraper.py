import mintapi, datetime, re
from secrets import mint_username, mint_password, mint_ius_session, mint_thx_guid, pn_to, pn_from
from secrets import depositor, sheet_title
import mint_google, mint_twilio

IUS_SESSION, THX_GUID = mint_ius_session, mint_thx_guid
USERNAME, PASSWORD = mint_username, mint_password

def getMint(ius_session, thx_guid, username, password):
	return mintapi.Mint(username, password, ius_session, thx_guid)

#
# Get total transactions (including pending) for given date.
# Date must be of form "mm/dd/yy"
# Returns {'expenses':expenses}, or {'expenses':expenses, 'income':income} if include_income == True
def getDayTransactions(mint, date, include_income=False, depositor=depositor):
	date_transactions = mint.get_transactions_json(start_date = date)
	ret = {'expenses':0, 'all_exp': []}
	if include_income: ret['income'] = 0
	for transaction in date_transactions:
		datetime_date = datetime.datetime.strptime(transaction['date'] + date[-2:], "%b %d%y")
		compare_date = datetime_date.strftime("%m/%d/%y")
		# Check if there were no transactions today
		if compare_date != date:                continue

		merchant = transaction['merchant']
		if re.search('Postmates Temp Auth', merchant):	continue
		amount = float(transaction['amount'].strip(u'$').replace(",", ""))
		is_transfer = transaction['isTransfer']
		if not is_transfer:
			# Check if a paycheck has come in, add to income
			is_deposit = re.search(depositor, merchant)
			if is_deposit and include_income:
				ret['income'] += amount
			elif not is_deposit:
				# print merchant, amount
				ret['expenses'] += amount
				ret['all_exp'] += [merchant + ':' + str(amount)]
		# counts as transfers but are still expenses
		elif merchant == 'Inst Xfer' or merchant == 'Venmo':
			# print merchant, amount
			ret['expenses'] += amount
			ret['all_exp'] += [merchant + ':' + str(amount)]
	return ret

def constructText(curr_day_exp, date, all_exp):
	money_data = mint_google.getMoneyData(curr_day_exp, sheet_title, date)
	cum_exp, budget_left, expected_cum = money_data['cum_exp'], money_data['budget_left'], \
										 money_data['expected_cum']
	ret_string = "{}: You spent ${} today.\n".format(date, curr_day_exp)
	ret_string += "Cumulative expenses: ${}; Expected cumulative expenses: ${}. \n".format(cum_exp, expected_cum)
	if float(budget_left) <= 0.0:
		ret_string += "STOP SPENDING. Budget left: ${}.".format(budget_left)
	elif float(budget_left) <= 100.0:
		ret_string += "You gotta slow down. Budget left: ${}.".format(budget_left)
	else:
		ret_string += "Budget left: ${}.".format(budget_left)
	ret_string += str(all_exp)
	return ret_string


def init():
	try:
		mint = getMint(IUS_SESSION, THX_GUID, USERNAME, PASSWORD)
	except Exception as e:
		print "ERROR:", e
		return False
	# Get current date in proper format: mm/dd/yy
	date = _formatDate()
	# date = "07/08/17"

	curr_day_transactions = getDayTransactions(mint, date)
	curr_day_exp = curr_day_transactions['expenses']
	all_exp = curr_day_transactions['all_exp']
	print curr_day_exp

	text_msg = constructText(curr_day_exp, date, all_exp)
	print text_msg

	ret = mint_twilio.sendText(pn_to, pn_from, text_msg)
	if not ret:
		mint_twilio.sendText(pn_to, pn_from, "Your script broke. Fix it!")
		return False
	return True

def init_test():
	try:
		mint = getMint(IUS_SESSION, THX_GUID, USERNAME, PASSWORD)
	except Exception as e:
		print "ERROR:", e
		return False
	# Get current date in proper format: mm/dd/yy
	date = _formatDate()
	# date = "07/07/17"

	curr_day_transactions = getDayTransactions(mint, date)
	curr_day_exp = curr_day_transactions['expenses']
	all_exp = curr_day_transactions['all_exp']
	print curr_day_exp

	text_msg = constructText(curr_day_exp, date, all_exp)
	print text_msg



def _formatDate():
	now = datetime.datetime.now()
	date = now.strftime("%m/%d/%y")
	return date

# init()
init_test()