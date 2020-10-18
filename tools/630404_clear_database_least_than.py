from pymongo import MongoClient


def drop_except_in_list(except_db_list):
    client = MongoClient()
    except_db_global_list = ['admin', 'config', 'local']

    confirm = input("Enter: 'YES' (case sensitive) for process OR other to cancel\n")
    if confirm == 'YES':
        for db_name in client.database_names():
            cond = (db_name not in except_db_global_list) and (db_name not in except_db_list)
            if cond:
                client.drop_database(db_name)
                print(db_name, 'Deleted')
        print('______ Clean OK ______')
    else:
        print('Canceled')


if __name__ == '__main__':
    """
    This Tool made for drop all database except in list
    \\(> w <)/ Clean them all Woho!
    /!\\ WARNNING: Another your Database will delete
    """
    # except_db_list = ['fbta_20190619_0031', 'fbta_20190702_0058', 'fbta_20190824_1839', 'fbta_20190825_1941',
    #                   'fbta_20190828_1919', 'fbta_20190906_1220']
    # drop_except_in_list(except_db_list)
    client = MongoClient()
    except_db_global_list = ['admin', 'config', 'local']

    except_db_list = ['fbta_20200404_1328']

    for db_name in client.database_names():

        db = client.get_database(db_name)
        coll_card = db.get_collection('02_card_page')
        num_card = coll_card.estimated_document_count()

        stat_cond = num_card > 0
        cond = (db_name not in except_db_global_list) and (db_name not in except_db_list) and stat_cond
        if cond:
            confirm = input(
                f"Deleted? {num_card}) {db_name} Enter: 'YES' (case sensitive) for process OR other to cancel\n")
            if confirm == 'YES' or str(confirm).lower() == 'y':
                client.drop_database(db_name)
                print(f'({num_card}) {db_name} Deleted')
