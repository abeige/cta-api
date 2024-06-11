from dotenv import load_dotenv
import os
import requests


class TransitClient:
    """
    # TransitClient
    """

    def __init__(self):
        env = os.path.join(os.getcwd(), '.env')

        if not load_dotenv(env):
            raise Warning('No .env file found in cwd')

        self.bus_api_key = os.getenv('BUS_API_KEY')
        self.train_api_key = os.getenv('TRAIN_API_KEY')

        self.bus = Bus(self.bus_api_key)
        self.train = Train(self.train_api_key)


class Transit:
    """
    # Transit
    """

    def __init__(self, key, url):
        self.key = key
        self.url = url

    def request(self, endpoint, params):
        params['key'] = self.key

        r = requests.get(self.url + endpoint, params=params)
        return r.json()

    def assert_id_len(self, *args):
        for arg in args:
            if arg:
                assert len(str(arg)) == 5, 'Station and stop IDs should be 5 characters'


class Train(Transit):
    """
    # Train
    """

    def __init__(self, key):
        url = 'http://lapi.transitchicago.com/api/1.0/'
        Transit.__init__(self, key, url)

    def get_arrivals(self, station_id=None, stop_id=None, max_results=None, route_code=None):
        """
        # get_arrivals

        #### Parameters:
        - station_id: required if stop_id not specified
        - stop_id: required if station_id not specified
        - max_results: optional
        - route_code: optional
        """

        assert bool(station_id) != bool(stop_id), "Specify exactly one of station_id or stop_id"
        self.assert_id_len(station_id, stop_id)

        endpoint = 'ttarrivals.aspx'
        params = {
            'mapid': station_id,
            'stpid': stop_id,
            'max': max_results,
            'rt': route_code,
            'outputType': 'json',
        }

        return self.request(endpoint, params)

    def follow(self, run_number):
        """
        # follow

        This API produces a list of arrival predictions for a given train at all subsequent stations for which that
        train is estimated to arrive, up to 20 minutes in the future or to the end of its trip.

        #### Parameters:
        - run_number: single run number for a train
        """

        endpoint = 'ttfollow.aspx'
        params = {
            'runnumber': int(run_number),
            'outputType': 'json',
        }

        return self.request(endpoint, params)

    def get_locations(self, route):
        """
        # get_locations

        This API produces a list of arrival predictions for a given train at all subsequent stations for which that
        train is estimated to arrive, up to 20 minutes in the future or to the end of its trip.

        #### Parameters:
        - route: one or more of the following routes
            - Red
            - Org
            - Y
            - G
            - Blue
            - P/Pexp
            - Pink
            - Brn
        """

        valid_routes = ( 'Red', 'Org', 'Y', 'G', 'Blue', 'P', 'Pexp', 'Pink', 'Brn' )
        assert route in valid_routes, "Route should be one of Red, Org, Y, G, Blue, P, Pexp, Pink, Brn"

        endpoint = 'ttpositions.aspx'
        params = {
            'rt': route,
            'outputType': 'json',
        }

        return self.request(endpoint, params)


class Bus(Transit):
    """
    # Bus
    """

    dir_abbrev = {
        'nb': 'Northbound',
        'sb': 'Southbound',
        'eb': 'Eastbound',
        'wb': 'Westbound',
    }

    def __init__(self, key):
        url = 'http://ctabustracker.com/bustime/api/v2/'
        Transit.__init__(self, key, url)

    def get_stops(self, route_code, direction):
        """
        # get_stops
        parameters:
        - route_code: bus route number
        - direction: nb, sb, eb, wb
        """

        endpoint = 'getstops'
        params = {
            'rt': route_code,
            'dir': self.dir_abbrev[direction],
            'format': 'json',
        }

        return self.request(endpoint, params)
