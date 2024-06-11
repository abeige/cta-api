import cta

client = cta.TransitClient()

etas = client.train.get_arrivals(40380)['ctatt']['eta']
result = map(lambda x: (x['rt'], x['destNm'], x['arrT']), etas)
for r in result:
    print(f"{r[0]} to {r[1]} arriving at {r[2][11:16]}")
