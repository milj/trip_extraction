# Trip extractor

Packages required:
```
pip install geopy iso8601 pytest pytest-describe expects
```

I chose to implement the `StreamProcessor` interface.

Usage:
```
extract_trips.py [-h] waypoint-file trip-file
```

Running tests:
```
pytest
```

# Assumptions

It is assumed for simplicity that JSON files can be loaded into momery
as a whole. Otherwise an iterative parser should be used.

It is assumed that the input waypoint stream is sorted by timestamp.

# Trip start detection

The first waypoint that is more than 15 meters away from the end position
of the previous trip becomes the starting point of the new trip. This means
that, if the waypoints come every minute, up to three kilometers of the trip
will be lost (@ 180 km/h). On the other hand this is a simple way to filter out
spurious trips consisting of a single waypoint more than 15 meters away,
because if there is no other waypoint even more away in the next 3 minutes,
the trip ends up being zero length and is ignored.

# GPS position "skip" detection:

There is a simple vehicle speed & acceleration check. It should
detect anomalous speeds and accelerations but for simplicity it treats
the vehicle speed as a scalar, not a vector, so it won't detect sudden
physically impossible turns. It also doesn't account for the possibility
that the vehicle may be going down a steep hill (accelerated by gravity
in addition to the engine). An elevation map would be useful here to
determine if that is the case.

For the provided test data there were no anomalous speeds and accelerations
detected. Therefore I did not implement any track smoothing / outlier
filtering.

# Not implemented ideas:

Best solution would be an algorithm similar to what satelite navigation
software is doing: to have a map and use it to correct the GPS position
by snapping the car to the nearest drivable surface (with provisions for
staying on track on viaduct over another road etc.). This would help
to filter out GPS position "jumping" and give the precise track driven,
especially important on the crossings.

Another idea is to use a Kalman filter for better estimation of the current
position and velocity vector from the noisy GPS data.
