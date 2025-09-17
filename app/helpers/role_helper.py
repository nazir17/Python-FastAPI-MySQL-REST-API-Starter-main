from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.role_model import Role
from app.schemas.role_schema import RoleCreate

def create_role(db: Session, role: RoleCreate):
    existing = db.query(Role).filter(Role.role == role.role).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    new_role = Role(role=role.role)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_roles(db: Session):
    return db.query(Role).all()

def assign_role(db: Session, user, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user
