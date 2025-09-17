from sqlalchemy.orm import Session
from app.helpers import role_helper
from app.schemas.role_schema import RoleCreate
from app.models.user_model import User

def create_role(db: Session, role: RoleCreate):
    return role_helper.create_role(db, role)

def get_roles(db: Session):
    return role_helper.get_roles(db)

def assign_role(db: Session, user_id: int, role_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return role_helper.assign_role(db, user, role_id)
