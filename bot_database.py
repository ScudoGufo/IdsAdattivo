#!/usr/bin/python3
import pymysql

INSERT_IP="INSERT INTO ip (addres) VALUES ('{}')"
INSERT_IPS="INSERT INTO ips (provider) VALUES ('{}')"
INSERT_PAYLOAD="INSERT INTO payload (url , verb) VALUES ('{}', '{}')"
INSERT_ZONA="INSERT INTO zone (zone) VALUES ('{}')"
INSERT_LOG="INSERT INTO logs (ip, zone, payload, ips, time ) VALUES ({},{},{},{}, NOW())"

CHECK_IP="SELECT id FROM ip WHERE addres='{}'"
CHECK_IPS="SELECT id FROM ips WHERE provider='{}'"
CHECK_ZONA="SELECT id FROM zone WHERE zone='{}'"

INFO_LOG_NUMBERS="SELECT COUNT(*) FROM logs"

SELECT_LOG="\
SELECT ip.addres, zone.zone, ips.provider\
FROM logs \
INNER JOIN ip ON logs.ip=ip.id \
INNER JOIN zone ON logs.zone=zone.id \
INNER JOIN ips ON logs.ips=ips.id \
;"


def init():
    db=pymysql.connect("localhost","honeydba","honeydba","honey_log") #This saves a connection object into db
    cursor=db.cursor()
    print('[*] Database Connected')
    return [db, cursor] 

def clear_input(db, data):
    for x in data:
        x = db.escape(x)
    return x

def insert_ip(db, cursor, data):
    query = CHECK_IP.format(data)
    cursor.execute(query)
    id = cursor.fetchone()
    if id == None: 
        query = INSERT_IP.format(data)
        cursor.execute(query)
        db.commit()
        return cursor.lastrowid
    return id[0]

def insert_ips(db, cursor, data):
    query = CHECK_IPS.format(data)
    cursor.execute(query)
    id = cursor.fetchone()
    if id == None: 
        query = INSERT_IPS.format(data)
        cursor.execute(query)
        db.commit()
        return cursor.lastrowid
    return id[0]

def insert_zone(db, cursor, data):
    query = CHECK_ZONA.format(data)
    cursor.execute(query)
    id = cursor.fetchone()
    if id == None: 
        query = INSERT_ZONA.format(data)
        cursor.execute(query)
        db.commit()
        return cursor.lastrowid
    return id[0]

def insert_pl(db, cursor, data):
    query = INSERT_PAYLOAD.format(data[0], data[1])
    cursor.execute(query)
    db.commit()
    return cursor.lastrowid

def insert_request(db, cursor, data, intelipapi, intelshodan):
    ip = insert_ip(db, cursor, data.ip)
    pl = insert_pl(db, cursor, [data.path, data.verb])
    ips = insert_ips(db, cursor, intelipapi.isp)
    zone = insert_zone(db, cursor, "{}:{}".format(intelipapi.country, intelipapi.city))

    query = INSERT_LOG.format(ip, zone, pl, ips)
    cursor.execute(query)
    db.commit()

def get_info(cursor):
    cursor.execute(INFO_LOG_NUMBERS)
    number = cursor.fetchone()
    return "Sono presenti {} records".format(number[0])

def close(db, cursor):
    cursor.close()
    db.close()
    print('[*] Database Connection Closed')

'''
db, cursor = init()
data={\
"ip":"127.0.0.1",\
"pl":["/ciccina/test","GET"],\
"ips":"tecnotoot",\
"zone":"italia"\
}
insert_request(db, cursor,  data)
close(db, cursor)
'''