FROM python:3.10

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies directly
RUN pip install --no-cache-dir fastapi uvicorn openenv-core>=0.2.0 requests numpy flask

# Expose the port
EXPOSE 8000

# Start the application using the 'main' function we will create
CMD ["python", "-c", "from server.app import main; main()"]
