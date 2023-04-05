FROM python:3.9

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 50000

CMD ["python", "main.py"]
