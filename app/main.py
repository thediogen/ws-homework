import contextlib

from fastapi import FastAPI, WebSocket, Request, status, HTTPException, Depends, Path
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app.utils.auth import AuthForm
from app.models import User
from app.database import Session_DP, session_manager
from app.config import DB_URL, SESSION_MIDDLEWARE_SECRET_KEY
from app.connections import chat_manager, Chat
# from app.frontend.chat import html1, html2


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init(DB_URL)
    # del request.session['access_token']

    yield 
    await session_manager.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SESSION_MIDDLEWARE_SECRET_KEY)


# AUTHORIZE ===============================


def check_user(request: Request):
    access_token = request.session.get('access_token')

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='unauthorized. try to authorize or authenticate'
        )

    return access_token


@app.post('/authenticate')
async def authenticate(session: Session_DP, request: Request, form_data: AuthForm = Depends()):
    user = await User.get(session=session, email=form_data.email)
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with such email already exists'
        )

    new_user = await User.create(session=session, form_data=form_data)

    request.session['access_token'] = new_user.session_token

    return new_user.name, new_user.email, new_user.session_token


@app.post('/authorize')
async def authorize(session: Session_DP, request: Request, form_data: AuthForm = Depends()):
    user = await User.get(session=session, email=form_data.email)
    user = user[0]

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with such email does not exist'
        )
    
    if form_data.password != user.password or form_data.username != user.name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password or username'
        )

    request.session['access_token'] = user.session_token
    
    return {
        'access_token': user.session_token,
        'token_type': 'bearer'
    }


@app.websocket('/chat_ws/{chat_id}')
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            receive_text = await websocket.receive_text()
            print(receive_text)

            for connection in chat_manager.chats.values():
                print(connection)
                await connection.send_text(receive_text)
                
    except Exception as _:
        print('Something went wrong')


@app.get('/')
async def index(user: str = Depends(check_user)):
    with open('app/frontend/index.html', 'r') as file:
        html = file.read()

    return HTMLResponse(html)


@app.get('/chat/{chat_id}')
async def chat(chat_id: int = Path(...), user: str = Depends(check_user)):
    print(chat_id)
    with open('app/frontend/chat.html', 'r') as file:
        html = file.read()

    return HTMLResponse(html)


@app.post('/create_new_chat')
async def create_new_chat(user: str = Depends(check_user)):
    chat = chat_manager.create()
    # print('HERE')

    return {'chat_id': chat.chat_id}


@app.get('/check_user')
async def check_user(session: Session_DP, request: Request):
    user = await User.get_by_token(session=session, token=request.session.get('access_token'))

    return user

@app.get('/log_out')
async def log_out(request: Request):
    del request.session['access_token']

    return 200