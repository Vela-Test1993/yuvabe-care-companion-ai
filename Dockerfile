FROM python:3.11

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install dependencies and upgrade pip
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy remaining application code
COPY . /app

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Install additional dependencies
RUN apt-get update && apt-get install -y tmux curl

# Ensure the Hugging Face cache is set correctly
ENV TRANSFORMERS_CACHE="/app/.cache/huggingface"

# Set Python path
ENV PYTHONPATH="/app/src"

# Expose ports for both FastAPI (8000) and Streamlit (7860)
EXPOSE 8000 7860

# Combined startup with better control
CMD ["sh", "-c", "fastapi dev src/backend/main.py --host 0.0.0.0 --port 8000 & sleep 5 && streamlit run src/frontend/home.py --server.port 7860 --server.address 0.0.0.0"]