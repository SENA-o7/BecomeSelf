from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Kayıt olurken telefondan gelen veri."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Giriş yaparken telefondan gelen veri."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Başarılı girişte telefona verilen giriş kartı."""

    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    """Kullanıcı hakkında telefona geri gönderilen veri. Şifre burada yok."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime
