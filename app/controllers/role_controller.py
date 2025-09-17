from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.role_schema import RoleCreate, RoleOut
from app.services import role_service

router = APIRouter()

@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_service.create_role(db, role)

@router.get("/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)

@router.put("/assign/{user_id}/{role_id}")
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    updated_user = role_service.assign_role(db, user_id, role_id)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "Role assigned successfully", "user_id": updated_user.id, "role": updated_user.role.role}
