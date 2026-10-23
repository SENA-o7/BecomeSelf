from datetime import datetime

from sqlalchemy import DateTime, String, func  #veritabanındaki sütun tipleri ve veritabanı fonksiyonları

from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
"""Mapped[str] → "Python'da bu bir metin". VS Code bu sayede otomatik tamamlama yapabiliyor.
String(255) → "Veritabanında en fazla 255 karakterlik metin"
unique=True → "Aynı değer iki kez olamaz". Aynı e-postayla ikinci kayıt girişimini veritabanının kendisi reddeder.
index=True → "Bu sütunda hızlı arama yap". Girişte e-postaya göre kullanıcı arayacağız. Index, kitabın sonundaki dizin gibi: binlerce kullanıcı olsa da aramak anında olur."""