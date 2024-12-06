
from pymongo import MongoClient


uri = "mongodb+srv://hao123:hao123@mongodb.txxq6.mongodb.net/?retryWrites=true&w=majority&appName=Mongodb"
# Create a new client and connect to the server
cluster = MongoClient(uri)

db = cluster['face_ekyc']
collection = db['users']


def register():
    username = input("Vui lòng nhập tên đăng nhập: ")
    password = input("Vui lòng nhập mật khẩu: ")
    query = {
        "user_name": username,
        "password" : password
    }
    try:
        result = collection.insert_one(query)
        if result is not None:
            print('Register Successfully')
        else:
            print('Register Fail !')
    except Exception as e:
        raise Exception('Error: ' ,e)

def login():
    login_action = True
    try:
        while login_action:
            username = input('Tài khoản: ')
            password = input('Mật khẩu:')

            query = {
                'user_name': username,
                'password': password
            }
            user = collection.find_one(query)
            
            if user is None:
                print('Login Fail, Incorrect Usernam or Password !')
                login_action = True
            else:
                print(user)
                print('Login SuccesFully !')
                login_action = False
        
    except Exception as e:
        raise Exception('Error: ', e)

if __name__  == "__main__":
    
    while True:
        chosse = input('Vui lòng nhập lựa chọn: ')
        print("1. Đăng kí")
        print("2. Đăng nhập")
        if chosse == "1":
            register()
        elif chosse == "2":
            login()
        else:
            break