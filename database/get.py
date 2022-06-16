import pymysql
from datetime import date
db = pymysql.connect(
    host = '104.199.235.116',
    user = 'artarium',               
    password = '0000', 
    database = 'artarium',
    port = 3306
)
category = {
    '音樂' : 1,
    '戲劇' : 2,
    '舞蹈' : 3,
    '展覽' : 6 }
def search_Activity_by_title (title, /, db = db):
    try:
        with db.cursor() as cursor:
            title_str = "%" + title + "%"
            sql = 'SELECT title, imageURL FROM activities WHERE title LIKE %s'
            cursor.execute(sql, (title_str))
            datas = cursor.fetchmany(10)  
            for data in datas:
                print ("活動名稱:", data[0], "\n", "圖片:", data[1], "\n", "\n")
    except Exception as ex:
        print(ex)
            
def isValidDate(datestr):
    try: 
        date.fromisoformat(datestr)
    except:
        print ("Please print YYYY-MM-DD or YYYY,MM,DD")
        return False
    
def search_Activity_by_date (date, /, db = db):
    try:
        with db.cursor() as cursor:
            isValidDate(date)
            sql = 'SELECT title, imageURL, startDate FROM activities WHERE startDate >= %s ORDER BY startDate'
            cursor.execute(sql, (date))
            datas = cursor.fetchmany(10)
        
            if len(datas) == 0:
                print ("No activity...")
            else:
                for data in datas:
                    print("活動名稱:", data[0], "\n", "圖片:", data[1], "\n", "活動開始日期:", data[2], "\n", "\n")
    except Exception as ex:
        print(ex)      
def search_Activity_by_type (ty, /, db = db):#1音樂、2戲劇、3舞蹈、6展覽
    try:
        with db.cursor() as cursor:
            if ty in category:
                sql = 'SELECT title, imageURL FROM activities WHERE category = %s' 
                print ((category.get(ty)))
                cursor.execute(sql, (category.get(ty)))
                datas = cursor.fetchmany(10)
        
                if len(datas) == 0:
                    print ("No activity...")
                for data in datas:
                    print("活動名稱:", data[0], "\n", "圖片:", data[1], "\n", "\n", "\n")
            else:
                print('Please input 音樂 or 戲劇 or 舞蹈 or 展覽')
    except Exception as ex:
        print(ex) 
def get_favor(member, /, db = db):
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT title, imageURL FROM favorites JOIN activities ON activities.UID = favorites.UID WHERE member_id = %s', (member))     
            datas = cursor.fetchall()
    
            if len(datas) == 0:
                print ("No collection...")
            for data in datas:
                print("活動名稱:", data[0], "\n", "圖片:", data[1], "\n", "\n", "\n")
    
    except Exception as ex:
        print(ex) 
def update(UID, /, db = db):
    try:
        with db.cursor() as cursor:
           
                sql = 'UPDATE activities SET category = 3 WHERE UID = %s' 
                
                cursor.execute(sql, (UID))
                db.commit()
        
    except Exception as ex:
        print(ex) 
if __name__=='__main__':
    #search_Activity_by_title("博物館", db)
    #search_Activity_by_date("2022-12-01", db)
    #search_Activity_by_type('音樂', db)
    #update('607d50ddd083a37388433308', db)
    get_favor('test')
