# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port Quart will run on
EXPOSE 5000

# Command to run the application
CMD ["hypercorn", "run:app", "--bind", "0.0.0.0:5000"]
