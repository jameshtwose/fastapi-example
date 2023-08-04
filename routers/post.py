from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db
import datetime


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    """Get all posts.
    
    <pre>
    Parameters
    ----------
    db : Session
        The database session.
    current_user : int
        The current user.
    Returns
    -------
    list
        A list of posts.
    Raises
    ------
    HTTPException
        If the user is not authorized to perform the requested action.
    </pre>
    
    """
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Create a post and commit it to the database.
    
    <pre>
    Parameters
    ----------
    post : schemas.PostCreate
        The post to create.
    db : Session
        The database session.
    current_user : int
        The current user.
    Returns
    -------
    dict
        A dictionary containing the created post.
    Raises
    ------
    HTTPException
        If the user is not authorized to perform the requested action.
    </pre>
    
    """
    new_post = models.Post(created_at=datetime.datetime.now(), owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Get a post from the database by id.
    
    <pre>
    Parameters
    ----------
    id : int
        The id of the post to retrieve.
    db : Session
        The database session.
    current_user : int
        The current user.
    Returns
    -------
    dict
        A dictionary containing the post.
    Raises
    ------
    HTTPException
        If the post does not exist or the user is not authorized to perform the requested action.
    </pre>    
    
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.owner_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Delete a post from the database by id.
    
    <pre>
    Parameters
    ----------
    id : int
        The id of the post to delete.
    db : Session
        The database session.
    current_user : int
        The current user.
    Returns
    -------
    Response
        A response object with status code 204.
    Raises
    ------
    HTTPException
        If the post does not exist or the user is not authorized to perform the requested action.
    </pre>
    
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.owner_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Update a post in the database by id.
    
    <pre>
    Parameters
    ----------
    id : int
        The id of the post to update.
    updated_post : schemas.PostCreate
        The updated post.
    db : Session
        The database session.
    current_user : int
        The current user.
    Returns
    -------
    dict
        A dictionary containing the updated post.
    Raises
    ------
    HTTPException
        If the post does not exist or the user is not authorized to perform the requested action.
    </pre>
    
    """
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.owner_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return post_query.first()
