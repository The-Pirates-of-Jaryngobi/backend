import json
import psycopg2

# PostgreSQL 연결을 위한 함수
def connect_to_postgres():
    # RDS 연결 정보
    rds_host = "your-rds-endpoint.amazonaws.com"
    username = "your-db-username"
    password = "your-db-password"
    db_name = "your-db-name"

    try:
        conn = psycopg2.connect(host=rds_host, user=username, password=password, dbname=db_name)
        return conn
    except psycopg2.Error as e:
        print("ERROR: Could not connect to PostgreSQL instance.")
        print(e)
        raise

# 메뉴명 전처리 함수
def preprocess_menu_name(menu_name: str) -> str:
	preprocessed_menu_name = ''
	# 메뉴명 전처리 코드 작성.
	# ex) "소 불고기" => "소불고기"
		
	return preprocessed_menu_name

# "menu" 테이블에서 메뉴 이름의 id를 반환하는 함수.
def get_menu_id(cursor, menu_name: str) -> int:
	menu_id = None
	"""
	메뉴 이름에 대한 쿼리 코드 작성.
	"""
	return menu_id # 만약 메뉴 이름이 없다면 None으로 반환할 예정.

# "recipe" 테이블에서 해당 메뉴 아이디를 갖는 레시피 리스트를 반환하는 함수.
def get_recipe_id_list(cursor, menu_id: int) -> list:
	recipe_id_list = []
	"""
	메뉴 id에 대한 쿼리 코드 작성.
	"""
	return recipe_id_list # 만약 레시피 목록이 없다면 빈 리스트 반환할 예정.

# "ingredient" 테이블에서 해당 레시피 아이디를 갖는 재료 정보를 반환하는 함수.
def get_ingredient_info_list(cursor, recipe_id: int) -> list:
	ingredient_info_list = []
	"""
	재료 정보 쿼리 코드 작성.
	예상 결과 : [[ingredient_name1, ingredient_volume1, ingredient_unit1], ...]
	"""
	return ingredient_info_list

# "product" 테이블에서 해당 재료명에 대해서 정보를 반환하는 함수.
def get_product_info(cursor, ingredient_name: str) -> tuple:
	product_price = None
	product_unit_price = None
	product_url = None
	"""
	재료명에 대한 쿼리 -> 가격, 단위당 가격, 상품 링크 정보 추출.
	"""
	return (product_price, product_unit_price, product_url)

# 총 가격을 계산하는 함수.
def calculate_total_price(ingredient_info_list: list, product_info_list: list) -> float:
	total_price = 0.0
	"""
	로직 작성.
	"""
	return total_price

# "youtube_video" 테이블에서 해당 레시피 아이디에 대해서 정보를 반환하는 함수.
def get_youtube_info(cursor, recipe_id: int) -> tuple:
    youtube_url = ''
    youtube_thumbnail = ''
    youtube_title = ''
    channel_name = ''
    channel_img = ''
    """
    recipe_id에 대해서 youtube_video table에 쿼리.
    -> channel_id를 받아서 channel 테이블에 쿼리.
    """
    return (youtube_url, youtube_thumbnail, youtube_title, channel_name, channel_img)

def lambda_handler(event, context):
    # HTTP GET 요청인지 확인
    if event['httpMethod'] != 'GET':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    conn = connect_to_postgres()
    cursor = conn.cursor()
    
    # event로부터 메뉴명 추출
    body = json.loads(event['body'])
    menu_name = body.get('menu_name')
		
	# 메뉴명 전처리 및 검색
    menu_name = preprocess_menu_name(menu_name)
    menu_id = get_menu_id(cursor=cursor, menu_name=menu_name)
    if menu_id is None:
        return {
            'statusCode': 404,
            'body': json.dumps('메뉴명이 존재하지 않습니다.')
        }
		
    recipe_id_list = get_recipe_id_list(cursor=cursor, menu_id=menu_id) # 레시피 목록 검색
    if len(recipe_id_list) == 0:
        return {
            'statusCode': 404,
            'body': json.dumps('메뉴명에 대한 레시피가 존재하지 않습니다.')
        }
    
    recipe_infos = {
			'recipe_id_list' : [],
			'ingredient_info_list' : [],
			'product_info_list' : [],
			'recipe_total_price_list' : []
	}
    # 각 레시피에 대한 가격 정보 조회
    for recipe_id in recipe_id_list:
        recipe_infos['recipe_id_list'].append(recipe_id)
        ingredient_info_list = get_ingredient_info_list(cursor=cursor, recipe_id=recipe_id)
        recipe_infos['ingredient_info_list'].append(ingredient_info_list)
        # 각 재료에 대한 정보 조회
        for ingredient_info in ingredient_info_list:
            ingredient_name = ingredient_info[0]
            ingredient_volume = ingredient_info[1]
            ingredient_unit = ingredient_info[2]
            """
            위와 같은 방식으로 코드 작성 예정...
            """
    
    conn.close()