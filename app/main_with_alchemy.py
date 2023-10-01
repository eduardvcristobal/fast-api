from fastapi import FastAPI, Depends

from database import SessionLocal, get_db, engine
import models

app = FastAPI()

@app.get("/get-all-posts")
def root(db: SessionLocal = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts}

@app.get("/get-post-by-id/{id}")
def get_post_by_id(id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"data" : post}

@app.post("/create-post")
def create_post(db: SessionLocal = Depends(get_db)):
    post = models.Post(title="test title", content="test content")
    db.add(post)
    db.commit()
    return {"data" : "post created"}

@app.put("/update-post/{id}")
def update_post(id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    post.title = "updated title"
    db.commit()
    return {"data" : "post updated"}

@app.delete("/delete-post/{id}")
def delete_post(id: int, db: SessionLocal = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(post)
    db.commit()
    return {"data" : "post deleted"}