FROM python:3.10 as base
# EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install debugpy

WORKDIR /app/
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client  -m flask run -h 0.0.0.0 -p 5000

###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod

# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]