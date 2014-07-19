#!env/bin/python
import os
from app import app

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5050)), host="0.0.0.0")