import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread as gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds_g.json', scopes=SCOPES)

TABLE_NAME = 'Меню'

CATEGORY_ARN = 'arn:aws:execute-api:eu-central-1:991466274654:ws7r41qs05/*/GET/EL_MENU/categories'
DISHES_ARN = 'arn:aws:execute-api:eu-central-1:991466274654:ws7r41qs05/*/GET/EL_MENU/dishes'


def get_dishes_list(category: str, gs):
    sheet = gs.open(TABLE_NAME).worksheet(category)
    dishes_list = sheet.get_all_records()
    return dishes_list


def get_sheet_list(gs):
    worksheet_list = gs.open(TABLE_NAME).worksheets()
    sheet_title_list = [sheet.title for sheet in worksheet_list]
    return sheet_title_list


def lambda_handler(event, context):
    gs = gspread.authorize(credentials)
    query_string = event.get('queryStringParameters')
    category = query_string.get('category') if query_string else None
    if category:
        output = get_dishes_list(category, gs)
        status_code = 200
    else:
        output = get_sheet_list(gs)
        status_code = 200
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(output, ensure_ascii=True)
    }
