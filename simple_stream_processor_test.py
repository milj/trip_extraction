from expects import *
import pytest

from simple_stream_processor import (
    SerializableWaypoint, SerializableTrip, SimpleStreamProcessor
)


def describe_process_waypoint():

    # 0.0001 degree of longitude on equator = 11.1 m
    @pytest.mark.parametrize("test_data", [
        [
            # spurious movement by 22 meters
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0001, 'timestamp': '2018-01-10T12:00:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'}, None),
            ({'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:04:00Z'}, None),
        ],
        [
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0001, 'timestamp': '2018-01-10T12:00:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'}, None),
            ({'lat': 0.0, 'lng': 0.0003, 'timestamp': '2018-01-10T12:00:03Z'}, None),
            ({'lat': 0.0, 'lng': 0.0004, 'timestamp': '2018-01-10T12:00:04Z'}, None),
            ({'lat': 0.0, 'lng': 0.0005, 'timestamp': '2018-01-10T12:04:00Z'}, {
                'start': {'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'},
                'end':   {'lat': 0.0, 'lng': 0.0004, 'timestamp': '2018-01-10T12:00:04Z'},
                'distance': 22,
            }),
            ({'lat': 0.0, 'lng': 0.0005, 'timestamp': '2018-01-10T12:05:00Z'}, None),
        ],
        [
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0001, 'timestamp': '2018-01-10T12:00:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'}, None),
            ({'lat': 0.0, 'lng': 0.0003, 'timestamp': '2018-01-10T12:00:03Z'}, None),
            ({'lat': 0.0, 'lng': 0.0003, 'timestamp': '2018-01-10T12:01:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0005, 'timestamp': '2018-01-10T12:01:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:01:02Z'}, None),
            ({'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:02:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:04:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:04:03Z'}, {
                'start': {'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'},
                'end':   {'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:01:02Z'},
                'distance': 55,
            }),
            ({'lat': 0.0, 'lng': 0.0007, 'timestamp': '2018-01-10T12:05:00Z'}, None),
        ],
        [
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0001, 'timestamp': '2018-01-10T12:00:01Z'}, None),
            ({'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'}, None),
            # 1 waypoint per 2h (patchy network, vehicle driven non stop):
            ({'lat': 0.0, 'lng': 1.0000, 'timestamp': '2018-01-10T14:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 2.0000, 'timestamp': '2018-01-10T16:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 3.0000, 'timestamp': '2018-01-10T18:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 3.0000, 'timestamp': '2018-01-10T18:02:59Z'}, None),
            ({'lat': 0.0, 'lng': 3.0000, 'timestamp': '2018-01-10T19:00:00Z'}, {
                'start': {'lat': 0.0, 'lng': 0.0002, 'timestamp': '2018-01-10T12:00:02Z'},
                'end':   {'lat': 0.0, 'lng': 3.0000, 'timestamp': '2018-01-10T18:00:00Z'},
                'distance': 333936,
            }),
        ],
        [
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:00:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:01:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:02:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0000, 'timestamp': '2018-01-10T12:03:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0050, 'timestamp': '2018-01-10T12:04:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0100, 'timestamp': '2018-01-10T12:05:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0150, 'timestamp': '2018-01-10T12:06:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:07:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:08:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:09:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:10:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:11:00Z'}, {
                'start': {'lat': 0.0, 'lng': 0.0050, 'timestamp': '2018-01-10T12:04:00Z'},
                'end':   {'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:07:00Z'},
                'distance': 1669,
            }),
            ({'lat': 0.0, 'lng': 0.0200, 'timestamp': '2018-01-10T12:16:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0250, 'timestamp': '2018-01-10T12:17:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0300, 'timestamp': '2018-01-10T12:18:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:19:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:20:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:21:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:22:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:23:00Z'}, {
                'start': {'lat': 0.0, 'lng': 0.0250, 'timestamp': '2018-01-10T12:17:00Z'},
                'end':   {'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:19:00Z'},
                'distance': 1113,
            }),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:25:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:27:00Z'}, None),
            ({'lat': 0.0, 'lng': 0.0350, 'timestamp': '2018-01-10T12:29:00Z'}, None),
        ],
    ])
    def it_extracts_trips(test_data):
        processor = SimpleStreamProcessor()
        for waypoint_entity, expected_result in test_data:
            waypoint = SerializableWaypoint(
                timestamp=waypoint_entity['timestamp'],
                lat=waypoint_entity['lat'],
                lng=waypoint_entity['lng'],
            )
            result = processor.process_waypoint(waypoint)
            if isinstance(result, SerializableTrip):
                expect(result.json_dict()).to(equal(expected_result))
            else:
                expect(result).to(equal(expected_result))
