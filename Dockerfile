FROM python
RUN pip install psutil pyembedded
COPY rbp-logger.py ./
CMD ["python","./rbp-logger.py"]
