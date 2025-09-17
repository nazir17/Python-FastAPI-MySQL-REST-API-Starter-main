from pydantic import BaseModel

class RoleBase(BaseModel):
    role: str

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True
