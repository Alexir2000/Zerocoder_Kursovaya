from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

Base = declarative_base()

class Zhurnal_status_Zakaza(Base):
    __tablename__ = 'zhurnal_status_zakaza'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Zakaza = Column(Integer, ForeignKey('zakaz.ID'), nullable=False)
    Izmenenie = Column(String(255), nullable=False)
    pole_izm = Column(String(255), nullable=True)
    json_str = Column(String(600), nullable=False)
    Date = Column(DateTime, nullable=True, default=None)
    peredano = Column(Boolean, default=False)

# Создаем соединение с базой данных
DATABASE_URL = "sqlite:///../db.sqlite3"  # замените на URL вашей базы данных
engine = create_engine(DATABASE_URL)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Удаляем все записи из таблицы Zhurnal_status_Zakaza
try:
    num_rows_deleted = session.query(Zhurnal_status_Zakaza).delete()
    session.commit()
    print(f"{num_rows_deleted} записей было удалено.")
except Exception as e:
    session.rollback()
    print(f"Произошла ошибка: {e}")
finally:
    session.close()
