FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask numpy requests
RUN pip install .

EXPOSE 5000

CMD ["python", "app.py"]
