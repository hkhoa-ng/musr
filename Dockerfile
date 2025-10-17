# Use an official Python runtime as the base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    OPENAI_API_KEY=""  
# Default (override at runtime)

# Set the working directory
WORKDIR /src

# Copy dependencies file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Run RAG database script first, then start the main application
CMD ["bash", "-c", "python /src/app/tools/rag_database.py --reset && python /src/app/main.py"]
# CMD ["bash", "-c", "python /src/app/main.py"]