import happybase


def create_table():
    connection = happybase.Connection('210.102.142.14')
    # dict_families = {'sp_ird': dict()}
    dict_families = {'measurement_conditions': dict(),
                     'results': dict(),
                     'general_information': dict(),
                     'sp_ird': dict(),
                     'uv': dict()}

    connection.create_table('natural_light', dict_families)

    table = connection.table('natural_light')
    print(connection.tables())
    connection.close()


if __name__ == "__main__":
    create_table()
