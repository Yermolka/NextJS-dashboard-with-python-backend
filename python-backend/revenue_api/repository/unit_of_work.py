from typing import Self
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class UnitOfWork:
    def __init__(self) -> None:
        self.session_maker = sessionmaker(
            bind=create_engine(os.getenv('DATABASE_URL'))
        )

    def __enter__(self) -> Self:
        self.session = self.session_maker()
        return self
    
    def __exit__(self, exc_type, exc_val, traceback) -> None:
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()