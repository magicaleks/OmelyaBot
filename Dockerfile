# Dockerfile for run.py

FROM python:3
# FROM d0a59aeea3bc
COPY . /app/
# COPY requirements.txt /
WORKDIR /app/
# RUN python -m pip install --upgrade pip && pip install -r requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "run.py"]