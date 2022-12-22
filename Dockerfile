FROM python:3.9
COPY . /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8501
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]