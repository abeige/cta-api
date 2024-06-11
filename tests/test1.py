import cta

conn = cta.TransitClient()
stops = conn.bus.get_stops(8, 'nb')
print(type(stops))

arrivals = conn.train.get_arrivals(41220)
print(type(arrivals))

conn.train.get_arrivals()