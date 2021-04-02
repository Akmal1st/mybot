import telebot
mytoken = "914066529:AAEjK16XuhHzX6amB1mgC31cPFLrda2ZE0c"
bot = telebot.TeleBot(mytoken)
print("Bot ishga tushdi")

@bot.message_handler(commands=["start"])
def starts(m):
    bot.send_message(m.chat.id, f"Assalomu alaykum {m.from_user.first_name}")

@bot.message_handler(commands=["namoz"])
def namoz_vaqtlari(m):
    text2 = ""
    import urllib.request as ul
    from bs4 import BeautifulSoup
    site = "https://islom.uz/prayertimes"
    try:
        page = ul.urlopen(site)
        #bot.send_message(m.chat.id, 'done')
        soup = BeautifulSoup(page, features='lxml')
        s = []
        for x in soup.find_all('div'):
            clas = " ".join(x.get('class')) if x.get('class')!=None else ""
            #print(clas)
            if clas=="p_clock" or clas=='p_clock c_active':
                s.append(x.get_text())

        #s = s[4:]
        #print(s)
        text2 = f"Bugun:\n {s[0]} - bomdod\n {s[1]} - quyosh\n {s[2]} - peshin\n {s[3]} - asr\n {s[4]} - shom\n {s[5]} - xufton\n\n islom.uz saytidan olindi"
        bot.send_message(m.chat.id, text2)
    except Exception as e:
        bot.send_message(m.chat.id, "Ma`lumot olinmadi, keyinroq urinib ko'ring")
        bot.send_message(m.chat.id, e)

@bot.message_handler(commands=['jadval'])
def jadval(m):
    import urllib.request as ul
    import urllib.parse as up
    import time
    from bs4 import BeautifulSoup
    my_data = {"request":"true","auth_stud_id":"300034845","password":"O9IM-D21-62RE"}
    site = "http://talaba.tdpu.uz/student/jadval"
    data = up.urlencode(my_data)
    data = data.encode('cp1251')
    try:
        page = ul.urlopen(site,data)
        soup = BeautifulSoup(page, features='lxml')
        jadval = []
        for x in soup.find_all('div'):
            clas = " ".join(x.get('class')) if x.get('class')!=None else ""
            xona = [n.get_text() for n in x.find_all('div') if n.get('style')=='padding:3px;']
            xl = len(xona)
            if clas=="panel panel-default col-md-3":
                h4 = x.find('h4').get_text().split()[0]
                b = [n.get_text() for n in x.find_all('b')]
                div = [n.get_text() for n in x.find_all('div') if n.get('align')=='right']
                s = ''
                s+=h4+"\n\n"
                for k in range(len(b)//4):
                    s+="%s\n" % (" ".join(div[k].split()))
                    s+="%s\n%s\n" % (b[4*k+2], " ".join(b[4*k+3].split()))
                    s+='%s\n' % (xona[k%xl])
                jadval.append(s)
        day = time.gmtime().tm_wday
        #print(len(jadval))
        if day==6:
            text2 = "dam olish kuni"
        else:
            text2 = jadval[day]
        bot.send_message(m.chat.id, text2)
    except:
        bot.send_message(m.chat.id, 'Jadvalni olishda xatolik\nKeyinroq urinib ko\'ring')



if __name__=='__main__':
    bot.polling(none_stop=True)
