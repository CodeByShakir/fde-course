import httpx
from pydantic import BaseModel

URL = "https://api.open-meteo.com/v1/forecast"


class CurrentWeather(BaseModel):
    time: str
    temperature_2m: float
    wind_speed_10m: float


class Forecast(BaseModel):
    latitude: float
    longitude: float
    current: CurrentWeather


def get_forecast(latitude: float, longitude: float) -> Forecast:
    response = httpx.get(
        URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )
    response.raise_for_status()
    return Forecast.model_validate(response.json())


karachi = get_forecast(24.86, 67.01)
print(f"{karachi.current.temperature_2m}°C, wind {karachi.current.wind_speed_10m} km/h")
