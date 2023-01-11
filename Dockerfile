FROM python
RUN pip install kubernetes
COPY rpi-logger-v3.py ./
CMD ["python","./rpi-logger-v3.py"]
