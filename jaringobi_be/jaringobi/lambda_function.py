import json, psycopg2
from .logger import *
set_file_logger()


def connect_to_postgres():
    # rds_host = "your-rds-endpoint.amazonaws.com"
    # username = "your-db-username"
    # password = "your-db-password"
    # db_name = "your-db-name"

    rds_host = "de-6-1-test.ch4xfyi6stod.ap-northeast-2.rds.amazonaws.com"
    username = "jaryngobi"
    password = "pirates-recipe"
    db_name = "service"

    try:
        conn = psycopg2.connect(host=rds_host, user=username, password=password, dbname=db_name)
        return conn
    except psycopg2.Error as e:
        print("ERROR: Could not connect to PostgreSQL instance.")
        print(e)
        raise

# 웹에서 검색한 메뉴명 전처리 함수
# ex) "소 불고기" => "소불고기"
def preprocess_menu_name(menu_name: str) -> str:
    logging.info("menu name: {}".format(menu_name))
    return menu_name.replace(" ", "")

# "menu" 테이블에서 메뉴의 이름의 id를 반환하는 함수
def get_menu_id(cursor, menu_name: str) -> int:
    menu_id = None

    # 메뉴 이름에 대한 쿼리 코드 작성
    sql_query = """
        SELECT id
        FROM menu
        WHERE name = %s
    """

    cursor.execute(sql_query, (menu_name,))
    result = cursor.fetchone()

    if result:
        menu_id = result[0]

    return menu_id

# "recipe" 테이블에서 해당 메뉴 아이디를 갖는 레시피 리스트를 반환하는 함수
def get_recipe_id_list(cursor, menu_id: str) -> list:
    recipe_id_list = []

    """
    메뉴 id에 대한 쿼리 코드 작성
    """
    sql_query = """
        SELECT id
        FROM recipe
        WHERE menu_id = %s
    """
    cursor.execute(sql_query, (menu_id,))
    recipe_ids = cursor.fetchall()

    for recipe_id in recipe_ids:
        recipe_id_list.append(recipe_id[0])

    # 만약 레시피 목록이 없다면 빈 리스트 반환할 예정
    return recipe_id_list

# "ingredient" 테이블에서 해당 레시피 아이디를 갖는 재료 정보를 반환하는 함수
def get_ingredient_info_list(cursor, recipe_id: str) -> list:
    ingredient_info_list = []

    """
    재료 정보 쿼리 코드 작성
    예상 결과 : [[ingredient_name1, ingredient_volume1, ingredient_unit1], ...]
    """
    sql_query = """
        SELECT name, volume, unit
        FROM ingredient
        WHERE recipe_id = %s
    """
    cursor.execute(sql_query, (recipe_id,))
    ingredient_infos = cursor.fetchall()
    
    for ingredient in ingredient_infos:
        ingredient_info_list.append(list(ingredient))

    return ingredient_info_list

# "product" 테이블에서 해당 재료명에 대해서 최저가 상품 정보를 반환하는 함수.
def get_cheapest_product_info(cursor, ingredient_name: str) -> tuple:
    product_price = None
    product_gram_price = None
    product_url = None
    product_img = None

    # 해당 재료명에 대한 쿼리. gram_price가 가장 싼 것 위주로 검색. 만약 없다면 그냥 price를 기준으로.
    sql_query = """
    SELECT price, gram_price, url, image
    FROM (
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_1
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_2
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_3
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_4
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_5
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_6
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_7
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_8
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_9
        UNION ALL
        SELECT price, gram_price, url, ingredient_name, image
        FROM product_10
    ) AS combined_products
    WHERE ingredient_name = %s
    ORDER BY COALESCE(gram_price, price) ASC 
    LIMIT 1
    """
    cursor.execute(sql_query, (ingredient_name,))
    product_info = cursor.fetchone()

    if product_info:
        # 결과에서 필요한 정보 추출
        product_price = product_info[0]  # 가격
        product_gram_price = product_info[1]  # 단위당 가격
        product_url = product_info[2] # 상품 링크 정보
        product_img = product_info[3] # 상품 이미지

    return (product_price, product_gram_price, product_url, product_img)

# 총 가격을 계산하는 함수.
def get_total_price(ingredient_infos: list) -> float:
    total_price = 0.0
    ingredient_list_without_unit = []
    for i in range(len(ingredient_infos)):
        ingredient_name = ingredient_infos[i][0] # 재료명
        product_unit_price = ingredient_infos[i][1] # 단위당 가격
        # product_price = ingredient_infos[i][2] # 가격
        ingredient_volume = ingredient_infos[i][3] # 첨가량
        # ingredient_unit = ingredient_infos[i][4] # 첨가 단위
        # product_url = ingredient_infos[i][5] # 상품 링크
        # product_img = ingredient_infos[i][6] # 상품 이미지

        if product_unit_price and ingredient_volume: # 만약 단위당 가격이 존재한다면
            total_price += ingredient_volume * product_unit_price # ex) 10(g) * 1g당355원 -> 3550
        else:
            ingredient_list_without_unit.append(ingredient_name)

    return total_price, ingredient_list_without_unit

# "youtube_video", "channel" 테이블에서 해당 레시피 아이디에 대해서 정보를 반환하는 함수.
def get_youtube_info(cursor, recipe_id: str) -> tuple:
    youtube_url = ''
    youtube_thumbnail = ''
    youtube_title = ''
    youtube_uploaded_date = ''
    channel_name = ''
    channel_img = ''

    # recipe_id에 대해서 recipe 테이블에서 쿼리하여 youtube_video_id를 찾기.
    cursor.execute("SELECT youtube_video_id FROM recipe WHERE id = %s", (recipe_id,))
    youtube_video_id = cursor.fetchone()[0]
    # youtube_video_id에 대해서 youtube_video 테이블에 쿼리.
    cursor.execute("SELECT url, thumbnail_src, title, uploaded_date, channel_id FROM youtube_video WHERE id = %s", (youtube_video_id,))
    video_info = cursor.fetchone()

    if video_info:
        youtube_url = video_info[0]
        youtube_thumbnail = video_info[1]
        youtube_title = video_info[2]
        youtube_uploaded_date = video_info[3]

        # channel_id를 받아서 channel 테이블에서 조회
        channel_id = video_info[4]
        cursor.execute("SELECT name, img_src FROM channel WHERE id = %s", (channel_id,))
        channel_info = cursor.fetchone()

        if channel_info:
            channel_name = channel_info[0]
            channel_img = channel_info[1]

    return (youtube_url, youtube_thumbnail, youtube_title, youtube_uploaded_date, channel_name, channel_img)

def lambda_handler(menu_name):
    conn = connect_to_postgres()
    cursor = conn.cursor()

    menu_name = preprocess_menu_name(menu_name)
    menu_id = get_menu_id(cursor=cursor, menu_name=menu_name)
    if menu_id is None:
        conn.close()
        return {
            'statusCode': 404,
            'body': json.dumps('메뉴명이 존재하지 않습니다.')
        }

    recipe_id_list = get_recipe_id_list(cursor=cursor, menu_id=menu_id) # 레시피 목록 검색
    if len(recipe_id_list) == 0:
        conn.close()
        return {
            'statusCode': 404,
            'body': json.dumps('메뉴명에 대한 레시피가 존재하지 않습니다.')
        }

    recipe_infos = {
        'recipe_id_list' : [],
        'ingredient_info_list' : [],
        'recipe_total_price_list' : [],
        'ingredient_list_without_unit' : []
    }

    # 각 레시피에 대한 가격 정보 조회
    for recipe_id in recipe_id_list:
        recipe_infos['recipe_id_list'].append(recipe_id)
        ingredient_info_list = get_ingredient_info_list(cursor=cursor, recipe_id=recipe_id)
        ingredient_infos = []
        # 각 재료에 대한 정보 조회
        for ingredient_info in ingredient_info_list:
            ingredient_name = ingredient_info[0]
            ingredient_volume = ingredient_info[1]
            ingredient_unit = ingredient_info[2]
            product_price, product_unit_price, product_url, product_img = get_cheapest_product_info(cursor=cursor, ingredient_name=ingredient_name)
            ingredient_infos.append([ingredient_name, product_unit_price, product_price, ingredient_volume, ingredient_unit, product_url, product_img])

        recipe_total_price, ingredients_without_unit = get_total_price(ingredient_infos=ingredient_infos) # 레시피 총 가격 계산
        recipe_infos['ingredient_info_list'].append(ingredient_infos)
        recipe_infos['recipe_total_price_list'].append(recipe_total_price)
        recipe_infos['ingredient_list_without_unit'].append(ingredients_without_unit)

    # recipe_total_price_list에서 최저가의 인덱스를 찾은 후 해당 레시피 아이디로 유튜브 데이터 조회. 조건: 가격이 존재 and 레시피 재료가 3개 이상.
    valid_indices = [i for i, price in enumerate(recipe_infos['recipe_total_price_list']) if price != 0 and len(recipe_infos['ingredient_info_list'][i]) >= 3]
    min_price_index = min(valid_indices, key=lambda x: recipe_infos['recipe_total_price_list'][x])
    min_recipe_id = recipe_infos['recipe_id_list'][min_price_index]
    
    youtube_url, youtube_thumbnail, youtube_title, youtube_uploaded_date, channel_name, channel_img = get_youtube_info(cursor=cursor, recipe_id=min_recipe_id)
    
    # 최저가 레시피의 데이터 추출.
    total_price = recipe_infos['recipe_total_price_list'][min_price_index]
    ingredient_list_without_unit = recipe_infos['ingredient_list_without_unit'][min_price_index]
    ingredient_list = []
    ingredient_info_list = recipe_infos['ingredient_info_list'][min_price_index]
    for i in range(len(ingredient_info_list)):
        ingredient_name = ingredient_info_list[i][0]
        ingredient_unit_price = ingredient_info_list[i][1]
        ingredient_price = ingredient_info_list[i][2]
        ingredient_volume = ingredient_info_list[i][3]
        ingredient_unit = ingredient_info_list[i][4]
        ingredient_url = ingredient_info_list[i][5]
        ingredient_img = ingredient_info_list[i][6]

        ingredient = {
            "ingredient_name": ingredient_name,
            "ingredient_unit_price": ingredient_unit_price,
            "ingredient_price": ingredient_price,
            "ingredient_volume": ingredient_volume,
            "ingredient_unit": ingredient_unit,
            "ingredient_url": ingredient_url,
            "ingredient_img": ingredient_img
        }
        ingredient_list.append(ingredient)

    result = {
        "youtube_url": youtube_url,
        "youtube_thumbnail": youtube_thumbnail,
        "youtube_title": youtube_title,
        "youtube_uploaded_date": youtube_uploaded_date,
        "channel_name": channel_name,
        "channel_img": channel_img,
        "total_price": total_price,
        "ingredient_list": ingredient_list,
        "ingredient_list_without_unit": ingredient_list_without_unit
    }

    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
