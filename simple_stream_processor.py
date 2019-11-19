import datetime
from typing import Union

import geopy.distance
import iso8601

from processor import Waypoint, Trip, StreamProcessor


GPS_DISTANCE_THRESHOLD = 15 # m
TRIP_MAX_STOP_DURATION = 180 # s

# Typical values for a small car, hardcoded for simplicity
VEHICLE_POWER = 60000 # W
VEHICLE_MASS = 1700 # kg
VEHICLE_MAX_DECELERATION = 3 # m/(s^2)
VEHICLE_MAX_SPEED = 70 # m/s


def distance(a: Waypoint, b: Waypoint) -> float:
    '''Distance in meters between two waypoints'''
    return geopy.distance.distance(
        (a.lat, a.lng),
        (b.lat, b.lng)
    ).m


def duration(a: Waypoint, b: Waypoint) -> datetime.timedelta:
    '''Elapsed time between two waypoints'''
    result = b.timestamp - a.timestamp
    if result < datetime.timedelta(seconds=0):
        raise ProcessingError('Waypoints not sorted')
    return result


def acceleration_feasible(
        speed_start: float,
        speed_end: float,
        duration: datetime.timedelta,
) -> bool:
    '''Check if the vehicle acceleration is within feasible range.
    The vehicle acceleration (kinetic energy increase) is limited by
    engine power. Deceleration is limited by brakes and tyre adhesion.
    '''

    if duration.seconds < 1:
        return True

    if speed_end <= speed_start:
        return (
            (speed_start - speed_end) / duration.seconds
            <= VEHICLE_MAX_DECELERATION
        )

    def kinetic_energy(speed: float):
        return VEHICLE_MASS * (speed ** 2) / 2

    return (
        kinetic_energy(speed_end) - kinetic_energy(speed_start)
    ) / duration.seconds <= VEHICLE_POWER


class ProcessingError(Exception):
    pass


class SerializableWaypoint(Waypoint):
    def __new__(cls, timestamp: str, lat: float, lng: float):
        return super().__new__(
            cls,
            timestamp=iso8601.parse_date(timestamp),
            lat=lat,
            lng=lng
        )

    @property
    def timestamp_str(self):
        return str(self.timestamp).replace('+00:00', 'Z').replace(' ', 'T')

    def json_dict(self):
        return {
            'timestamp': self.timestamp_str,
            'lat': self.lat,
            'lng': self.lng,
        }


class SerializableTrip(Trip):
    def __repr__(self):
        return str(self.json_dict())

    def json_dict(self):
        return {
            'start': self.start.json_dict(),
            'end': self.end.json_dict(),
            'distance': int(self.distance),
        }


class SimpleStreamProcessor(StreamProcessor):
    def __init__(self):
        self.start = None
        self.end = None
        self.moving = False
        self.distance = 0.0
        self.previous_speed = 0.0
        self.current_speed = 0.0

    def process_waypoint(self, waypoint: Waypoint) -> Union[Trip, None]:
        # initial waypoint
        if not self.start:
            self.start = waypoint
            self.end = waypoint
            return None

        elapsed_time = duration(self.end, waypoint)

        if (
                self.moving
                and elapsed_time > datetime.timedelta(
                    seconds=TRIP_MAX_STOP_DURATION
                )
                and distance(self.end, waypoint) < GPS_DISTANCE_THRESHOLD
        ):
            self.moving = False
            if self.distance > 0.0:
                return SerializableTrip(
                    distance=self.distance,
                    start=self.start,
                    end=self.end,
                )
            return None

        if distance(self.end, waypoint) < GPS_DISTANCE_THRESHOLD:
            # ignore waypoint
            return None

        if not self.moving:
            # setup a new trip
            self.start = waypoint
            self.end = waypoint
            self.moving = True
            self.distance = 0.0
            self.current_speed = 0.0
        else:
            # trip continues
            segment_distance = distance(self.end, waypoint)
            self.end = waypoint
            self.distance += segment_distance
            self.previous_speed = self.current_speed
            self.current_speed = segment_distance / elapsed_time.seconds

            # physics checks
            if self.current_speed > VEHICLE_MAX_SPEED:
                print('Vehicle speed too high')
            if not acceleration_feasible(
                    speed_start=self.previous_speed,
                    speed_end=self.current_speed,
                    duration=elapsed_time,
            ):
                print('Vehicle acceleration out of range')

        return None
