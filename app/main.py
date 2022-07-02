from typing import List

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from envirophat import light, weather, motion, analog, leds

import time
import datetime

app = FastAPI()

origins = ["*"] # Configured for public API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EnviroPhat FastAPI"}

@app.get("/enviro")
async def enviro(blink: bool = True):
    rgb = light.rgb()
    analog_values = analog.read_all()
    mag_values = motion.magnetometer()
    acc_values = [round(x, 2) for x in motion.accelerometer()]
    unit = 'hPa'  # Pressure unit, can be either hPa (hectopascals) or Pa (pascals)    
    output = {
        "enviro":{
            "temperature": round(weather.temperature(), 2),
            "pressure": round(weather.pressure(unit=unit), 2),
            "altitude": round(weather.altitude(), 2),
            "light": light.light(),
            "rgb": {"r": rgb[0], "g": rgb[1], "b": rgb[2]},
            "heading": motion.heading(),
            "magnetometer": {"mx": mag_values[0], "my": mag_values[1], "mz": mag_values[2]},
            "accelerometer": {"ax": acc_values[0], "ay": acc_values[1], "az": acc_values[2]},
            "analog": {"a0": analog_values[0], "a1": analog_values[1], "a2": analog_values[2], "a3": analog_values[3]}
        }
    }
    if blink is not False:
        leds.on()
        time.sleep(0.01)
        leds.off()

    return output  
    