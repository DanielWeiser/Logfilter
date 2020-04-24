if __name__ == '__main__':

    from systemd import journal
    from os import listdir
    from os.path import isfile, join
    import re
    import MySQLdb
    import config

    def db_insert_log(entry, danger):
        data = (entry['_SYSTEMD_UNIT'], entry['MESSAGE'], entry['PRIORITY'], entry['_SOURCE_REALTIME_TIMESTAMP'], danger)
        cursor.execute(insert_str, data)
        db.commit()

    j = journal.Reader()
    j.this_boot()

    #service_list - array of filenames in rules/
    service_list = [f for f in listdir("/etc/logfilterd/rules/") if isfile(join("/etc/logfilterd/rules/", f))]

    fds = list()
    for service in service_list:
        j.add_match(_SYSTEMD_UNIT = service)
        path = "/etc/logfilterd/rules/" + service
        fds.append(open(path, "r"))

    rules = dict()
    for i in range(0, len(service_list)):
        #read rules from files in rules/ to dict where key - service, value - array of rules
        rules[service_list[i]] = fds[i].read().splitlines()
        fds[i].close()

    db = MySQLdb.connect(config.mysql["host"], config.mysql["user"], config.mysql["password"], config.mysql["db"])
    cursor = db.cursor()

    insert_str = "INSERT INTO IDS_log (unit, message, priority, timestamp, danger) VALUES (%s, %s, %s, %s, %s)"

    while True:
        for entry in j:
            for service in service_list:
                if entry['_SYSTEMD_UNIT'] == service:
                    for rule in rules[service]:
                        if re.search(rule[0 : rule.rindex(',')], entry['MESSAGE'], re.IGNORECASE):
                            db_insert_log(entry, rule.strip()[-1])

        j.wait()

    db.close() 