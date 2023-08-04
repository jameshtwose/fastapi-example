from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
import datetime


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a user and commit it to the database.
    
    <pre>
    Parameters
    ----------
    user : schemas.UserCreate
        The user to create.
    db : Session
        The database session.
    Returns
    -------
    dict
        A dictionary containing the created user.
    Raises
    ------
    HTTPException
        If the user is not authorized to perform the requested action.
    </pre>
    
    """
    # hash the users password
    user.password = utils.get_password_hash(user.password)
    
    # add the created_at field
    user.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    """Get a user from the database by id.
    
    <pre>
    Parameters
    ----------
    id : int
        The id of the user to retrieve.
    db : Session
        The database session.
    Returns
    -------
    dict
        A dictionary containing the user.
    Raises
    ------
    HTTPException
        If the user is not authorized to perform the requested action
        or if the user does not exist.
    </pre>
    
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user