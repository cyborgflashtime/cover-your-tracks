import MySQLdb

import config


class Db(object):

    def __init__(self):
        self.host = config.db_host
        self.username = config.db_username
        self.password = config.db_password
        self.database = config.db_database
        self.port = config.db_port

    def connect(self):
        self.cxn = MySQLdb.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            db=self.database,
            port=self.port)

    def count_sightings(self, cookie, signature):
        c = self.cxn.cursor()
        c.execute("""SELECT COUNT(cookie_id) FROM cookies
            WHERE cookie_id=%s AND signature=%s""", (str(cookie), signature))
        return c.fetchone()[0]

    def record_sighting(self, cookie, signature, ip, google_style_ip, timestamp):
        c = self.cxn.cursor()
        c.execute("""INSERT INTO cookies SET
            cookie_id=%s,
            signature=%s,
            ip=%s,
            ip34=%s,
            timestamp=%s""", (
            str(cookie),
            signature,
            ip,
            google_style_ip,
            timestamp
        )
        )
        self.cxn.commit()

    def record_fingerprint(self, whorls):
        c = self.cxn.cursor()
        exec_str = "INSERT INTO fingerprint SET "
        exec_str += ", ".join(map(lambda x: x + "=%s", whorls.keys()))
        exec_str += " ON DUPLICATE KEY UPDATE count=count + 1"
        c.execute(exec_str, tuple(whorls.values()))
        self.cxn.commit()

    def update_totals(self, whorls):
        c = self.cxn.cursor()
        update_str = "INSERT INTO totals SET total=1, variable=%s,value=%s ON DUPLICATE KEY UPDATE total=total+1"
        c.execute(update_str, ('count', ''))
        for i in whorls:
            c.execute(update_str, (i, whorls[i]))
        self.cxn.commit()