from flask import Flask, jsonify
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds_g.json', scopes=SCOPES)

TABLE_NAME = 'Меню'

app = Flask(__name__)


@app.route('/dishes/<category>', methods=['GET'])
def get_dishes_list(category: str):
    gs = gspread.authorize(credentials)
    sheet = gs.open(TABLE_NAME).worksheet(category)
    dishes_list = sheet.get_all_records()
    return jsonify({
        'statusCode': 200,
        'body': dishes_list,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
    })


@app.route('/categories', methods=['GET'])
def get_categories():
    gs = gspread.authorize(credentials)
    worksheet_list = gs.open(TABLE_NAME).worksheets()
    sheet_title_list = [sheet.title for sheet in worksheet_list]
    return jsonify({
        'statusCode': 200,
        'body': sheet_title_list,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
    })


if __name__ == '__main__':
    app.run(debug=True)
