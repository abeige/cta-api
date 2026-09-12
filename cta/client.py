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

        # set output type to json for bus and train
        outputSpecifier = 'format' if type(self) == Bus else 'outputType'
        params[outputSpecifier] = 'json'

        r = requests.get(self.url + endpoint, params=params)
        return r.json()

    def assert_id_len(self, *args):
        for arg in args:
            if arg is not None:
                if type(self) == Bus:
                    assert int(arg) >= 0 and int(arg) < 30000, 'Bus stop IDs should be between 0 and 29999'
                elif type(self) == Train:
                    assert int(arg) >= 30000 and int(arg) < 50000, 'Train station and stop IDs should be between 30000 and 49999'


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
        url = 'http://ctabustracker.com/bustime/api/v3/'
        Transit.__init__(self, key, url)

    def get_time(self, unix_time=None):
        """
        # get_time

        Use the gettime request to retrieve the current system date and time. Since BusTime is a time-dependent
        system, it is important to synchronize your application with BusTime's system date and time.

        Returns local time YYYYMMDD HH:MM:SS

        #### Parameters:
        - unix_time (optional): if true, return milliseconds since 00:00:00 UTC (Thursday, 1 January 1970)
        """

        endpoint = 'gettime'
        params = {
            'unixTime': unix_time,
        }

        return self.request(endpoint, params)

    def get_vehicles(self, vehicle_id=None, route=None, time_res=None):
        """
        # get_vehicles

        Use the getvehicles request to retrieve vehicle information (i.e., locations) of all or a subset of vehicles currently being tracked by BusTime.

        Note: The vehicle_id and route parameters cannot be combined in one request. If both parameters are specified, only the first parameter specified on the request will be processed.

        #### Parameters:
        - vehicle_id: one or more vehicle IDs (max 10)
        - route: one or more route codes (max 10)
        - time_res: resolution of timestamps - 's' or 'm', optional; default 'm'
        """

        assert bool(vehicle_id) ^ bool(route), 'Only one of vehicle_id or route can be specified'

        endpoint = 'getvehicles'
        params = {
            'vid': vehicle_id,
            'rt': route,
            'tmres': time_res,
        }

        return self.request(endpoint, params)

    def get_routes(self):
        """
        # get_routes

        Retrieve set of routes serviced by the system
        """

        endpoint = 'getroutes'
        params = { }

        return self.request(endpoint, params)

    def get_directions(self, route):
        """
        # get_directions 

        Retrieve set of directions serviced by the specific route

        #### Parameters:
        - route: single route designator
        """

        endpoint = 'getdirections'
        params = {
            'rt': route,
        }

        return self.request(endpoint, params)

    def get_stops(self, route=None, direction=None, stop_id=None):
        """
        # get_stops

        Use the getstops request to retrieve the set of stops for the specified route and direction.

        Stop lists are only available for a valid route/direction pair. A list of all stops that service a particular route regardless of direction cannot be requested.

        #### Parameters:
        - route: bus route code
        - direction: nb, sb, eb, wb
        - stop_id: required if route and direction not provided
        """
        assert (bool(route) and bool(direction)) ^ bool(stop_id), 'A request must provide either a rt & dir or up to 10 stpids, but not both.'

        self.assert_id_len(stop_id)

        endpoint = 'getstops'
        params = {
            'rt': route,
            'dir': self.dir_abbrev[direction],
            'stpid': stop_id
        }

        return self.request(endpoint, params)

    def get_patterns(self, pattern_id=None, route=None):
        """
        # get_patterns 

        Use the getpatterns request to retrieve the set of geo-positional points and stops that when connected can be used to construct the geo-positional layout of a pattern (i.e., route variation).

        The pattern_id and route parameters cannot be combined in one request. If both are specified, only the first parameter specified on the request will be processed.

        #### Parameters:
        - pattern_id: One or more pattern IDs whose points should be returned (max 10)
        - route: single route designator for which all active patterns should be returned
        """

        endpoint = 'getpatterns'
        params = {
            'pid': pattern_id,
            'rt': route,
        }

        return self.request(endpoint, params)

    def get_predictions(self, stop_id=None, route=None, vehicle_id=None, top=None):
        """
        # get_predictions

        Use the getpredictions request to retrieve predictions for one or more stops or one or more vehicles. Predictions are always returned in ascending order according to prdtm.

        #### Parameters:
        - stop_id: one or more stop IDs (max 10), not available with `vehicle_id`
        - route: one or more route designators, optional, available with `stop_id`
        - vehicle_id: one or more vehicle IDs (max 10), not available with `stop_id`
        - top: maximum number of predictions to be returned
        """

        assert bool(stop_id) ^ bool(vehicle_id), 'Only one of stop_id and vehicle_id can be specified'
        if vehicle_id:
            assert route is None, 'Route parameter is not available with vehicle_id'
        if stop_id:
            self.assert_id_len(stop_id)

        endpoint = 'getpredictions'
        params = {
            'stpid': stop_id,
            'rt': route,
            'vid': vehicle_id,
            'top': top,
        }

        return self.request(endpoint, params)

    def get_service_bulletins(self, route, direction, stop_id):
        """
        # get_service_bulletins

        Use the getservicebulletins for a list of service bulletins that are in effect for a route(s) (rt), route & direction (rt & rtdir), route & direction & stop (rt & rtdir & stpid), or stop(s) (stpid). At a minimum, the rt or stpid parameter must be specified.

        A service bulletin (sb) definition without a srvc element indicates a “system-wide” service bulletin. System- wide service bulletins are valid for all routes/stops in the system.

        #### Parameters:
        - route: one or more route designators - if combined with `direction`, only one may be specified
        - direction: direction of travel of specified route
        - stop_id: one or more stop IDs. if combined with `route` and `direction`, only one may be specified
        """

        self.assert_id_len(stop_id)

        endpoint = 'getservicebulletins'
        params = {
            'rt': route,
            'rtdir': direction,
            'stpid': stop_id,
        }

        return self.request(endpoint, params)
