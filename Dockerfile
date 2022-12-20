FROM python
RUN pip install psutil pyembedded
COPY rpi-logger.py ./
CMD ["python","./rpi-logger.py"]
