# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . ./app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install virtualenv && \
    pip install contextily && \
    pip install imageio && \
    pip install matplotlib-scalebar && \
    pip install git+https://github.com/terensis/eodal_basetiffs_GPL3

# Make port 80 available to the world outside this container
EXPOSE 80

# Run eodal_basetiffs.sh when the container launches
ENTRYPOINT ["./eodal_basetiffs.sh",]