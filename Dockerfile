FROM python:3.11.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
