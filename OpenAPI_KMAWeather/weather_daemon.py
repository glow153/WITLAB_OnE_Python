import weather_fetcher_jake as wf
import datetime

toggle = True
while True:
    ctime = datetime.datetime.now()
    if (ctime.hour + 1) % 3 == 0:
        if toggle:
            wf.log_weather()
            toggle = False
    else:
        toggle = True


