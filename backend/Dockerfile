# minimal image
FROM python:3.13-slim
# cd in container
WORKDIR /app

# install dependencies in container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy codebase
COPY . .

# run uvicorn
ENTRYPOINT ["./run_docker.sh"]
CMD ["uvicorn", "main:API", "--host", "0.0.0.0", "--port", "8000"]
