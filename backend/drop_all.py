from app import create_app
from app.extensions.database import db

app = create_app()

with app.app_context():
    db.reflect()
    db.drop_all()
    
    # We also need to drop the alembic_version table manually if db.drop_all() misses it
    with db.engine.begin() as conn:
        conn.exec_driver_sql("DROP TABLE IF EXISTS alembic_version")
        
    print("All tables dropped successfully.")
