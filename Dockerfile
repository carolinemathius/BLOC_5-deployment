# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory to /home/app
WORKDIR /home/app

# Copy the current directory contents into the container at /app
COPY . /home/app

# Clear the pip cache
RUN pip cache purge

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "api-app:app", "--host", "0.0.0.0", "--port", "80"]
