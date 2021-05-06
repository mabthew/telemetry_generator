FROM python:3.7.5-slim
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD tail -f /dev/null