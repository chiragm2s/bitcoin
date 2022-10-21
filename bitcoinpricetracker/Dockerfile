FROM python:latest
ENV TZ="Asia/Kolkata"

#############
############ Adding cronjob content ########
# RUN apt-get update && apt-get install -y apt-utils && apt-get install cron -y && apt-get install -y apt-utils && apt-get upgrade -y && /usr/local/bin/python -m pip install --upgrade pip
#ADD cronjobs /etc/cron.d/cronjobs
#RUN chmod 0644 /etc/cron.d/cronjobs && touch /cron.log && crontab /etc/cron.d/cronjobs
######
ADD . /bitcoin
WORKDIR /bitcoin
# RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py","runserver"]
