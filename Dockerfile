# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements if you have one (optional)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies
RUN pip install flask flasgger

# Copy the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
