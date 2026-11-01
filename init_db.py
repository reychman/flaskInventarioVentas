from app import app, db
from app.models import Categoria

with app.app_context():
    metadata = Categoria.metadata
    for tabla in metadata.sorted_tables:
        print("--", tabla.name)
    metadata.create_all(bind=db.engine)
    print("Tablas creadas correctamente")