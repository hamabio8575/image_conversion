from moduls import *
import utils
import downloaders

# try:
print("■ 이미지 수정을 시작합니다..")
print("test11")

downloaders.new_model.textBrowser.append("■ 이미지 수정을 시작합니다..")
df = pd.read_excel("이미지 수정 세팅.xlsx")
change_color_range_start = float(df['채도'][0].split("~")[0])
change_color_range_end = float(df['채도'][0].split("~")[1])
brightness_factor_range_start = float(df['명도'][0].split("~")[0])
brightness_factor_range_end = float(df['명도'][0].split("~")[1])

path_df = pd.read_excel("이미지경로.xlsx")
path_df = path_df.replace(np.nan, '')
for image_number, orginal_path, save_path, keyword, quality in path_df.to_numpy().tolist():  # 엑셀 받아오기
    print(f'원본폴더경로 : ' + orginal_path.split("\\")[-1])
    ### 이미지,채도,명도
    resize_factor = random.uniform(0.80, 0.99)
    random_change_color = random.uniform(change_color_range_start, change_color_range_end)
    random_brightness_factor = random.uniform(brightness_factor_range_start, brightness_factor_range_end)
    enhance_random_list = [resize_factor, random_change_color, random_brightness_factor]

    ### 테두리
    # 테두리종류 랜덤 선택
    border = random.choice(['round', 'border'])
    # 테두리 - 라운드
    radius = random.uniform(70, 120)

    # 테두리 - 보더
    folder_image_list = os.listdir('border_images')
    border_image_path = f"border_images\\{random.choice(folder_image_list)}"
    border_thickness = random.randint(int(df['테두리'][0].split("~")[0]), int(df['테두리'][0].split("~")[1]))  # Adjust the thickness of the border

    ### 로고
    logo_position = (50, 50)
    sample_region = (50, 50, 150, 150)
    logo_resize_factor = random.uniform(0.30, 0.40)

    ### 폰트파일
    font_list = os.listdir('font_files')
    font_file = random.choice(font_list)
    file_cnt = 0
    for image_file_name in os.listdir(orginal_path):  # 선택폴더내에 있는 파일들
        if 'txt' not in image_file_name:  # txt 파일 제외한 이미지들만
            file_cnt += 1
            print(image_file_name)
            image_path = os.path.join(orginal_path, image_file_name)
            image = Image.open(image_path).convert('RGBA')  # 선택한 이미지 객체 생성
            width, height = image.size  # 선택한 이미지 크기 확인

            ### 테두리
            if border == 'round':
                resized_image = utils.add_round_corners(image, radius)
            else:
                resized_image = utils.insert_border(image, border_image_path, border_thickness)

            ### 이미지 크기, 채도, 명도
            resized_image, new_width, new_height = utils.enhance_image(resized_image, width, height, enhance_random_list)

            ### 1. 로고
            resized_image = utils.insert_logo(logo_position, sample_region, resized_image, logo_resize_factor, new_width)

            ### 2. 사진번호 삽입(텍스트) 및 3. 하단 텍스트 삽입
            description_text = utils.get_description(image_file_name, orginal_path)
            final_image = utils.add_text(resized_image, image_number, image_file_name, font_file, new_width, new_height,
                                   orginal_path, df)

            update_dir_path = utils.make_update_dir(save_path, keyword)
            utils.save_quality(final_image, update_dir_path, file_cnt, quality, format='JPEG')

    downloaders.new_model.textBrowser.append("■ " + orginal_path.split("\\")[-1] + " 완료")
print('★ 모든 이미지 변환 완료')
downloaders.new_model.textBrowser.append('★ 모든 이미지 변환 완료')
input()
# except Exception as e:
#     print(f"□ [apps.py] An error occurred: {e}")
#     input('□ 에러 메세지를 확인하세요...')