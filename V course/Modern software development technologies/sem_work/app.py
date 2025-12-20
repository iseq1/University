import random
import sqlite3
import datetime as dt
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash
import hashlib
import os
from dbpush import DataPusher

app = Flask(__name__)
app.secret_key = 'your_secret_key'

months_rus = {
    '01': 'Январь',
    '02': 'Февраль',
    '03': 'Март',
    '04': 'Апрель',
    '05': 'Май',
    '06': 'Июнь',
    '07': 'Июль',
    '08': 'Август',
    '09': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь'
}

# Путь для сохранения изображений
path_to_save_images = os.path.join(app.root_path, 'static', 'imgs')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/bartenders')
def bartenders():
    return render_template('bartenders.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def This_week_dates(day=None):
    today = dt.date.today()
    # Находим начало текущей недели
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)
    dates_of_week = []
    for i in range(7):
        dates_of_week.append(start_of_week + dt.timedelta(days=i))

    if day:
        if day == 'Monday':
            return dates_of_week[0].strftime('%d/%m/%Y')
        elif day == 'Tuesday':
            return dates_of_week[1].strftime('%d/%m/%Y')
        elif day == 'Wednesday':
            return dates_of_week[2].strftime('%d/%m/%Y')
        elif day == 'Thursday':
            return dates_of_week[3].strftime('%d/%m/%Y')
        elif day == 'Friday':
            return dates_of_week[4].strftime('%d/%m/%Y')
        elif day == 'Saturday':
            return dates_of_week[5].strftime('%d/%m/%Y')
        elif day == 'Sunday':
            return dates_of_week[6].strftime('%d/%m/%Y')

    return [date.strftime('%d/%m/%Y') for date in dates_of_week]

def Previous_week_dates(day=None):
    today = dt.date.today()
    # Находим начало текущей недели
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)
    # Находим начало и конец предыдущей недели
    start_of_last_week = start_of_week - dt.timedelta(days=7)
    end_of_last_week = start_of_last_week + dt.timedelta(days=6)
    dates_of_last_week = []
    for i in range(7):
        dates_of_last_week.append(start_of_last_week + dt.timedelta(days=i))
    if day:
        if day == 'Monday':
            return dates_of_last_week[0].strftime('%d/%m/%Y')
        elif day == 'Tuesday':
            return dates_of_last_week[1].strftime('%d/%m/%Y')
        elif day == 'Wednesday':
            return dates_of_last_week[2].strftime('%d/%m/%Y')
        elif day == 'Thursday':
            return dates_of_last_week[3].strftime('%d/%m/%Y')
        elif day == 'Friday':
            return dates_of_last_week[4].strftime('%d/%m/%Y')
        elif day == 'Saturday':
            return dates_of_last_week[5].strftime('%d/%m/%Y')
        elif day == 'Sunday':
            return dates_of_last_week[6].strftime('%d/%m/%Y')

    return [date.strftime('%d/%m/%Y') for date in dates_of_last_week]

def Next_week_dates(day=None):
    today = dt.date.today()
    # Находим начало текущей недели
    start_of_week = today - dt.timedelta(days=today.weekday())
    end_of_week = start_of_week + dt.timedelta(days=6)
    # Находим начало и конец следующей недели
    start_of_next_week = end_of_week + dt.timedelta(days=1)
    end_of_next_week = start_of_next_week + dt.timedelta(days=6)
    dates_of_next_week = []
    for i in range(7):
        dates_of_next_week.append(start_of_next_week + dt.timedelta(days=i))
    if day:
        if day == 'Monday':
            return dates_of_next_week[0].strftime('%d/%m/%Y')
        elif day == 'Tuesday':
            return dates_of_next_week[1].strftime('%d/%m/%Y')
        elif day == 'Wednesday':
            return dates_of_next_week[2].strftime('%d/%m/%Y')
        elif day == 'Thursday':
            return dates_of_next_week[3].strftime('%d/%m/%Y')
        elif day == 'Friday':
            return dates_of_next_week[4].strftime('%d/%m/%Y')
        elif day == 'Saturday':
            return dates_of_next_week[5].strftime('%d/%m/%Y')
        elif day == 'Sunday':
            return dates_of_next_week[6].strftime('%d/%m/%Y')

    return [date.strftime('%d/%m/%Y') for date in dates_of_next_week]

@app.route('/basket')
def basket():
    if session['basket']:
        try:
            block_lt = []
            conn = get_db_connection()
            for item in session['basket']:
                new_item = translate(item)
                blocks = conn.execute(f'SELECT * FROM menu WHERE name="{new_item}"').fetchall()
                block_lt.extend(blocks)  # Добавляем результаты запроса к списку
            conn.close()
            # Преобразование данных из БД в список словарей
            blocks_list = [dict(ix) for ix in block_lt]
            # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]
            # Теперь нужно сделать группировку списка в один словарь json
            # Группировка данных в словарь JSON
            json_data = {}
            for raw in blocks_list:
                # Создание новой записи, если ключ еще не существует
                if 'basket-list' not in json_data:
                    json_data['basket-list'] = []
                # Добавление данных в существующий ключ
                json_data['basket-list'].append({
                    'id': raw['id'],
                    'name': raw['name'],
                    'price': raw['price'],
                    'photo_path': raw['photo_path']
                })
            print(json_data)
            return render_template('basket.html', json_data=json_data)
        except Exception as e:
            print("Ошибка:", e)
    else:
        return redirect('/coffee-menu')
def Does_he_work_st(id, date):
    conn=get_db_connection()
    time_info = conn.execute(f'''
        SELECT start_time
        FROM schedule 
        WHERE barista_id = "{id}" AND date LIKE "{date}"
    ''').fetchall()
    conn.close()
    if time_info:
        return time_info[0][0]
    return '00:00'
def Does_he_work_ft(id, date):
    conn=get_db_connection()
    time_info = conn.execute(f'''
        SELECT finish_time
        FROM schedule 
        WHERE barista_id = "{id}" AND date LIKE "{date}"
    ''').fetchall()
    conn.close()
    if time_info:
        return time_info[0][0]
    return '00:00'
def time_difference(start_time, end_time):
    # Разбиваем время на часы и минуты
    start_hours, start_minutes = map(int, start_time.split(':'))
    end_hours, end_minutes = map(int, end_time.split(':'))
    # Преобразуем время в минуты
    start_total_minutes = start_hours * 60 + start_minutes
    end_total_minutes = end_hours * 60 + end_minutes
    # Вычисляем разницу
    difference_minutes = end_total_minutes - start_total_minutes
    # Преобразуем обратно в часы и минуты
    difference_hours, difference_minutes = divmod(difference_minutes, 60)
    return difference_hours, difference_minutes

@app.route('/admin-panel', methods=['GET', 'POST'])
def adminpage():
    conn = get_db_connection()
    barista_info = conn.execute(f'''
        SElECT barista.id, barista.name
        FROM barista
    ''').fetchall()
    total_orders_per_day = conn.execute(f'''
                    SELECT COUNT(orders.id)
                    FROM orders
                    WHERE orders.order_date LIKE "%{datetime.now().strftime('%d/%m/%Y')}"
                ''').fetchall()
    total_orders_per_month = conn.execute(f'''
                    SELECT COUNT(orders.id)
                    FROM orders
                    WHERE orders.order_date LIKE "%{datetime.now().strftime('%m/%Y')}"
                ''').fetchall()
    total_revenue_per_day = conn.execute(f'''
                    SELECT SUM(menu.price) as revenue
                    FROM orders
                    JOIN orders_has_order ON orders.id = orders_has_order.orders_id
                    JOIN personal_order ON orders_has_order.order_id = personal_order.id
                    JOIN menu ON menu.id = personal_order.menu_id
                    WHERE orders.order_date LIKE "%{datetime.now().strftime('%d/%m/%Y')}"
                ''').fetchall()
    total_revenue_per_month = conn.execute(f'''
                        SELECT SUM(menu.price) as revenue
                        FROM orders
                        JOIN orders_has_order ON orders.id = orders_has_order.orders_id
                        JOIN personal_order ON orders_has_order.order_id = personal_order.id
                        JOIN menu ON menu.id = personal_order.menu_id
                        WHERE orders.order_date LIKE "%{datetime.now().strftime('%m/%Y')}"
                    ''').fetchall()
    average_stars_per_day = conn.execute(f'''
                        SELECT SUM(orders.stars) as stars_sum, COUNT(orders.stars) as stars_count
                        FROM orders
                        WHERE orders.order_date LIKE "%{datetime.now().strftime('%d/%m/%Y')}"
                    ''').fetchall()
    average_stars_per_month = conn.execute(f'''
                        SELECT SUM(orders.stars) as stars_sum, COUNT(orders.stars) as stars_count
                        FROM orders
                        WHERE orders.order_date LIKE "%{datetime.now().strftime('%m/%Y')}"
                    ''').fetchall()
    if barista_info:
        barista_list = [dict(ix) for ix in list(barista_info)]
    else:
        barista_list = []
    json_data = {}
    pwi = Previous_week_dates()
    previous_week_info = conn.execute(f'''
        SELECT barista_id, date, start_time, finish_time, work_time
        FROM schedule 
        WHERE date IN ("{pwi[0]}", "{pwi[1]}", "{pwi[2]}", "{pwi[3]}", "{pwi[4]}", "{pwi[5]}", "{pwi[6]}")
    ''').fetchall()
    if 'admin_name' not in json_data:
        json_data['admin_name'] = []
    json_data['admin_name'].append({
        'name': conn.execute(f'''
                        SELECT name
                        FROM admin
                        WHERE admin_login = "{session['username']}"
                    ''').fetchall()[0][0]
    })
    if total_orders_per_month:
        total_orders_per_month_list = [dict(ix) for ix in list(total_orders_per_month)]
    else:
        total_orders_per_month_list = []
    for _ in total_orders_per_month_list:
        if 'casual-orders-info' not in json_data:
            json_data['casual-orders-info'] = []
        sb_info = {
            'date': f"{datetime.now().strftime('%d/%m/%Y')}",
            'month': f"{ months_rus.get(datetime.now().strftime('%m')) }",
            'total_orders_per_day': total_orders_per_day[0][0] if total_orders_per_day[0][0] is not None else 0,
            'total_orders_per_month': total_orders_per_month[0][0] if total_orders_per_month[0][0] is not None else 0,
            'total_revenue_per_day': round(total_revenue_per_day[0][0], 2) if total_revenue_per_day[0][0] is not None else 0,
            'total_revenue_per_month': round(total_revenue_per_month[0][0], 2) if total_revenue_per_month[0][0] is not None else 0,
            'average_stars_per_day': round(average_stars_per_day[0][0]/average_stars_per_day[0][1], 2) if average_stars_per_day[0][0] is not None else 0,
            'average_stars_per_month': round(average_stars_per_month[0][0]/average_stars_per_month[0][1], 2) if average_stars_per_month[0][0] is not None else 0
        }
        json_data['casual-orders-info'].append(sb_info)
    if request.method == 'POST' and 'timeframe' in request.form and 'barista' in request.form:
        selected_timeframe = request.form.get('timeframe')
        selected_barista = request.form.get('barista')
        if selected_barista != 0 and selected_timeframe != 0:
            print('суета пошла')
            conn = get_db_connection()
            barista_orders_info = conn.execute(
                f'''
                    SELECT orders.id, orders.order_date, orders.stars, User.fullname,
                           GROUP_CONCAT(menu.name) AS names, GROUP_CONCAT(personal_order.size) AS sizes, GROUP_CONCAT(menu.price) as prices
                    FROM orders
                    JOIN barista ON orders.barista_id = barista.id
                    JOIN User ON orders.user_id = User.login
                    JOIN orders_has_order ON orders.id = orders_has_order.orders_id
                    JOIN personal_order ON orders_has_order.order_id = personal_order.id
                    JOIN menu ON menu.id = personal_order.menu_id
                    WHERE barista.id = "{selected_barista}" AND orders.order_date LIKE "%{eval(selected_timeframe)}"
                    GROUP BY orders.id
                    ORDER BY orders.id 
                ''').fetchall()
            selected_barista_info = conn.execute(f'''
                    SElECT barista.name, barista.work_time
                    FROM barista
                    WHERE barista.id = "{selected_barista}"
                ''').fetchall()
            if selected_barista_info:
                selected_barista_list = [dict(ix) for ix in list(selected_barista_info)]
            else:
                selected_barista_list = []
            for raw in selected_barista_list:
                if 'selected-barista-info' not in json_data:
                    json_data['selected-barista-info'] = []
                sb_info = {
                    'name': raw['name'],
                    'work_time': raw['work_time'],
                }
                json_data['selected-barista-info'].append(sb_info)
            for raw in barista_orders_info:
                if 'barista-order-info' not in json_data:
                    json_data['barista-order-info'] = []
                order_info = {
                    'ID': raw['id'],
                    'names': reformate_from_db_to_page(raw['names']),
                    'sizes': raw['sizes'],
                    'date': raw['order_date'],
                    'stars': raw['stars'],
                    'client': raw['fullname'],
                    'kpi': round(sum([float(price) for price in raw['prices'].split(',')]) * 0.025, 2)
                }
                json_data['barista-order-info'].append(order_info)
        else:
            flash('Пожалуйста, укажите все параметры.')
    # Расписание на текущую неделю
    if request.method == 'POST' and 'timeStart_Monday' in request.form and 'timeEnd_Monday' in request.form:
        start_time = request.form.get('timeStart_Monday')
        end_time = request.form.get('timeEnd_Monday')
        addition_info = request.form.get('start_id').split('_')
        if start_time and end_time:
            date = This_week_dates(addition_info[3])
            h, m = time_difference(start_time, end_time)
            with DataPusher('database.db') as changer:
                if not changer.select_data(table='schedule',  barista_id=f'{addition_info[1]}', date=f'{date}', start_time=f'{start_time}', finish_time=f'{end_time}'):
                    if m >=45:
                        changer.insert_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}', start_time=f'{start_time}', finish_time=f'{end_time}', work_time=(h+1))
                    else:
                        changer.insert_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}', start_time=f'{start_time}', finish_time=f'{end_time}', work_time=h)
    if request.method == 'POST' and 'TimeStart_Done' in request.form and 'TimeEnd_Done' in request.form:
        start_time = request.form.get('TimeStart_Done')
        end_time = request.form.get('TimeEnd_Done')
        addition_info = request.form.get('start_id_done').split('_')
        date = This_week_dates(addition_info[3])
        with DataPusher('database.db') as changer:
            if changer.select_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',start_time=f'{start_time}', finish_time=f'{end_time}'):
                barista_id = changer.select_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',start_time=f'{start_time}', finish_time=f'{end_time}')[0][0]
                changer.delete_data(table='schedule', ID=barista_id)
    # Расписание на следующую неделю
    if request.method == 'POST' and 'timeStartNextWeek_Monday' in request.form and 'timeEndNextWeek_Monday' in request.form:
        start_time = request.form.get('timeStartNextWeek_Monday')
        end_time = request.form.get('timeEndNextWeek_Monday')
        addition_info = request.form.get('start_id_nextweek').split('_')
        if start_time and end_time:
            date = Next_week_dates(addition_info[3])
            h, m = time_difference(start_time, end_time)
            with DataPusher('database.db') as changer:
                if not changer.select_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',
                                           start_time=f'{start_time}', finish_time=f'{end_time}'):
                    if m >= 45:
                        changer.insert_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',
                                            start_time=f'{start_time}', finish_time=f'{end_time}', work_time=(h + 1))
                    else:
                        changer.insert_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',
                                            start_time=f'{start_time}', finish_time=f'{end_time}', work_time=h)
    if request.method == 'POST' and 'TimeStartNextWeek_Done' in request.form and 'TimeEndNextWeek_Done' in request.form:
        start_time = request.form.get('TimeStartNextWeek_Done')
        end_time = request.form.get('TimeEndNextWeek_Done')
        addition_info = request.form.get('start_id_done_nextweek').split('_')
        date = Next_week_dates(addition_info[3])
        with DataPusher('database.db') as changer:
            if changer.select_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',
                                   start_time=f'{start_time}', finish_time=f'{end_time}'):
                barista_id = changer.select_data(table='schedule', barista_id=f'{addition_info[1]}', date=f'{date}',
                                                 start_time=f'{start_time}', finish_time=f'{end_time}')[0][0]
                changer.delete_data(table='schedule', ID=barista_id)
    if 'dates_of_week' not in json_data:
        json_data['dates_of_week'] = []
    this_week = This_week_dates()
    previous_week = Previous_week_dates()
    next_week = Next_week_dates()
    for raw in barista_list:
        if 'barista-list' not in json_data:
            json_data['barista-list'] = []
        json_data['barista-list'].append({
            'id': raw['id'],
            'name': raw['name'],
            'last_week': {
                'Monday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[0]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[0]),
                },
                'Tuesday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[1]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[1]),
                },
                'Wednesday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[2]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[2]),
                },
                'Thursday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[3]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[3]),
                },
                'Friday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[4]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[4]),
                },
                'Saturday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[5]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[5]),
                },
                'Sunday': {
                    'start_time': Does_he_work_st(raw['id'], previous_week[6]),
                    'finish_time': Does_he_work_ft(raw['id'], previous_week[6]),
                }
            },
            'current_week': {
                'Monday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[0]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[0]),
                },
                'Tuesday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[1]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[1]),
                },
                'Wednesday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[2]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[2]),
                },
                'Thursday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[3]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[3]),
                },
                'Friday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[4]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[4]),
                },
                'Saturday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[5]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[5]),
                },
                'Sunday': {
                    'start_time': Does_he_work_st(raw['id'], this_week[6]),
                    'finish_time': Does_he_work_ft(raw['id'], this_week[6]),
                }
            },
            'next_week': {
                'Monday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[0]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[0]),
                },
                'Tuesday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[1]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[1]),
                },
                'Wednesday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[2]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[2]),
                },
                'Thursday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[3]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[3]),
                },
                'Friday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[4]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[4]),
                },
                'Saturday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[5]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[5]),
                },
                'Sunday': {
                    'start_time': Does_he_work_st(raw['id'], next_week[6]),
                    'finish_time': Does_he_work_ft(raw['id'], next_week[6]),
                }
            }
        })
    json_data['dates_of_week'].append({
        'Monday': this_week[0],
        'Tuesday': this_week[1],
        'Wednesday': this_week[2],
        'Thursday': this_week[3],
        'Friday': this_week[4],
        'Saturday': this_week[5],
        'Sunday': this_week[6]
    })
    if 'dates_of_previous_week' not in json_data:
        json_data['dates_of_previous_week'] = []
    json_data['dates_of_previous_week'].append({
        'Monday': previous_week[0],
        'Tuesday': previous_week[1],
        'Wednesday': previous_week[2],
        'Thursday': previous_week[3],
        'Friday': previous_week[4],
        'Saturday': previous_week[5],
        'Sunday': previous_week[6]
    })
    if 'dates_of_next_week' not in json_data:
        json_data['dates_of_next_week'] = []
    json_data['dates_of_next_week'].append({
        'Monday': next_week[0],
        'Tuesday': next_week[1],
        'Wednesday': next_week[2],
        'Thursday': next_week[3],
        'Friday': next_week[4],
        'Saturday': next_week[5],
        'Sunday': next_week[6]
    })
    conn.close()
    print(json_data)
    return render_template('admin_panel.html', json_data=json_data)

@app.route('/barista-panel')
def baristapage():
    print(session)
    conn = get_db_connection()
    barista_info = conn.execute(f'SELECT * FROM barista WHERE barista_login="{session["username"]}"').fetchall()
    barista_orders_info = conn.execute(
        f'''
        SELECT orders.id, orders.order_date, orders.stars, User.fullname,
               GROUP_CONCAT(menu.name) AS names, GROUP_CONCAT(personal_order.size) AS sizes, GROUP_CONCAT(menu.price) as prices
        FROM orders
        JOIN barista ON orders.barista_id = barista.id
        JOIN User ON orders.user_id = User.login
        JOIN orders_has_order ON orders.id = orders_has_order.orders_id
        JOIN personal_order ON orders_has_order.order_id = personal_order.id
        JOIN menu ON menu.id = personal_order.menu_id
        WHERE barista.barista_login = "{session["username"]}" AND orders.order_date LIKE "%{datetime.now().strftime('%d/%m/%Y')}"
        GROUP BY orders.id
        ORDER BY orders.id DESC
    ''').fetchall()
    today_orders_count = conn.execute(
        f'''
        SELECT COUNT(orders.id) as order_count
        FROM orders
        JOIN barista ON orders.barista_id = barista.id
        WHERE order_date LIKE "%{ datetime.now().strftime('%d/%m/%Y') }" AND barista.barista_login = "{session["username"]}"
    ''').fetchall()
    today_stars_info = conn.execute(
        f'''
            SELECT COUNT(orders.stars) as stars_count, AVG(orders.stars)
            FROM orders
            JOIN barista ON orders.barista_id = barista.id
            WHERE order_date LIKE "%{datetime.now().strftime('%d/%m/%Y')}" AND barista.barista_login = "{session["username"]}" AND orders.stars != "None"
        ''').fetchall()
    dates = This_week_dates()
    schedule_on_week = conn.execute(f'''
            SELECT schedule.date, schedule.start_time, schedule.finish_time
            FROM schedule
            JOIN barista ON schedule.barista_id = barista.id
            WHERE barista.barista_login = "{session["username"]}" AND ( schedule.date = "{dates[0]}" OR schedule.date = "{dates[1]}" OR schedule.date = "{dates[2]}" OR schedule.date = "{dates[3]}" OR schedule.date = "{dates[4]}" OR schedule.date = "{dates[5]}" OR schedule.date = "{dates[6]}")
        ''').fetchall()
    conn.close()
    if barista_info:
        barista_list = [dict(ix) for ix in list(barista_info)]
    else:
        barista_list = []
    if barista_orders_info:
        barista_orders_list = [dict(ix) for ix in list(barista_orders_info)]
    else:
        barista_orders_list = []
    if schedule_on_week:
        schedule_on_week_list = [dict(ix) for ix in list(schedule_on_week)]
    else:
        schedule_on_week_list = []
    json_data = {}
    for raw in barista_list:
        if raw['id'] not in json_data:
            json_data[raw['id']] = []
        json_data[raw['id']].append({
            'name': raw['name'],
            'orders_count': today_orders_count[0][0] if today_orders_count[0][0] is not None else 0,
            'stars_count': today_stars_info[0][0] if today_stars_info[0][0] is not None else 0,
            'average_stars': today_stars_info[0][1] if today_stars_info[0][1] is not None else 0,
        })
    if len(barista_orders_info)>0:
        for raw in barista_orders_info:
            if barista_info[0][1] not in json_data:
                json_data[barista_info[0][1]] = []
            order_info = {
                'ID': raw['id'],
                'names': reformate_from_db_to_page(raw['names']),
                'sizes': raw['sizes'],
                'date': raw['order_date'],
                'stars': raw['stars'],
                'client': raw['fullname'],
                'kpi': round(sum([float(price) for price in raw['prices'].split(',')]) * 0.025, 2)
            }
            json_data[barista_info[0][1]].append(order_info)
    else:
        if barista_info[0][1] not in json_data:
            json_data[barista_info[0][1]] = []
        order_info = {
            'ID': ' ',
            'names': ' ',
            'sizes': ' ',
            'date': ' ',
            'stars': ' ',
            'client': ' ',
            'kpi': ' '
        }
        json_data[barista_info[0][1]].append(order_info)
    if 'week' not in json_data:
        json_data['week'] = []
    this_week=This_week_dates()
    week_info = {
        'Monday': this_week[0],
        'Tuesday': this_week[1],
        'Wednesday': this_week[2],
        'Thursday': this_week[3],
        'Friday': this_week[4],
        'Saturday': this_week[5],
        'Sunday': this_week[6]
    }
    json_data['week'].append(week_info)
    for raw in schedule_on_week_list:
        if 'schedule' not in json_data:
            json_data['schedule'] = []
        json_data['schedule'].append({
            raw['date']: {
                'start_time': raw['start_time'],
                'finish_time': raw['finish_time']
            },
        })
    print(json_data)
    return render_template('barista_panel.html', json_data = json_data)

@app.route('/profile')
def profilepage():
    print(session)
    session['basket'] = []
    conn = get_db_connection()
    user_info = conn.execute(
        f'SELECT * FROM User WHERE login="{session["username"]}"').fetchall()
    order_count_info = conn.execute(f'''
            SELECT COUNT(order_id) as dishes_count, COUNT(DISTINCT orders_id) as order_count
            FROM orders_has_order 
            JOIN (
                SELECT id
                FROM orders
                WHERE User_id="{session["username"]}"
                ORDER BY id DESC
                LIMIT 3
            ) AS recent_orders ON orders_has_order.orders_id = recent_orders.id
            ''').fetchall()
    orders_info = conn.execute(
        f'''SELECT orders.id, orders.order_date, orders.stars, menu.name, menu.price
        FROM orders
        JOIN orders_has_order ON orders.id = orders_has_order.orders_id
        JOIN personal_order ON orders_has_order.order_id = personal_order.id
        JOIN menu ON menu.id = personal_order.menu_id
        WHERE orders.User_id = "{session["username"]}"
        ORDER BY orders.id DESC LIMIT {order_count_info[0][0]}'''
    ).fetchall()
    unique_coffee_count = conn.execute(
        f'''SELECT COUNT(DISTINCT menu.name) AS unique_coffee_count
            FROM orders
            JOIN orders_has_order ON orders.id = orders_has_order.orders_id
            JOIN personal_order ON orders_has_order.order_id = personal_order.id
            JOIN menu ON menu.id = personal_order.menu_id
            WHERE orders.User_id = "{session["username"]}"'''
    ).fetchall()
    conn.close()
    if user_info:  # Проверяем, что кортеж не пустой
        blocks_list = [dict(ix) for ix in list(user_info)]  # Преобразуем кортеж в список
    else:
        blocks_list = []  # Если кортеж пустой, создаем пустой список
    if orders_info:  # Проверяем, что кортеж не пустой
        orders_list = [dict(ix) for ix in list(orders_info)]  # Преобразуем кортеж в список
    else:
        orders_list = []  # Если кортеж пустой, создаем пустой список
    # Группировка данных в словарь JSON
    json_data = {}
    for raw in blocks_list:
        if raw['login'] not in json_data:
            json_data[raw['login']] = []
        json_data[raw['login']].append({
            'fullname': raw['fullname'],
            'email': raw['email'],
            'number': raw['number'],
            'rang': raw['rang'],
            'order_count': raw['order_count'],
            'average_points': raw['average_points'],
            'unique_coffee_count': unique_coffee_count[0][0]
        })
    for raw in orders_list:
        if raw['id'] not in json_data:
            json_data[raw['id']] = []
        json_data[raw['id']].append({
            'ID': raw['id'],
            'date': raw['order_date'],
            'stars': raw['stars'],
            'name': reformate_from_db_to_page(raw['name']),
            'price': raw['price']
        })
    print(json_data)
    return render_template('profile.html', json_data=json_data)

@app.route('/faq')
def faqpage():
    return render_template('faq.html')

@app.route('/specials')
def specialpage():
    return render_template('specials.html')

@app.route('/specials/<specials_count>')
def specialpages(specials_count):
    if specials_count == 'specials-1':
        return render_template('specials-1.html')
    if specials_count == 'specials-2':
        return render_template('specials-2.html')
    if specials_count == 'specials-3':
        return render_template('specials-3.html')

@app.route('/terms-of-service')
def Terms_of_Service():
    return render_template('terms-of-service.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/coffee-menu')
def MenuPage():
    conn = get_db_connection()
    types = conn.execute('''
        SELECT DISTINCT type
        FROM menu
    ''').fetchall()
    menu_list = {}
    for type_name in types:
        menu_list[type_name[0]] = conn.execute(f'''
            SELECT name, photo_path
            FROM menu
            WHERE type = "{type_name[0]}"
        ''').fetchall()
    conn.close()
    json_data = {}
    json_data['coffee-menu-list'] = []
    for type_name, menu_items in menu_list.items():
        menu_data = []
        for item in menu_items:
            menu_data.append({
                'name': item[0],
                'photo_path': item[1]
            })
        json_data['coffee-menu-list'].append({
            type_name: menu_data
        })
    print(json_data)
    return render_template('coffee-menu.html', json_data=json_data)

def translate(drink_name):
    drink_dict = {
        'cappuccino-banana-sponge-cake-with-strawberries': 'Капучино Банановый бисквит с клубникой',
        'Капучино Банановый бисквит с клубникой': 'cappuccino-banana-sponge-cake-with-strawberries',
        'mochaccino-orange-brownie': 'Мокачино Апельсиновый брауни',
        'Мокачино Апельсиновый брауни': 'mochaccino-orange-brownie',
        'sea-buckthorn-tea-with-orange-and-ginger': 'Чай облепиха с апельсином и имбирем',
        'Чай облепиха с апельсином и имбирем': 'sea-buckthorn-tea-with-orange-and-ginger',
        'raspberry-tea-with-cranberry-and-barberry': 'Чай малина с клюквой и барбарисом',
        'Чай малина с клюквой и барбарисом': 'raspberry-tea-with-cranberry-and-barberry',
        'mango-tea-with-jasmine-and-kaffir-lime': 'Чай манго с жасмином и каффир-лаймом',
        'Чай манго с жасмином и каффир-лаймом': 'mango-tea-with-jasmine-and-kaffir-lime',
        'raf-raspberry-coconut': 'Раф Малина кокос',
        'Раф Малина кокос': 'raf-raspberry-coconut',
        'latte-banana-ice-cream-with-salted-caramel': 'Латте Банановое мороженое с соленой карамелью',
        'Латте Банановое мороженое с соленой карамелью': 'latte-banana-ice-cream-with-salted-caramel',
        'raf-birds-milk': 'Раф Птичье молоко',
        'Раф Птичье молоко': 'raf-birds-milk',
        'cappuccino-croissant-with-maple-syrup-and-walnuts': 'Капучино Круассан с кленовым сиропом и грецким орехом',
        'Капучино Круассан с кленовым сиропом и грецким орехом': 'cappuccino-croissant-with-maple-syrup-and-walnuts',
        'raf': 'Раф',
        'Раф': 'raf',
        'latte': 'Латте',
        'Латте': 'latte',
        'cappuccino': 'Капучино',
        'Капучино': 'cappuccino',
        'americano': 'Американо',
        'Американо': 'americano',
        'flat-white': 'Флэт Уайт',
        'Флэт Уайт': 'flat-white',
        'hot-chocolate': 'Горячий шоколад',
        'Горячий шоколад': 'hot-chocolate',
        'cocoa': 'Какао',
        'Какао': 'cocoa',
        'espresso': 'Эспрессо',
        'Эспрессо': 'espresso',
        'ice-latte': 'Айс Латте',
        'Айс Латте': 'ice-latte',
        'ice-raf': 'Айс Раф',
        'Айс Раф': 'ice-raf',
        'ice-cappuccino': 'Айс Капучино',
        'Айс Капучино': 'ice-cappuccino',
        'ice-cocoa': 'Айс Какао',
        'Айс Какао': 'ice-cocoa',
        'ice-cappuccino-banana-sponge-cake-with-strawberries': 'Айс Капучино Банановый бисквит с клубникой',
        'Айс Капучино Банановый бисквит с клубникой': 'ice-cappuccino-banana-sponge-cake-with-strawberries',
        'latte-coconut-mango-ice-cream': 'Латте Кокосовый пломбир с манго',
        'Латте Кокосовый пломбир с манго': 'latte-coconut-mango-ice-cream',
        'ice-latte-coconut-ice-cream-with-mango': 'Айс Латте Кокосовый пломбир с манго',
        'Айс Латте Кокосовый пломбир с манго': 'ice-latte-coconut-ice-cream-with-mango',
        'raf-rice-pudding-with-papaya': 'Раф Рисовый пудинг с папайей',
        'Раф Рисовый пудинг с папайей': 'raf-rice-pudding-with-papaya',
        'ice-rough-rice-pudding-with-papaya': 'Айс Раф Рисовый пудинг с папайей',
        'Айс Раф Рисовый пудинг с папайей': 'ice-rough-rice-pudding-with-papaya',
        'lemonade-with-watermelon-pineapple-and-Rose': 'Лимонад с Арбузом, ананасом и розой',
        'Лимонад с Арбузом, ананасом и розой': 'lemonade-with-watermelon-pineapple-and-Rose',
        'coffee-tonic-with-watermelon-pineapple-and-rose': 'Кофейный тоник с Арбузом, ананасом и розой',
        'Кофейный тоник с Арбузом, ананасом и розой': 'coffee-tonic-with-watermelon-pineapple-and-rose',
        'lemonade-with-peach-passion-fruit-and-orange-blossom': 'Лимонад с Персиком, маракуйей и цветами апельсина',
        'Лимонад с Персиком, маракуйей и цветами апельсина': 'lemonade-with-peach-passion-fruit-and-orange-blossom',
        'coffee-tonic-with-peach-passion-fruit-and-orange-blossom': 'Кофейный тоник с Персиком, маракуйей и цветами апельсина',
        'Кофейный тоник с Персиком, маракуйей и цветами апельсина': 'coffee-tonic-with-peach-passion-fruit-and-orange-blossom',
        'lemonade-with-grapes-aloe-and-lavender': 'Лимонад с Виноградом, алоэ и лавандой',
        'Лимонад с Виноградом, алоэ и лавандой': 'lemonade-with-grapes-aloe-and-lavender',
        'coffee-tonic-with-grapes-aloe-and-lavender': 'Кофейный тоник с Виноградом, алоэ и лавандой',
        'Кофейный тоник с Виноградом, алоэ и лавандой': 'coffee-tonic-with-grapes-aloe-and-lavender'
    }
    return drink_dict[drink_name]

@app.route('/coffee-menu/<drink_name>')
def drink_page(drink_name):
    print(session)
    translated_name = translate(drink_name)
    conn = get_db_connection()
    drink_info = conn.execute(f'SELECT * FROM menu WHERE name="{translated_name}"').fetchall()
    drink_size_info = conn.execute(f'SELECT size, kcal, protein, fat, carbohydrate FROM menu_size_info WHERE menu_id="{drink_info[0][0]}"').fetchall()
    drink_description_info = conn.execute(f'SELECT ingredient FROM menu_description_info WHERE menu_id="{drink_info[0][0]}"').fetchall()
    conn.close()
    json_data = {}
    if 'drink-page' not in json_data:
        json_data['drink-page'] = []
    size_data = {
        'mid-size': {
            'size': drink_size_info[0][0],
            'kcal': int(drink_size_info[0][1]),
            'protein': int(drink_size_info[0][2]),
            'fat': int(drink_size_info[0][3]),
            'carbohydrate': int(drink_size_info[0][4])
        }
    }
    if len(drink_size_info) > 1:
        size_data['small-size'] = {
            'size': drink_size_info[1][0],
            'kcal': int(drink_size_info[1][1]),
            'protein': int(drink_size_info[1][2]),
            'fat': int(drink_size_info[1][3]),
            'carbohydrate': int(drink_size_info[1][4])
        }
    if len(drink_size_info) > 2:
        size_data['big-size'] = {
            'size': drink_size_info[2][0],
            'kcal': int(drink_size_info[2][1]),
            'protein': int(drink_size_info[2][2]),
            'fat': int(drink_size_info[2][3]),
            'carbohydrate': int(drink_size_info[2][4])
        }
    json_data['drink-page'].append({
        'name': translated_name,
        'type': drink_info[0][1],
        'price': drink_info[0][3],
        'description': drink_info[0][4],
        'photo_path': drink_info[0][5],
        'ingredient': [ingredient for item in drink_description_info for ingredient in item],
        **size_data
    })
    print(json_data)
    return render_template(f'selected-coffee.html', drink_name=drink_name, json_data=json_data)

@app.route('/add_to_basket_and_go_menu', methods=['POST'])
def add_to_basket_and_go_menu():
    drink_name = request.form.get('drink_name')
    if drink_name:
        # Записываем название товара в сессию
        session['basket'] = session.get('basket', []) + [drink_name]
        # Перенаправляем пользователя на страницу каталога
        return redirect('/coffee-menu')
    return 'Bad request', 400

@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    drink_name = request.form.get('drink_name')
    if drink_name:
        # Записываем название товара в сессию
        session['basket'] = session.get('basket', []) + [drink_name]
        # Перенаправляем пользователя на страницу корзины
        return redirect('/basket')
    return 'Bad request', 400
def reformate_from_db_to_page(name):
    return name.replace("_", " ").capitalize()

@app.route('/delete_from_basket', methods=['POST'])
def delete_from_basket():
    drink = translate(request.form.get('basket_item'))
    if 'basket' in session:
        # Удаляю напиток из сессии
        if drink in session['basket']:
            idx = session['basket'].index(drink)
            del session['basket'][idx]
            session.modified = True  # Пометить сессию как измененную
            return redirect('/basket')
    return 'Bad request', 400

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    conn = get_db_connection()
    cursor = conn.cursor()
    last_personal_order_ids = []
    last_orders_id = None
    current_date = datetime.now()
    time_formatted = current_date.strftime('%H:%M:%S')  # Формат времени часы:минуты:секунды
    date_formatted = current_date.strftime('%d/%m/%Y')  # Формат даты день/месяц/год
    final_formatted_date = f"{time_formatted} {date_formatted}"
    barista_at_work = conn.execute(f'''
                SELECT schedule.barista_id, schedule.start_time, schedule.finish_time
                FROM schedule
                WHERE schedule.date = "{date_formatted}"
            ''').fetchall()
    barista_pool = []
    for item in barista_at_work:
        if time_difference(time_formatted[:5], item[2])[0] > 0 or (
                time_difference(time_formatted[:5], item[2])[0] == 0 and time_difference(time_formatted[:5], item[2])[1] > 0):
            if time_difference(item[1], time_formatted[:5])[0] > 0 or (
                    time_difference(item[2], time_formatted[:5])[0] == 0 and
                    time_difference(item[1], time_formatted[:5])[1] > 0):
                barista_pool.append(item[0])
    # if len(barista_pool) == 0:
    #     print('У вас не заполнен график на данный день, поэтому ошибка при формировании заказа!!!')
    #     return redirect('/')
    # Вставка данных в таблицу "personal order"
    # Для каждого объекта в корзине
    for item in session['basket']:
        # считываем его айди в таблице меню
        new_item = translate(item)
        coffee_IDs = conn.execute(f'SELECT id FROM menu WHERE name="{new_item}"').fetchall()
        # записываем в персональный заказ айди позиции
        values_personal_order = ('M', coffee_IDs[0][0])
        cursor.execute('INSERT INTO personal_order (size, menu_id) VALUES (?, ?)', values_personal_order)
        conn.commit()
        # запоминаем айди вставки
        last_personal_order_ids.append(cursor.lastrowid)
    # чистим корзину от заказа
    order_count_up = 0
    if session['basket']:
        order_count_up = 1
    with DataPusher('database.db') as changer:
        changer.update_data(table='User', ID=(changer.select_data('User', 'id', login=session['username'])[0][0]),order_count=(changer.select_data('User', 'order_count', login=session['username'])[0][0] + order_count_up))
    session['basket'].clear()
    session.modified = True  # Пометить сессию как измененную
    # Добавляем заказ в таблицу заказов
    values_orders = (final_formatted_date, 0, 1, session['username'])
    # values_orders = (final_formatted_date, 0, random.choice(barista_pool), session['username'])
    cursor.execute('INSERT INTO orders (order_date, stars, barista_id, User_id) VALUES (?, ?, ?, ?)', values_orders)
    conn.commit()
    # запоминаем айди вставки
    last_orders_id = cursor.lastrowid
    # Связываем заказанные позиции с общим заказом
    for item in last_personal_order_ids:
        values_oho = (item, last_orders_id)
        cursor.execute('INSERT INTO orders_has_order (order_id, orders_id) VALUES (?, ?)', values_oho)
        conn.commit()
    conn.close()
    return redirect('/profile')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print(session)
        if session.get('role') == 'user':
            return redirect(url_for('profilepage'))
        elif session.get('role') == 'barista':
            return redirect(url_for('baristapage'))
        elif session.get('role') == 'admin':
            return redirect(url_for('adminpage'))
        else:
            return redirect(url_for('profilepage'))
    print(session)
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        session['username'] = user['username']
        print(session)
        if user and user['password'] == hashed_password and user['role'] == 'user':
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['logged_in'] = True
            session.modified = True  # Пометить сессию как измененную
            return redirect(url_for('profilepage'))

        elif user and user['password'] == hashed_password and user['role'] == 'admin':
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('adminpage'))

        elif user and user['password'] == hashed_password and user['role'] == 'barista':
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('baristapage'))
        else:
            error = 'Неправильное имя пользователя или пароль'
    return render_template('login.html', error=error)

@app.route('/registration', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        second_password = request.form['second_password']
        email = request.form['email']
        fullname = request.form['fullname']
        phone_number = request.form['number']
        if password != second_password:
            error = 'Пароли не совпадают!'
            print(error)
            return render_template('registration.html', error=error)
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user:
            error = 'Пользователь с таким логином уже зарегестрирован!'
            print(error)
            return render_template('registration.html', error=error)
        if not user:
            conn = get_db_connection()
            c = conn.cursor()
            # Вставка данных в таблицу "users"
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            values_users = (username, hash_password, 'user')
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', values_users)
            conn.commit()
            # Вставка данных в таблицу "User"
            values_User = (username, fullname, email, phone_number, 'Beginner', 0, 0)
            c.execute(
                'INSERT INTO User (login, fullname, email, number, rang, order_count, average_points) VALUES (?, ?, ?, ?, ?, ?, ?)',
                values_User)
            conn.commit()
            conn.close()
            session['username'] = username
            session['logged_in'] = True
            session.modified = True  # Пометить сессию как измененную
            return redirect(url_for('profilepage'))
        else:
            error = 'Неправильное имя пользователя или пароль'
    return render_template('registration.html', error=error)

@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)