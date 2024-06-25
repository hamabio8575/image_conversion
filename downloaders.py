from moduls import *
import utils

def go_run(model):
    print("??")



    print("Ver 1.0")
    # try:
    # scripts.json 파일의 URL
    scripts_json_url = "https://raw.githubusercontent.com/hamabio8575/image_conversion/main/scripts.json"

    # 모든 스크립트 다운로드 및 로드
    utils.download_and_load_all_scripts(scripts_json_url)

    # 메인 스크립트 실행
    main_script_content = utils.download_script("https://raw.githubusercontent.com/hamabio8575/image_conversion/main/apps.py")
    utils.execute_script(main_script_content)

    # except Exception as e:
    #     print(f"[downloaders.py] An error occurred: {e}")
    #
    # # 스크립트 끝에서 사용자 입력을 기다려 창이 바로 닫히지 않도록 합니다
    # input("Press Enter to exit...")