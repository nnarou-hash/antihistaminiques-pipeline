FROM python:3.9.0

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir notebooks

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app/notebooks"]
