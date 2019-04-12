import googleMapsAPIPOC as api
import psycopg2

routes = [('35 E Quay Rd, Key West, FL 33040','5789 US-17, Bartow, FL 33830'),
    ('5789 US-17, Bartow, FL 33830', '185 NW Leonia Way, Lake City, FL 32055'),
    ('185 NW Leonia Way, Lake City, FL 32055','9907 Front Beach Rd, Panama City Beach, FL 32407'),
    ('185 NW Leonia Way, Lake City, FL 32055','7345 Talbot Colony NE, Atlanta, GA 30328'),
    ('185 NW Leonia Way, Lake City, FL 32055','261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464'),
    ('7345 Talbot Colony NE, Atlanta, GA 30328','261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464'),
    ('261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464','1417 Gum Branch Rd, Charlotte, NC 28214'),
    ('261 Johnnie Dodds Blvd, Mt Pleasant, SC 29464','1106 NC-24, Kenansville, NC 28349'),
    ('1417 Gum Branch Rd, Charlotte, NC 28214','3201 Broad Street, Philadelphia, PA 19148'),
    ('400 D St, New Bern, NC 28560','611 Savannah Rd, Lewes, DE 19958'),
    ('611 Savannah Rd, Lewes, DE 19958','4301 Atlantic Brigantine Blvd, Brigantine, NJ 08203'),
    ('4301 Atlantic Brigantine Blvd, Brigantine, NJ 08203','79th St Transverse, New York, NY'),
    ('79th St Transverse, New York, NY','2000 Montauk Point State Pkwy, Montauk, NY 11954'),
    ('1287 NY-311, Patterson, NY 12563','4776 McKnight Rd, Pittsburgh, PA 15237'),
    ('333 Hancock St, Quincy, MA 02171','578 Perry St, Buffalo, NY 14210'),
    ('6 Needles Eye Rd, Pomfret Center, CT 06259','810 Weaver St, Larchmont, NY 10538'),
    ('142 Bradford St, Provincetown, MA 02657','6 Needles Eye Rd, Pomfret Center, CT 06259'),
    ('166 1st St, Swanton, VT 05488','92 MA-127, Rockport, MA 01966'),
    ('Van Buren Rd, Van Buren, ME 04785','74 Hoit Rd, Concord, NH 03301'),
    ('Natanis Point Rd, Eustis, ME 04936','35 March Rd, Sanbornton, NH 03269')]

types = ['amusement_park','aquarium','art_gallery','campground','casino',
         'food','library','movie_theater','museum','night_club','park','place_of_worship',
         'shopping_mall','spa','zoo']

keywords = ['family friendly', 'adventure', 'outdoor', 'tourist','attraction','landmark','nature',
            'children','entertainment','theater','hiking','plaza','sports',
            'monument','music','culture','religion','leisure','history','beach','art',
            'sightseeing','tour']

east_states = ['FL','GA','SC','NC','VA','MD','DC','NJ','PA','DE','ME','MA','NH','NY','RI','VT','WV','CT']


for route in routes:
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
            else:
                d['coast'] = 'west'
            cur.execute("""INSERT INTO "Places"(name,address,coast,state,lat,lng,reviews,ratings,
                        types,photos) VALUES (%(name)s,%(address)s, %(coast)s,%(state)s,%(lat)s,
                        %(long)s,%(reviews)s,%(rating)s, %(types)s,%(photos)s);""", d)
            conn.commit()
            
    for k in keywords:
        print(k)
        rst = api.generateSearchResults(route[0],route[1],keyword=k)
        for d in rst:
            if d['id'] in seen:
                pass
            seen.add(d['id'])
            if d['state'] in east_states:
                d['coast'] = 'east'
            else:
                d['coast'] = 'west'
            cur.execute("""INSERT INTO "Places"(name,address,coast,state,lat,lng,reviews,ratings,
                        types,photos) VALUES (%(name)s,%(address)s, %(coast)s,%(state)s,%(lat)s,
                        %(long)s,%(reviews)s,%(rating)s, %(types)s,%(photos)s);""", d)
            conn.commit()
        





