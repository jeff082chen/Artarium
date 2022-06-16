import pymysql


db = pymysql.connect(
    host = '104.199.235.116',
    user = 'artarium',               
    password = '0000', 
    database = 'artarium',
    port = 3306
)


def insert_Team(ID, UID, member, place, contact, /, db = db): #揪團
    try:
        with db.cursor() as cursor:
            sql = 'INSERT INTO team (id, UID, member_id, place, contact) VALUES (%s, %s, %s, %s, %s)' 
            cursor.execute(sql, (ID, UID, member, place, contact))
            db.commit()
    except Exception as ex:
        print(ex)
        
def delete_Team(ID, UID, /, db = db):#刪除揪團
    try:
        with db.cursor() as cursor:
            sql = 'DELETE FROM team WHERE id = %s AND UID = %s'  
            cursor.execute(sql, (ID, UID))
            db.commit()
    except Exception as ex:
        print(ex)  

def leave_message(ID, UID, member, content, /, db = db): #留言
    try:
        with db.cursor() as cursor:          
            sql = 'INSERT INTO reply (id, UID, member_id, content) VALUES (%s, %s, %s, %s)'
            cursor.execute(sql, (ID, UID, member, content))
            db.commit()
    except Exception as ex:
        print(ex)
def delete_message(ID, UID, /, db = db): #刪除留言
    try:
        with db.cursor() as cursor:
            sql = 'DELETE FROM reply WHERE id = %s AND UID = %s' 
            cursor.execute(sql, (ID, UID))
            db.commit()
    except Exception as ex:
        print(ex)
        
def thumb_up(ID, UID, member, /, db = db): #按讚
    try:
        with db.cursor() as cursor:
            command = 'SELECT likeCount from reply WHERE id = %s AND UID = %s'
            cursor.execute(command, (ID, UID))
            result = cursor.fetchone()
            likecount = list(result)[0] + 1
            sql = 'UPDATE reply SET likeCount = %s WHERE id = %s AND UID = %s'  
            cursor.execute(sql, (likecount, ID, UID))
            db.commit()
            
    except Exception as ex:
        print(ex)

def unlike(ID, UID, /, db = db): #取消讚
    try:
         with db.cursor() as cursor:
             command = 'SELECT likeCount from reply WHERE id = %s AND UID = %s'
             cursor.execute(command, (ID, UID))
             result = cursor.fetchone()
             likecount = list(result)[0] - 1
             sql = 'UPDATE reply SET likeCount = %s WHERE id = %s AND UID = %s'
             cursor.execute(sql, (likecount, ID, UID))
             db.commit()
             
    except Exception as ex:
        print(ex)
def favor(UID, member, /, db = db):
    try:
         with db.cursor() as cursor:
             cursor.execute('INSERT INTO favorites (UID, member_id) VALUES (%s, %s)', (UID, member))
             db.commit()
    except Exception as ex:
        print(ex)
def rm_favor(UID, member, /, db = db):
    try:
         with db.cursor() as cursor:
             cursor.execute('DELETE FROM favorites WHERE UID = %s AND member_id = %s', (UID, member))
             db.commit()
    except Exception as ex:
        print(ex)
def recommend(db = db):
    try:
        with db.cursor() as cursor:
            sql = 'SELECT title, imageURL FROM activities \
                JOIN reply ON activities.UID = reply.UID \
                    WHERE reply.likeCount > 0 \
                        ORDER BY reply.likeCount'
            cursor.execute(sql)       
            datas = list(cursor.fetchall())
        
            if len(datas) < 20:
                cursor.execute('SELECT title, imageURL FROM activities ORDER BY RAND() LIMIT %d' % (20-len(datas)))
                result = cursor.fetchall()
                for i in result:
                    datas.append(i)
            for data in datas:
                print ("活動名稱:", data[0], "\n", "圖片:", data[1], "\n", "\n")
    except Exception as ex:
        print(ex)         
if __name__=='__main__':
    #insert_Team(6,'5c7e1bcdaaa375d860933d3a','test', '博物館', '0911222055', db)
    
    #delete_Team(4, '5c7e1bcdaaa375d860933d3a', db)
    #leave_message(1, '5c7e1bcdaaa375d860933d3a','test', 'cool', db)
    #delete_message(1, '5c7e1bcdaaa375d860933d3a', db)
    #thumb_up(1, '5c7e1bcdaaa375d860933d3a', 'test')
    #unlike(1, '5c7e1bcdaaa375d860933d3a', 'test')
    #recommend(db)
    #favor('60796f9ad083a3a724cd5a1b', 'test')
    rm_favor('60796f9ad083a3a724cd5a1b', 'test')
    
    