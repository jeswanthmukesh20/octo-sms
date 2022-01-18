FROM python:3.8-slim

RUN mkdir FastAPI

RUN pip install --upgrade pip   

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --quiet --no-cache-dir -r requirements.txt
EXPOSE 8001
COPY . /FastAPI
WORKDIR /FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]