import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = pymysql.connect(
    host = '104.199.235.116', 
    port = 3306, 
    user = 'artarium', 
    passwd = '0000', 
    db = 'artarium'
)

def main(user_id = None, db = db):

    already_end = 'SELECT title, member_id, endDate FROM favorites JOIN activities ON favorites.UID = activities.UID WHERE endDate < CURDATE()'
    end_in_a_week = 'SELECT title, member_id, endDate FROM favorites JOIN activities ON favorites.UID = activities.UID WHERE 0 <= datediff(endDate, CURDATE()) and datediff(endDate, CURDATE()) <= 7'

    if user_id is not None:
        already_end = already_end + f" AND member_id = '{user_id}'"
        end_in_a_week = end_in_a_week + f" AND member_id = '{user_id}'"

    cur = db.cursor()
    cur.execute(already_end)
    already_end_list = cur.fetchall()
    cur.execute(end_in_a_week)
    end_in_a_week_list = cur.fetchall()

    for event in already_end_list:

        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = f"你在 Artarium 追蹤的活動已經結束了😭"  #郵件標題
        content["from"] = "artarium0000@gmail.com"  #寄件者
        content["to"] = f"{event[1]}@gmail.com" #收件者
        content.attach(MIMEText(f"你追蹤的活動\n\n{event[0]}\n\n已經在 {event[2]} 結束了"))  #郵件內容

        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("artarium0000@gmail.com", "qwcmzdsooaygmoac")  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)

    for event in end_in_a_week_list:
        
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = f"你在 Artarium 追蹤的活動將在一週內結束"  #郵件標題
        content["from"] = "artarium0000@gmail.com"  #寄件者
        content["to"] = f"{event[1]}@gmail.com" #收件者
        content.attach(MIMEText(f"你追蹤的活動\n\n{event[0]}\n\n將在一週內結束"))  #郵件內容

        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("artarium0000@gmail.com", "qwcmzdsooaygmoac")  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)


if __name__ == "__main__":
    main()
    db.close()