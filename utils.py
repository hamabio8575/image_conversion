from moduls import *


# 수정이미지 폴더 생성
def make_update_dir(save_path, keyword):
    update_dir_path = os.path.join(save_path, keyword)
    if not os.path.exists(update_dir_path):
        print("■ 자동업로드 또는 하위 폴더가 없어 새로 생성합니다.")
        os.makedirs(update_dir_path)
    return update_dir_path


# 테두리 라운드 처리
def add_round_corners(image, radius):
    # 라운드 코너 마스크 생성
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius=radius, fill=255)

    # 이미지에 알파 채널 추가
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.putalpha(mask)

    # 원본 이미지와 라운드 마스크 결합
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image


def insert_border(image, border_image_path, border_thickness):
    # 테두리 이미지 객체
    border_image = Image.open(border_image_path).convert("RGBA")
    # 테두리 이미지 랜덤값으로 변환
    border_image = border_image.resize((border_thickness, border_thickness))
    # 테두리 이미지 90도 회전
    height_border_image = border_image.rotate(90)

    # 원본 이미지와 동일한 크기에 랜덤값으로 변환된 테두리를 더한 새 이미지를 만듭니다.
    new_width = image.width + 2 * border_image.width
    new_height = image.height + 2 * border_image.height
    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

    # 원본 이미지를 새 이미지 중앙에 붙여넣습니다.
    new_image.paste(image, (border_image.width, border_image.height))

    # 상,하 테두리 삽입
    # 랜덤값으로 변환된 테두리 이미지를 삽입
    for x in range(0, new_width, border_image.width):
        # 상
        new_image.paste(border_image, (x, 0), border_image)
        # 하
        new_image.paste(border_image, (x, new_height - border_image.height), border_image)

    # 좌,우 테두리 삽입
    # 랜덤값으로 변환된 테두리 이미지를 삽입
    for y in range(0, new_height, border_image.height):
        # 좌
        new_image.paste(height_border_image, (0, y), height_border_image)
        # 우
        new_image.paste(height_border_image, (new_width - border_image.width, y), height_border_image)

    return new_image


# 이미지 크기, 채도, 명도
def enhance_image(image, width, height, enhance_random_list):
    # 이미지 크기
    resize_factor = enhance_random_list[0]
    new_width = int(width * resize_factor)
    new_height = int(height * resize_factor)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # 채도변경
    random_change_color = enhance_random_list[1]
    enhancer = ImageEnhance.Color(resized_image)
    resized_image = enhancer.enhance(random_change_color)

    # 명도변경
    random_brightness_factor = enhance_random_list[2]
    enhancer = ImageEnhance.Brightness(resized_image)
    resized_image = enhancer.enhance(random_brightness_factor)

    return resized_image, new_width, new_height


# 로고 삽입
def insert_logo(logo_position, sample_region, resized_image, logo_resize_factor, new_width):
    # 밝기 계산
    region = resized_image.crop(sample_region)
    stat = ImageStat.Stat(region)
    brightness = stat.mean[0]

    # 밝기에 따라 로고 선택
    if brightness < 80:  # 어두운 배경
        logo_image_path = "logo_files/logo_white.png"
    else:  # 밝은 배경
        logo_image_path = f"logo_files/{random.choice(['logo_black.png', 'logo_basic.png'])}"

    insert_image = Image.open(logo_image_path)

    # 로고 크기를 원본 이미지의 특정비율로 조정
    new_logo_width = int(new_width * logo_resize_factor)
    aspect_ratio = insert_image.width / insert_image.height
    new_logo_height = int(new_logo_width / aspect_ratio)
    insert_image = insert_image.resize((new_logo_width, new_logo_height), Image.LANCZOS)
    insert_width, insert_height = insert_image.size
    resized_image.paste(insert_image, logo_position, mask=insert_image)
    return resized_image


# 주석 읽기
def get_description(image_file_name, orginal_path):
    description_file_name = image_file_name.split(".")[0] + ".txt"
    description_path = os.path.join(orginal_path, description_file_name)

    with open(description_path, "r", encoding='UTF-8') as f:
        description_text = f.read().strip()

    return description_text


# 사진번호 및 하단 텍스트 삽입
def add_text(resized_image, image_number, image_file_name, font_file, new_width, new_height, orginal_path, df):
    # 드로잉 객체 생성
    draw_resized = ImageDraw.Draw(resized_image)

    # 사진번호 삽입
    font_size_percent = 0.05
    font_size = int(new_width * font_size_percent)
    font = ImageFont.truetype(f"font_files/{font_file}", font_size, encoding="UTF-8")

    # 텍스트 바운딩 박스 계산
    text_bbox = draw_resized.textbbox((0, 0), image_number, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    while text_width > 0.2 * new_width:
        font_size -= 1
        font = ImageFont.truetype(f"font_files/{font_file}", font_size, encoding="UTF-8")
        text_bbox = draw_resized.textbbox((0, 0), image_number, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

    x_position_right = new_width - text_width - 50
    y_position = 50

    region = resized_image.crop((0, 0, new_width, 150))
    stat = ImageStat.Stat(region)
    brightness = stat.mean[0]

    if brightness < 150:
        text_color = "white"
    else:
        text_color = "black"

    draw_resized.text((x_position_right, y_position), image_number, font=font, fill=text_color)

    # 하단 주석 삽입
    description_text = get_description(image_file_name, orginal_path)  # 주석

    font_size_percent = 0.2  # 폰트 크기 비율 설정
    font_size = int(new_width * font_size_percent)
    font = ImageFont.truetype(f"font_files/{font_file}", font_size, encoding="UTF-8")

    description_bbox = draw_resized.textbbox((0, 0), description_text, font=font)
    description_width = description_bbox[2] - description_bbox[0]
    description_height = description_bbox[3] - description_bbox[1]

    while description_width > 0.9 * new_width:  # 주석 텍스트의 너비가 이미지 너비의 80%를 넘지 않도록
        font_size -= 1
        font = ImageFont.truetype(f"font_files/{font_file}", font_size, encoding="UTF-8")
        description_bbox = draw_resized.textbbox((0, 0), description_text, font=font)
        description_width = description_bbox[2] - description_bbox[0]
        description_height = description_bbox[3] - description_bbox[1]

    margin = 20
    padding = 10
    final_image_height = new_height + description_height + margin + padding * 2

    final_image = Image.new("RGBA", (new_width, final_image_height), "white")
    final_image.paste(resized_image, (0, 0))

    new_draw = ImageDraw.Draw(final_image)
    x_position_description = (new_width - description_width) // 2
    y_position_description = new_height + margin + padding

    region = final_image.crop((0, new_height - 150, new_width, new_height))
    stat = ImageStat.Stat(region)
    brightness = stat.mean[0]

    if brightness < 100:
        text_color_description = "white"
    else:
        text_color_description = "black"

    text_color_description = random.choice(df['주석 컬러'][0].split(","))
    new_draw.text((x_position_description, y_position_description), description_text, font=font,
                  fill=text_color_description)

    return final_image


# 이미지 품질 낮춰서 저장
def save_quality(final_image, update_dir_path, file_cnt, quality, format='JPEG'):
    if quality == "":  # quality가 문자열이면 100으로 판단하고 quality 옵션 없이 저장
        print("str")
        print("quality 옵션 없이 저장")
        final_image.save(f'{update_dir_path}\\이미지 ({file_cnt}).{format.lower()}')

    else:
        quality = int(float(quality))
        print("not str")
        if quality > 95:
            quality = 95
            print(quality)
            print(f"quality 옵션 {quality}")

        elif quality < 96:
            quality = int(quality)
            print(quality)
            print(f"quality 옵션 {quality}")

        if format.upper() == 'JPEG':
            if final_image.mode == 'RGBA':
                final_image = final_image.convert('RGB')
            final_image.save(f'{update_dir_path}\\이미지 ({file_cnt}).jpeg', quality=quality)
        elif format.upper() == 'PNG':
            compress_level = 9 - int(quality / 10)  # quality 값을 압축 수준으로 변환
            final_image.save(f'{update_dir_path}\\이미지 ({file_cnt}).png', compress_level=compress_level)
        else:
            final_image.save(f'{update_dir_path}\\이미지 ({file_cnt}).{format.lower()}')
