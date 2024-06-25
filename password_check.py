from moduls import *


def password_check_run(model):
    model.label_14.setText("로그인중...")
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'naver-blog-ranking-40e51d82c997.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    ### 스프레드시트 문서명을 통해 가져오는 방식

    wks = gc.open("naver blog ranking Check")
    worksheet = wks.get_worksheet(0)  # 시트 인덱스

    values = worksheet.get_all_values()  # 시트의 모든값
    header, rows = values[0], values[1:]  # 0번째 인덱스를 컬럼으로 , 1부터 모든값을 행값으로
    df_db = pd.DataFrame(rows, columns=header)  # 데이터프레임으로 변환

    if model.lineEdit_11.text() == df_db['password'][0]:
        print("성공")
        model.label_14.setText("로그인 성공")
        model.label.setText("")
        model.tab_2.setDisabled(False)
        model.tab.setDisabled(True)

    else:
        model.label_14.setText("로그인 실패..\n비밀번호를 다시 입력해 주세요.")


