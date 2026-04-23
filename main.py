from fastapi import FastAPI, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db, Base
from app import models, schemas, crud

# Ma'lumotlar bazasida jadvallarni yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Blog API",
    description="FastAPI bilan yaratilgan mini blog REST API",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
async def root():
    """Asosiy endpoint - API haqida ma'lumot"""
    return {
        "message": "Mini Blog API ga xush kelibsiz!",
        "docs": "/docs",
        "endpoints": {
            "barcha_postlar": "GET /posts",
            "bitta_post": "GET /posts/{post_id}",
            "post_yaratish": "POST /posts",
            "post_yangilash": "PUT /posts/{post_id}",
            "post_ochirish": "DELETE /posts/{post_id}",
            "qidiruv": "GET /posts/search?q=...",
        },
    }


# ==================== POSTLAR ====================

@app.get("/posts", response_model=List[schemas.Post], tags=["Posts"])
async def get_all_posts(
    skip: int = Query(0, ge=0, description="Nechta postni o'tkazib yuborish"),
    limit: int = Query(100, ge=1, le=100, description="Qancha post qaytarish"),
    db: Session = Depends(get_db),
):
    """Barcha postlarni olish (pagination bilan)"""
    return crud.get_posts(db, skip=skip, limit=limit)


@app.get("/posts/search", response_model=List[schemas.Post], tags=["Posts"])
async def search_posts(
    q: str = Query(..., min_length=1, description="Qidiruv so'zi"),
    db: Session = Depends(get_db),
):
    """Postlarni sarlavha yoki matn bo'yicha qidirish"""
    return crud.search_posts(db, q)


@app.get("/posts/{post_id}", response_model=schemas.Post, tags=["Posts"])
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Bitta postni ID bo'yicha olish"""
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    return post


@app.post(
    "/posts",
    response_model=schemas.Post,
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"],
)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Yangi post yaratish"""
    return crud.create_post(db, post)


@app.put("/posts/{post_id}", response_model=schemas.Post, tags=["Posts"])
async def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
):
    """Postni yangilash"""
    updated = crud.update_post(db, post_id, post)
    if not updated:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    return updated


@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Posts"],
)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Postni o'chirish"""
    deleted = crud.delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post topilmadi")
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
