PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

run-backend:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0

check:
	$(PYTHON) -m compileall backend frontend
