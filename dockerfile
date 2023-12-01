# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install virtualenv && \
    pip install contextily && \
    pip install imageio && \
    pip install matplotlib-scalebar

# make the script executable
RUN chmod +x ./eodal_basetiffs.sh

# Run eodal_basetiffs.sh when the container launches
ENTRYPOINT ["./eodal_basetiffs.sh"]