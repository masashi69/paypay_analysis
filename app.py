import sys
import sqlite3
import datetime


def subDateisoformat(d):
    df = datetime.datetime.strptime(d, '%Y/%m/%d')
    sub_y, sub_m, sub_d = df.year, df.month, df.day

    return datetime.date(sub_y, sub_m, sub_d).isoformat()


def main():
    # Delete BOM in file
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as f:
        csvfile = f.readlines()

    con = sqlite3.connect(':memory:')
    cur = con.cursor()

    for n, c in enumerate(csvfile):
        field = c.split(',')
        if n == 0:
            headers = (field[0], field[1], field[6])
            # Create sql statement becouse can't used qmark style
            headers = f'CREATE TABLE pay ({field[0]} TEXT,{field[1]} TEXT, \
                       {field[6]} TEXT)'
            cur.execute(headers)
        else:
            # Delete double quotes
            field[0] = field[0].replace("\"","")
            field[1] = field[1].replace("\"","")
            field[6] = field[6].replace("\"","")

            field[0] = subDateisoformat(field[0])
            insert_row = (field[0], field[1], field[6])
            cur.execute('INSERT INTO pay VALUES (?,?,?)', insert_row)

    cur.execute('SELECT "利用日/キャンセル日", "利用店名・商品名", sum("支払総額"), \
                 count("利用店名・商品名") FROM pay GROUP BY "利用日/キャンセル日", \
                 "利用店名・商品名" ORDER BY "利用日/キャンセル日"')

    for x in cur.fetchall():
        print(*x)

    cur.execute('SELECT sum("支払総額") FROM pay')
    # Use 'format' for use astarisk
    print('Total: {}'.format(*cur.fetchone()))

    con.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Be specify csvfile.')
        sys.exit(1)

    main()

