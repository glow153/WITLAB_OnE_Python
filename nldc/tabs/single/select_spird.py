def getSpectra(date: str):
    import happybase
    connection = happybase.Connection('210.102.142.14')
    print(connection.tables())
    table = connection.table('natural_light')
    return table.row(date, ['sp_ird'])

# if __name__ == '__main__':
#     date = '2017-04-13'
#     time = '1000'
#     print(getSpectra(date + ' ' + time))
