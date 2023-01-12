FROM python:alpine
WORKDIR /mt
COPY . .
EXPOSE 80
RUN pip install pymongo \
pip install pytelegrambotapi
ENTRYPOINT [ "python", "MeasTools.py" ]
