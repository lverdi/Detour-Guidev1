import googleMapsAPIPOC as api
import psycopg2

# routes = [
#     ('1417 Gum Branch Rd, Charlotte, NC 28214','3201 Broad Street, Philadelphia, PA 19148'),
#     ('400 D St, New Bern, NC 28560','611 Savannah Rd, Lewes, DE 19958'),
#     ('611 Savannah Rd, Lewes, DE 19958','4301 Atlantic Brigantine Blvd, Brigantine, NJ 08203'),
#     ('4301 Atlantic Brigantine Blvd, Brigantine, NJ 08203','79th St Transverse, New York, NY'),
#     ('79th St Transverse, New York, NY','2000 Montauk Point State Pkwy, Montauk, NY 11954'),
#     ('1287 NY-311, Patterson, NY 12563','4776 McKnight Rd, Pittsburgh, PA 15237'),
#     ('333 Hancock St, Quincy, MA 02171','578 Perry St, Buffalo, NY 14210'),
#     ('6 Needles Eye Rd, Pomfret Center, CT 06259','810 Weaver St, Larchmont, NY 10538'),
#     ('142 Bradford St, Provincetown, MA 02657','6 Needles Eye Rd, Pomfret Center, CT 06259'),
#     ('166 1st St, Swanton, VT 05488','92 MA-127, Rockport, MA 01966'),
#     ('Van Buren Rd, Van Buren, ME 04785','74 Hoit Rd, Concord, NH 03301'),
#     ('Natanis Point Rd, Eustis, ME 04936','35 March Rd, Sanbornton, NH 03269')]
    #('35 E Quay Rd, Key West, FL 33040','5789 US-17, Bartow, FL 33830'),
    #('185 NW Leonia Way, Lake City, FL 32055','9907 Front Beach Rd, Panama City Beach, FL 32407'),
    # ('5789 US-17, Bartow, FL 33830', '185 NW Leonia Way, Lake City, FL 32055'),
    # ('185 NW Leonia Way, Lake City, FL 32055','7345 Talbot Colony NE, Atlanta, GA 30328'),
    # ('185 NW Leonia Way, Lake City, FL 32055','261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464'),
    # ('7345 Talbot Colony NE, Atlanta, GA 30328','261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464'),
    # ('261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464','1417 Gum Branch Rd, Charlotte, NC 28214'),
    # ('261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464','1106 NC-24, Kenansville, NC 28349'),
    
#routes = [('3330-3340 Hillside Avenue, New Hyde Park, NY 11040','3 N Woods Ln, East Hampton, NY 11937'),
  #          ('93-30 Van Wyck Expy, Richmond Hill, NY 11418','420 Columbus Ave, New York, NY 10024')]

routes = [('28 Elm St, Potsdam, NY 13676','37 Stone Creek Ln, Briarcliff Manor, NY 10510'),
            ('10365 Bennett Rd, Fredonia, NY 14063','10365 Bennett Rd, Fredonia, NY 14063'),
            ('5855 NY-19, Belmont, NY 14813','7350 NY-28, Oneonta, NY 13820'),
            ('3962 NY-14, Himrod, NY 14842','3744 Green Rd, Locke, NY 13092')]

types = ['amusement_park','aquarium','art_gallery','campground','casino',
         'museum','night_club','park','zoo']

keywords = ['adventure','botanical garden','monument','beach', 'sightseeing','tour']

east_states = ['FL','GA','SC','NC','VA','MD','DC','NJ','PA','DE','ME','MA','NH','NY','RI','VT','WV','CT']
west_states = ['CA','WA','OR','NV']

for route in [routes[0]]:
    print(route)
    seen = set()
    conn = psycopg2.connect("dbname=my_app_db")
    cur = conn.cursor()
    for k in keywords[3:]:
        print(k)
        rst = api.generateSearchResults(route[0],route[1],keyword=k)
        for d in rst:
            if d['id'] in seen:
                pass
            seen.add(d['id'])
            if d['state'] in east_states:
                d['coast'] = 'east'
            elif d['state'] in west_states:
                d['coast'] = 'west'
            else:
                d['coast'] = 'other'
            try:
                cur.execute("""INSERT INTO places(name,address,coast,state,lat,lng,reviews,ratings,
                            types,photos) VALUES (%(name)s,%(address)s, %(coast)s,%(state)s,%(lat)s,
                            %(long)s,%(reviews)s,%(rating)s, %(types)s,%(photos)s);""", d)
                conn.commit()
            except:
                continue

for route in routes[1:]:
    print(route)
    seen = set()
    conn = psycopg2.connect("dbname=my_app_db")
    cur = conn.cursor()
    for t in types:
        print(t)
        rst = api.generateSearchResults(route[0],route[1], types=[t])
        for d in rst:
            if d['id'] in seen:
                pass
            seen.add(d['id'])
            if d['state'] in east_states:
                d['coast'] = 'east'
            elif d['state'] in west_states:
                d['coast'] = 'west'
            else:
                d['coast'] = 'other'
            try:
                cur.execute("""INSERT INTO places(name,address,coast,state,lat,lng,reviews,ratings,
                            types,photos) VALUES (%(name)s,%(address)s, %(coast)s,%(state)s,%(lat)s,
                            %(long)s,%(reviews)s,%(rating)s, %(types)s,%(photos)s);""", d)
                conn.commit()
            except:
                continue
            
    for k in keywords:
        print(k)
        rst = api.generateSearchResults(route[0],route[1],keyword=k)
        for d in rst:
            if d['id'] in seen:
                pass
            seen.add(d['id'])
            if d['state'] in east_states:
                d['coast'] = 'east'
            elif d['state'] in west_states:
                d['coast'] = 'west'
            else:
                d['coast'] = 'other'
            try:
                cur.execute("""INSERT INTO places(name,address,coast,state,lat,lng,reviews,ratings,
                            types,photos) VALUES (%(name)s,%(address)s, %(coast)s,%(state)s,%(lat)s,
                            %(long)s,%(reviews)s,%(rating)s, %(types)s,%(photos)s);""", d)
                conn.commit()
            except:
                continue
        





