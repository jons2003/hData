FROM python:3.13.0a2-bookworm
WORKDIR /opt/coin

COPY ./requirements.txt /opt/coindex/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install bs4

COPY . /opt/coin

VOLUME /opt/coin/data
CMD ["python", "historical-data.py"] 
