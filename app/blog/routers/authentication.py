from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from blog.token import create_access_token
from blog import models
from blog.database import get_db
from blog.hashing import Hash
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.
                                        username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid Credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect Password')

    access_token = create_access_token(data={"sub": user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
