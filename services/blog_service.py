import models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.blog_schema import BlogCreate, BlogBase
from database import engine
from models import  Blog

session = Session(bind=engine)

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(form: BlogCreate, db:Session ):
    db_publisher_id=session.query(Blog).filter(Blog.publisher_id==form.publisher_id).first()
    if db_publisher_id is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with publisher id not found")
    
    new_blog = models.Blog(title = form.title, 
                           content = form.content,
                           publisher_id = form.publisher_id
                           )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return {"Blog Id" : new_blog.id,
            "Title" : form.title,
            "Content" : form.content,
            "Publisher Id" : form.publisher_id}


def update_blog(id: int, form: BlogBase, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Blog with id {id} not found")
    blog.update({"title" : form.title, "content" : form.content})
    db.commit()

    return "Updated successfully"



def delete_blog(id: int, db: Session):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted successfully"
