#!.venv/bin/python

import argparse
import json
import sys

from simple_stream_processor import (
    SerializableWaypoint, SimpleStreamProcessor
)


def main(args):
    parser = argparse.ArgumentParser(
        description='Extract a list of trips from a list of waypoints.'
    )
    parser.add_argument(
        'waypoint_file',
        help='input JSON file containing waypoints',
        metavar='waypoint-file',
        type=str,
    )
    parser.add_argument(
        'trip_file',
        help='output JSON file containg extracted trips',
        metavar='trip-file',
        type=str,
    )
    args = parser.parse_args(args)

    with open(args.waypoint_file) as waypoint_file:
        waypoint_list = json.load(waypoint_file)

    processor = SimpleStreamProcessor()
    trips = []

    for waypoint_entity in waypoint_list:
        waypoint = SerializableWaypoint(
            timestamp=waypoint_entity['timestamp'],
            lat=waypoint_entity['lat'],
            lng=waypoint_entity['lng'],
        )
        trip = processor.process_waypoint(waypoint)
        if trip:
            trips.append(trip)

    with open(args.trip_file, 'w', encoding='utf-8') as trip_file:
        json.dump(
            [trip.json_dict() for trip in trips],
            trip_file,
            indent=2,
        )


if __name__ == '__main__':
    main(sys.argv[1:])
