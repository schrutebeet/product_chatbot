from database.connection import SessionLocal, engine
from database.models import Mercadona


res = SessionLocal().query(Mercadona).all()
print(res[1].id)