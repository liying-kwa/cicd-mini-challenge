from pydantic import BaseModel, Field


class Station(BaseModel):
    name: str = Field(..., alias="station_name")
    type: str
    latitude: float = Field(..., alias="lat")
    longitude: float = Field(..., alias="lng")

    def get_latlong(self):
        return [self.latitude, self.longitude]
