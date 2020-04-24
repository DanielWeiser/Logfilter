if __name__ == '__main__':

    import MySQLdb
    import config
    import time
    from datetime import datetime, timedelta

    db = MySQLdb.connect(config.mysql["host"], config.mysql["user"], config.mysql["password"], config.mysql["db"])
    cursor = db.cursor()
    
    while True:
        time_query = "delete from IDS_log where timestamp < '" + str(datetime.today() - timedelta(days = config.lifetime)) + "';"
        cursor.execute(time_query)
        db.commit()
        num_query = "delete from IDS_log WHERE id NOT IN (SELECT id from (SELECT id from IDS_log ORDER BY id DESC LIMIT " + str(config.max_logs) + ") foo);"
        cursor.execute(num_query)
        db.commit()
        time.sleep(5)

    db.close() 
    

