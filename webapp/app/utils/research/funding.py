from collections import defaultdict

from app.research.models import FundingAgency
from app import db

def parse_funding_data(worksheet, agencies):
    row = 4  # a starting row
    print(worksheet.title)
    while True:
        fund_cell = 'D%d' % row
        agency_cell = 'A%d' % row
        val = worksheet.acell(fund_cell).value
        if val == 'END':
            return
        elif val.strip() == '':
            agency = worksheet.acell(agency_cell).value
            row += 1
            continue
        else:
            agencies[agency][worksheet.title] = float(val)
            row += 1


# @backoffice.route('/gdrive/loadsheet/research_funds/')
def update():
    '''
    Update research fundings from Google Sheet.
    '''
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    gc = gspread.authorize(credentials)
    workbook = gc.open("research_funds.xls")
    agencies = defaultdict(dict)

    for worksheet in workbook.worksheets():
        parse_funding_data(worksheet, agencies)

    for a in agencies:
        print(a)
