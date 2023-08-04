from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, utils, oauth2
from database import get_db


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Login endpoint.
    
    <pre>
    Parameters
    ----------
    user_credentials : OAuth2PasswordRequestForm
        The user credentials.
    db : Session
        The database session.
    Returns
    -------
    dict
        A dictionary containing the access token and token type.
    </pre>
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # create a token
    return {"access_token": access_token, "token_type": "bearer"}
