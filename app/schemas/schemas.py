

def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        'user_name': user["user_name"],
        'password': user['password'],
        'full_name': user['full_name'],
        'phone': user['phone']
    }

def users_entity(users) -> list:
    return [user_entity(user) for user in users]


def identify_card(card) -> dict:
    return {
        'id' : str(card['_id']),
        'user_name': card['user_name'],
        'so_cccd': card['so_cccd'],
        'ho_ten': card['ho_ten'],
        'ngay_sinh': card['ngay_sinh'],
        'gioi_tinh': card['gioi_tinh'],
        'quoc_tich': card['quoc_tich'],
        'que_quan': card['que_quan'],
        'thuong_tru': card['thuong_tru'],
        'ngay_cap': card['ngay_cap'],
        'noi_cap': card['noi_cap']
    }


