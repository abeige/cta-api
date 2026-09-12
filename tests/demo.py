import cta

client = cta.TransitClient()

# etas = client.train.get_arrivals(40380)['ctatt']['eta']
# for e in etas:
#     print(f"He['rt']} to {e['destNm']} arriving at {e['arrT'][11:16]}")

stops = client.bus.get_stops(8, 'nb')['bustime-response']['stops']
for s in stops:
    print(f"{s['stpnm']}: {s['stpid']}")

# run_number = client.train.get_arrivals(40380)['ctatt']['eta'][0]['rn']
# print(run_number)
# print(client.train.follow(715))