# bookly
fastapi personal project
python -m venv .venv (virtual environment important)
pip install fastapi
pip install uvicorn (server)
pip install python-dotenv
pip install -r requirements.txt
uvicorn main:app --reload (--port 8000)(optional)

To run the project simply write
python -m venv .venv 
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
