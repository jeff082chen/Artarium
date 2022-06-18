import pymysql
import xml.etree.ElementTree as ET
import requests
import json

db = pymysql.connect(
    host = '104.199.235.116', 
    port = 3306, 
    user = 'artarium', 
    passwd = '0000', 
    db = 'artarium'
)

category = {
    b'\x01' : '音樂',
    b'\x02' : '戲劇',
    b'\x03' : '舞蹈',
    b'\x06' : '展覽'
}

category_int = {
    '音樂' : 1,
    '戲劇' : 2,
    '舞蹈' : 3,
    '展覽' : 6 
}

weather_dict = {
    "宜蘭縣": "F-D0047-003", 
    "桃園市": "F-D0047-007", 
    "新竹縣": "F-D0047-011",
    "苗栗縣": "F-D0047-015", 
    "彰化縣": "F-D0047-019",
    "南投縣": "F-D0047-023",
    "雲林縣": "F-D0047-027", 
    "嘉義縣": "F-D0047-031",
    "屏東縣": "F-D0047-035",
    "臺東縣": "F-D0047-039",
    "花蓮縣": "F-D0047-043",
    "澎湖縣": "F-D0047-047",
    "基隆市": "F-D0047-051",
    "新竹市": "F-D0047-055",
    "嘉義市": "F-D0047-059",
    "臺北市": "F-D0047-063",
    "高雄市": "F-D0047-067",
    "新北市": "F-D0047-071",
    "臺中市": "F-D0047-075",
    "臺南市": "F-D0047-079",
    "連江縣": "F-D0047-083",
    "金門縣": "F-D0047-087"
}

def get_slides(db = db):
    cur = db.cursor()
    slide = {}
    cur.execute(
        'SELECT imageUrl, UID FROM activities WHERE category = 1 AND imageUrl IS NOT NULL LIMIT 5'
    )
    slide['music'] = [{'imgUrl': res[0], 'UID': res[1]} for res in cur.fetchall()]
    cur.execute(
        'SELECT imageUrl, UID FROM activities WHERE category = 2 AND imageUrl IS NOT NULL LIMIT 5'
    )
    slide['drama'] = [{'imgUrl': res[0], 'UID': res[1]} for res in cur.fetchall()]
    cur.execute(
        'SELECT imageUrl, UID FROM activities WHERE category = 3 AND imageUrl IS NOT NULL LIMIT 5'
    )
    slide['dance'] = [{'imgUrl': res[0], 'UID': res[1]} for res in cur.fetchall()]
    slide['dance'] += slide['dance'][:2]
    cur.execute(
        'SELECT imageUrl, UID FROM activities WHERE category = 6 AND imageUrl IS NOT NULL LIMIT 5'
    )
    slide['exhibition'] = [{'imgUrl': res[0], 'UID': res[1]} for res in cur.fetchall()]
    cur.execute(
        'SELECT imageUrl, UID FROM activities WHERE imageUrl IS NOT NULL LIMIT 5'
    )
    slide['all'] = [{'imgUrl': res[0], 'UID': res[1]} for res in cur.fetchall()]
    return slide

def get_info(UID, db = db):
    cur = db.cursor()
    info = {}

    cur.execute(
        'SELECT title, category, descriptionFilterHtml, imageUrl, likeCount, UID FROM activities WHERE UID = %s', (UID, )
    )
    res = cur.fetchone()
    if res is None:
        return None
    info['title'] = res[0]
    info['category'] = category[res[1]]
    info['description'] = res[2]
    info['image'] = res[3]
    info['likeCount'] = res[4]
    info['UID'] = res[5]

    cur.execute(
        'SELECT startTime, endTime, location, locationName, onSales, longitude, latitude FROM shows WHERE UID = %s', (UID, )
    )
    res = cur.fetchall()
    info['shows'] = []
    for row in res:
        show = {}
        show['start_time'] = row[0]
        show['end_time'] = row[1]
        show['address'] = row[2]
        show['location'] = row[3]
        show['on_sale'] = "售票" if row[4] else "免費"
        show['longitude'] = row[5]
        show['latitude'] = row[6]
        info['shows'].append(show)

    cur.execute(
        'SELECT id, member_id, content FROM reply WHERE UID = %s', (UID, )
    )
    res = cur.fetchall()
    info['reply'] = []
    for row in res:
        reply = {}
        reply['id'] = row[0]
        reply['member_id'] = row[1]
        reply['content'] = row[2]
        info['reply'].append(reply)
    return info

def get_favorite(member_id, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT UID FROM favorites WHERE member_id = %s', (member_id, )
    )
    res = [row[0] for row in cur.fetchall()]
    shows = []
    for UID in res:
        cur.execute(
            'SELECT title FROM activities WHERE UID = %s', (UID, )
        )
        res = cur.fetchone()
        if res is None:
            continue
        shows.append({"title": res[0], "UID": UID})
    return shows

def get_search(title, category, city, date, db = db):
    cur = db.cursor()
    execute_str = f'SELECT UID FROM activities WHERE 1 '
    if title != '':
        execute_str += f' AND title LIKE "%{title}%"'
    if category != "全部":
        execute_str += f' AND category = {category_int[category]}'
    if date is not "":
        execute_str += f' AND startDate <= "{date}" AND endDate >= "{date}"'
    print(execute_str)
    cur.execute(
        execute_str
    )
    res = [row[0] for row in cur.fetchall()]
    res2 = []
    if city is not "":
        for UID in res:
            cur.execute(
                'SELECT location FROM shows WHERE UID = %s', (UID, )
            )
            res3 = cur.fetchall()
            if res3 is None:
                continue
            if any(row[0] is None for row in res3):
                continue
            if any(city in row[0] for row in res3):
                res2.append(UID)
    else:
        res2 = res
    shows = []
    for UID in res2:
        cur.execute(
            'SELECT title FROM activities WHERE UID = %s', (UID, )
        )
        res = cur.fetchone()
        if res is None:
            continue
        shows.append({"title": res[0], "UID": UID})
    return shows

def lucky_draw(db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT UID, imageUrl FROM activities WHERE imageUrl IS NOT NULL ORDER BY RAND() LIMIT 1'
    )
    res = cur.fetchone()
    return res[0], res[1]

def leave_reply(UID, member_id, content, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT id FROM reply WHERE UID = %s', (UID)
    )
    res = cur.fetchall()
    if res is None:
        reply_id = 1
    else:
        reply_id = len([row[0] for row in res]) + 1
    cur.execute(
        'INSERT INTO reply (id, UID, member_id, content) VALUES (%s, %s, %s, %s)', (reply_id, UID, member_id, content)
    )
    db.commit()

def delete_reply(UID, user_id, comment_id, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT member_id FROM reply WHERE UID = %s AND id = %s', (UID, comment_id)
    )
    res = cur.fetchone()
    if res is None:
        return False
    if res[0] != user_id:
        return False
    cur.execute(
        'UPDATE reply SET content = "已刪除" WHERE UID = %s AND id = %s', (UID, comment_id)
    )
    db.commit()

def get_weather(longitude, latitude, db = db):
    try:
        r = requests.get(f"https://api.nlsc.gov.tw/other/TownVillagePointQuery/{longitude}/{latitude}")
        print(f"https://api.nlsc.gov.tw/other/TownVillagePointQuery/{longitude}/{latitude}")
        root = ET.fromstring(r.text)
        city = root[1].text
        area = root[3].text
        params = {
            "Authorization": "CWB-E4C5EEEE-2ACE-473C-AD41-FC89855FBAD2",
            "locationName": area
        }
        r = requests.get(f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{weather_dict[city]}", params=params)
        weather_data = json.loads(r.text)
        weather_data = weather_data["records"]["locations"][0]["location"][0]["weatherElement"]
        weather_info = []
        rain_info = weather_data[0]["time"]
        T_info = weather_data[1]["time"]
        for i in range(len(rain_info)):
            _weather = {}
            _weather["rain"] = rain_info[i]["elementValue"][0]["value"] if rain_info[i]["elementValue"][0]["value"] != " " else "Null"
            _weather["T"] = T_info[i]["elementValue"][0]["value"]
            _weather["start"] = rain_info[i]["startTime"]
            _weather["end"] = rain_info[i]["endTime"]
            weather_info.append(_weather)
    except:
        weather_info = []
    return weather_info

def get_team(UID, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT id, member_id, place, contact FROM team WHERE UID = %s', (UID, )
    )
    res = cur.fetchall()
    if res is None:
        return []
    teams = []
    for row in res:
        team = {}
        team["id"] = row[0]
        team["member_id"] = row[1]
        team["place"] = row[2]
        team["contact"] = row[3]
        teams.append(team)
    return teams

def send_team(UID, member_id, contact, place, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT id FROM team WHERE UID = %s', (UID, )
    )
    res = cur.fetchall()
    if res is None:
        team_id = 1
    else:
        team_id = len([row[0] for row in res]) + 1
    cur.execute(
        'INSERT INTO team (id, UID, member_id, contact, place) VALUES (%s, %s, %s, %s, %s)', (team_id, UID, member_id, contact, place)
    )
    db.commit()

def cancel_team(UID, team_id, user_id, db = db):
    cur = db.cursor()
    cur.execute(
        'SELECT member_id FROM team WHERE UID = %s AND id = %s', (UID, team_id)
    )
    res = cur.fetchone()
    if res is None:
        return False
    if res[0] != user_id:
        return False
    cur.execute(
        'UPDATE team SET contact = "已刪除", place = "" WHERE UID = %s AND id = %s', (UID, team_id)
    )
    db.commit()
    return True

def get_restaurant(latitude: float, longitude: float, dis: float, /, db = db, n: int = None):
    ''' get restaurants close to a specific place
    latitude, longitude: coordinate of specific place
    dis: maximum distance (in kilometer)
    n: maximun return (default infinite)
    
    return value: list of tuple
    '''
    
    dis *= 0.01
    
    cursor = db.cursor()
    execute_str = "SELECT * FROM restaurant WHERE "
    execute_str += " %s - %s <= latitude "
    execute_str += " and %s + %s >= latitude "
    execute_str += " and %s - %s <= longitude "
    execute_str += " and %s + %s >= longitude "
    cursor.execute(execute_str, (latitude, dis, latitude, dis, longitude, dis, longitude, dis))
    
    result = list(cursor.fetchall())
    
    if n is not None:
        result = result[:n]

    restaurants = []
    for i, r in enumerate(result):
        restaurant = {}
        restaurant['id'] = i
        restaurant['latitude'] = r[0]
        restaurant['longitude'] = r[1]
        restaurant['type'] = r[2]
        restaurant['name'] = r[3]
        restaurant['address'] = r[4]
        restaurant['city'] = r[5]
        restaurant['area'] = r[6]
        restaurants.append(restaurant)

    return restaurants