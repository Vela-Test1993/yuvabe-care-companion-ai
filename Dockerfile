FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 7860

# Ensure logs directory exists
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Install tmux to run multiple processes
RUN apt-get update && apt-get install -y tmux

# Start FastAPI & Streamlit together using tmux

CMD ["sh", "-c", "uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 & sleep 5 && streamlit run src/frontend/home.py --server.port 7860 --server.address 0.0.0.0"]