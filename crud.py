from sqlalchemy.orm import Session
from sqlalchemy import desc

from app import models, schemas


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """Barcha postlarni olish (eng yangilari birinchi)"""
    return (
        db.query(models.Post)
        .order_by(desc(models.Post.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post(db: Session, post_id: int):
    """Bitta postni ID bo'yicha olish"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def search_posts(db: Session, query: str):
    """Postlarni sarlavha yoki matn bo'yicha qidirish"""
    search = f"%{query}%"
    return (
        db.query(models.Post)
        .filter(
            (models.Post.title.ilike(search)) | (models.Post.content.ilike(search))
        )
        .order_by(desc(models.Post.created_at))
        .all()
    )


def create_post(db: Session, post: schemas.PostCreate):
    """Yangi post yaratish"""
    db_post = models.Post(
        title=post.title,
        content=post.content,
        author=post.author,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    """Postni yangilash (faqat yuborilgan maydonlar)"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None

    # Faqat yuborilgan (None bo'lmagan) maydonlarni yangilash
    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    """Postni o'chirish"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return False

    db.delete(db_post)
    db.commit()
    return True
