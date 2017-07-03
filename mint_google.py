import gspread, datetime
from oauth2client.service_account import 
from secrets import KEYFILE_NAME

CUM_EXP_CELL = 'D2'
BUD_LEFT_CELL = 'E2'

def _validateAndOpen(wks_name):
	scope = ['https://spreadsheets.google.com/feeds']

	credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE_NAME, scope)
	gc = gspread.authorize(credentials)
	finance_wks = gc.open(wks_name)

	return finance_wks
#
# Takes in a float, EXP_TODAY_VAL of the total amount of money spent today.
# Returns {'cum_exp':cum_exp, 'budget_left':budget_left, 'expected_cum':expected_cum}
def getMoneyData(exp_today_val, wks_name):
	finance_wks = _validateAndOpen(wks_name)

	now = datetime.datetime.now()

	# open current month sheet
	curr_month = now.strftime("%B")
	month_wks = finance_wks.worksheet(curr_month)

	# get row for current day expenses
	curr_date = now.strftime("%m/%d/%y")
	date_cell = month_wks.find(curr_date)
	
	# get expected cumulative expenses for today
	expected_cum_row, expected_cum_col = date_cell.row, date_cell.col + 2
	expected_cum = month_wks.cell(expected_cum_row, expected_cum_col).value
	# append expenses for today
	exp_today_row, exp_today_col = date_cell.row, date_cell.col + 1
	month_wks.update_cell(exp_today_row, exp_today_col, exp_today_val)
	# get cumulative expenses and budget left
	cum_exp = month_wks.acell(CUM_EXP_CELL).value
	budget_left = month_wks.acell(BUD_LEFT_CELL).value

	return {'cum_exp':cum_exp, 'budget_left':budget_left, 'expected_cum':expected_cum}

	# TODO: add functionality for "how to stay on budget"
