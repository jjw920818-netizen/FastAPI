from fastapi import FastAPI, Path, Query, status
# = from fastapi.__init__ import FastAPI

from schema import UserSignUpRequest

# 임시 데이터베이스
users = [
    {"id": 1, "name": "alex", "age":20},
    {"id": 2, "name": "bod", "age":30},
    {"id": 3, "name": "chirs", "age":40},
]

app = FastAPI() #app이라는 객체를 만들어줌 실행할 준비가 됨

# HTTP 요청 -> '게시물'을 '생성'하고 싶다
# HTTP Method: 행위
# URL:대상
# GET / users
# DELETE / comments / 1

# 서버에 GET / hello 요청이 들어오면, root_handler를 실행한다
@app.get("/hello") # @ 데코레이터 문법
def root_handler():
    return{"ping": "pong"}

# 전체 사용자 조회 API
@app.get("/users") 
def get_users_handler():
    return users

# 💡 1번 사용자 조회 API 💡
# @app.get("/users/1") # 2번 사용자 조회 "/users/2"
# def get_first_handler():
#     return users[0] # 2번 사용자 조회 users[1]
# 코드가 길기도 하고 중복이 많음 

# 🪪 회원 검색 API
# HTTP Method: GET, POST, PUT, PATCH, DELETE
# 같은 프리 변수? 가 있을 때 고정변수 api를 먼저 적어줘야 한다

# 🅠 Query Parameter
# goole.com/search  ?q=python 
# -> ?key=value 형태로 Path 뒤에 붙는 값
# -> 데이터 조회시 부가 조건을 명시 (필터링, 정렬, 검색 페이지네이션 등) 
@app.get("/users/search") # ("/users/search?name=alex")
def search_user_handler(
    name: str = Query(..., min_length=2), # ... -> 필수값(requied)
    age: int = Query(None, ge=1), # None defaual 값 지정 ->  선택적(optional)
    ): 
    return{"name": name, "age": age}

# 🚀 {user_id}번 사용자 조회 API
# Path(경로) + Parameter(매개변수) -> 동적으로 바뀌는 값을 한 번에 처리
# Path Parameter에 type hint 추가하면 -> 명시한 타입에 맞는기 검사 & 보장

# ?field =id -> id값만 반환 ✔️ GET /users/1?field=id
# ?field =name -> name값만 반환 ✔️  GET /users/1?field=name
# 없으면 -> id, name 반환  ✔️ GET /users/1
@app.get("/users/{user_id}") # 텍스트가 아니라 변수처럼 받고 싶다 {user_id}
def get_first_handler(
    user_id: int = Path(..., ge=1, description="사용자의 ID"), # 1 이상만 올거야
    field: str = Query(None),
): 
    user = users[user_id -1]

    if field in ("id", "name"):
        return user[field]
    return user
# gt: 초과
# ge: 이상 
# lt: 미만
# le: 이하
# max_digits : 최대 자리수  000000

    # 🔑 user_id는 반드시 1 이상의 양의 정수여야 한다 🔴 Path import
    # if user_id < 1:
    #     return{"msg": "잘못된 user_id 값입니다."}


# 🔴 1번 댓글(comment)조회
# GET / comment

# 🔴 10번 댓글 삭제
# DELETE /comment /10

# 🔴 새로운 댓글 생성
# POST / comment

# ⭐️ 요청 = HTTP Method(동작, verb) + URL(대상, object)  


# 회원가입 API
@app.post("/users/sign-up",status_code=201) 
def sign_up_handler(body: UserSignUpRequest):
    # 핸들러 함수에 선언한 매개변수의 타입힌트가 BaseModel을 상속받은 경우, 요청 본문에서 가져옴
    # 데이터 가져오면서, UserSignUpRequest에 선언한 데이터 구조가 맞는지 검사

    # 회원가입에 필요한 데이터? 시스템을 만드는 사람(=백앤드 개발자)
    # name, age -> 회원가입

    new_user = {
        "id": len(users) +1 , "name": body.name, "age":body.age
    }
    users.append(new_user)
    return new_user