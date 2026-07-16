load:
	python src/etl/loader.py

ratios:
	python src/analytics/ratio_engine.py

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --reload

test:
	pytest

clean:
	python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"