#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on August 20 12:50 PM 2022
Created in PyCharm
Created as FitNotes_Database_Append/main.py

@author: Dylan Neff, Dylan
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta


def main():
    fit_notes_db_path = 'E:/Transfer/FitNotes_Backup.fitnotes'
    new_csv_path = 'E:/Transfer/FitNotes_Export_Dylan.csv'

    lbs_to_kg = 0.45359237  # kg per lb

    conn = sqlite3.connect(fit_notes_db_path)
    # print_db_test_info(conn)

    exercise_id_dict = get_exercise_id_dict(conn)

    db = pd.read_csv(new_csv_path, encoding='cp1252')
    # print_csv_test_info(db)

    for index, row in db.iterrows():
        log, comment = csv_row_to_sql_log(row, exercise_id_dict, lbs_to_kg)
        print(log, comment)
        row_id = create_training_log(conn, log)
        if not pd.isna(comment):
            comment_date = datetime.strftime(datetime.strptime(log[1], '%Y-%m-%d') + timedelta(hours=14),
                                             '%Y-%m-%d %H:%M:%S')
            print(comment_date, comment)
            create_comment(conn, (comment_date, 1, row_id, comment))

    print('donzo')


def print_db_test_info(conn):
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cur = conn.cursor()
    cur.execute(tables_query)
    print(cur.fetchall())

    cur.execute('Select * FROM exercise')
    print(next(zip(*cur.description)))
    rows = cur.fetchall()
    for row in rows[:10]:
        print(row)

    cur.execute('Select * FROM Comment')
    print(next(zip(*cur.description)))
    rows = cur.fetchall()
    for row in rows[:10]:
        print(row)

    cur.execute('Select * FROM training_log')
    print(next(zip(*cur.description)))
    rows = cur.fetchall()
    for row in rows[:10]:
        print(row)
        if row[5] != 2:
            print(f'unit row: {row}')
    print(rows[-1])
    print(rows[-1][0])


def print_csv_test_info(db):
    print(db)
    for index, row in db.iterrows():
        print(row['Weight (lbs)'])


def create_training_log(conn, log):
    """
    Create a new training log
    :param conn: Connection to sql database being appended to
    :param log: Tuple with training log info:
      ('exercise_id', 'date', 'metric_weight', 'reps', 'unit', 'routine_section_exercise_set_id',
      'timer_auto_start', 'is_personal_record', 'is_personal_record_first', 'is_complete', 'is_pending_update',
      'distance', 'duration_seconds')
    :return:
    """
    command = ''' INSERT INTO training_log(exercise_id,date,metric_weight,reps,unit,routine_section_exercise_set_id,
    timer_auto_start,is_personal_record,is_personal_record_first,is_complete,is_pending_update,distance,
    duration_seconds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(command, log)
    conn.commit()

    return cur.lastrowid


def create_comment(conn, comment):
    """
    Create a new training log
    :param conn: Connection to sql database being appended to
    :param comment: Tuple with training log info:
      ('date', 'owner_type_id', 'owner_id', 'comment')
    :return:
    """
    command = ''' INSERT INTO Comment(date,owner_type_id,owner_id,comment) VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(command, comment)
    conn.commit()

    return cur.lastrowid


def get_exercise_id_dict(conn):
    """
    Pull exercise table from database and construct a dictionary linking exercise names to ids.
    :param conn: Connection to sql database containing exercise table
    :return:
    """
    cur = conn.cursor()
    cur.execute('Select * FROM exercise')
    rows = cur.fetchall()
    exercise_name_ids = {row[1]: row[0] for row in rows}

    return exercise_name_ids


def csv_row_to_sql_log(row, exercise_id_dict, lbs_to_kg):
    extra_log_vals = [2, 0, 0, 0, 0, 0, 0, 0, 0]
    try:
        exercise_id = exercise_id_dict[row['Exercise']]
    except KeyError:
        print(row['Exercise'], ' not found')
        exercise_id = -1
    weight = row['Weight (lbs)'] * lbs_to_kg
    weight = 0 if pd.isna(weight) else weight
    reps = row['Reps']
    date = datetime.strftime(datetime.strptime(row['Date'], '%m/%d/%Y'), '%Y-%m-%d')
    comment = row['Comment']

    return (exercise_id, date, weight, reps, *extra_log_vals), comment


if __name__ == '__main__':
    main()
