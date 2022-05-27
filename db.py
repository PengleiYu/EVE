from sqlalchemy import Table, Column, String, Integer, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class MineOrder(Base):
    __tablename__ = 'mineOrder'
    order_id = Column(Integer(), primary_key=True)
    mine_name = Column(String(10))
    price = Column(Integer())
    volume = Column(Integer())
    is_ice = Column(Boolean(), default=False)

    def __repr__(self):
        return f"MineOrder(mine_name='{self.mine_name}',price='{self.price}',volume='{self.volume}')"


engine = create_engine('sqlite:///eve.sqlite', echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
