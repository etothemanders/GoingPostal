#!env/bin/python
import os
from app import app

if __name__ == "__main__":
    # db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    # if not db_uri:
    #     db_uri = "sqlite:///shipments.db"
    # model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5050)), host="0.0.0.0")