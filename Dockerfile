# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the dependency files to the working directory
COPY pyproject.toml uv.lock* ./

# Install any needed packages specified in pyproject.toml
RUN uv pip install --system --no-cache .

# Copy the rest of the application's code to the working directory
COPY . .

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
