import cta

client = cta.TransitClient()

etas = client.train.get_arrivals(40380)['ctatt']['eta']
etas = map(lambda x: (x['rt'], x['destNm'], x['arrT']), etas)
for e in etas:
    print(f"{e[0]} to {e[1]} arriving at {e[2][11:16]}")

stops = client.bus.get_stops(8, 'nb')['bustime-response']['stops']
stops = map(lambda x: (x['stpid'], x['stpnm']), stops)
for s in stops:
    print(f"{s[1]}: {s[0]}")

client.train.assert_id_len(200)
