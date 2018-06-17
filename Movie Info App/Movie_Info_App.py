from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from http.client import HTTPSConnection
from xml.dom.minidom import parse, parseString
from datetime import datetime
import webbrowser
import arrangeStr

# 이메일 ---------
import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Tk_DayMovie
DayMovieDoc = None
MovieChart = None
ChartFlag = True
NextList = None
PrevList = None
FrontText = ["순위", "제목", "점유율", "누적관객수"]
SecondText = []
TitleText = []
ColorText = ["red", "green", "yellow", "pink", "orange"]

#
# Tk_SearchMovie
SearchMovieDoc = None
MovieList = None
SearchMovieInput = None
MovieName = ''
ResultMovie = None
DetailMovieLabel = None
MovieJPG = None
ResultDic = None

# 익진
RelYearFrom = 0
RelYearTo = 0
RelYearExist = False
firstRun = True
clickedBtn = False
wrongInput = False
titleStrLabel = None
subtitleStrLabel = None
directorLabel = None
actorLabel = None
userRatingLabel = None

#Tk_Email
Email = None
SendEmailEntry = None

def CGVLogoButton():
    webbrowser.open_new('http://www.cgv.co.kr/')


def MEGABOXLogoButton():
    webbrowser.open_new('http://www.megabox.co.kr')

def LOTTELogoButton():
    webbrowser.open_new('http://www.lottecinema.co.kr')


def getuserRating(ImageDoc, title):
    itemList = ImageDoc.getElementsByTagName('item')

    for item in itemList:
        for attr in item.childNodes:
            if attr.nodeName == "userRating":
                if attr.hasChildNodes():
                    return attr.firstChild.nodeValue
                    break

def changeDate(): # 날짜 변경(제대로 입력 && 검색 버튼 클릭시) 및 잘못 입력한 경우 예외처리
    global insertedDate, clickedBtn, DayMovieDoc, wrongInput, ChartFlag
    clickedBtn = True
    ChartFlag = True

    if boxSubEntry.get() is not '':  # 비어있지 않으면 읽고, 날짜 변경
        insertedDate = str(boxSubEntry.get())
        if len(boxSubEntry.get()) != 8:
            boxSubEntry.delete(0, 'end')
            boxSubEntry.insert(0, 'ex)20171201')
            wrongInput = True
        else:
            DayMovieDoc = LoadXML_DayMovie(insertedDate)
            TitleText = Label_DayMovie(['movieNm', 'rank', 'salesShare', 'audiAcc'])
            Image_DayMovie(TitleText)
            clickedBtn = False

    if boxSubEntry.get() is '':
        boxSubEntry.delete(0, 'end')
        boxSubEntry.insert(0, 'ex)20180525')
        wrongInput = True




def getToday(): # 검색에 용이하게 현재 날짜 가져옴.
    now = datetime.now()

    if now.month / 10 <= 1:
        zeroMonth = '0' + str(now.month)
    else:
        zeroMonth = str(now.month)

    if now.day / 10 <= 1:
        zeroDay = '0' + str(now.day-1)
    else:
        zeroDay = str(now.day-1)

    today = str(now.year) + str(zeroMonth) + str(zeroDay)
    return today


# -----------------------------------------------------------------------------

def Tk_DayMovie():
    global MovieChart
    global DayMovieDoc
    global insertedDate # 삽입되는 날짜
    global clickedBtn   # 검색 버튼 눌렀는지?

    MovieChart = Tk()

    MovieChart.title("MovieChart")
    MovieChart.geometry("1000x600+500+100")

    if firstRun is True:
        insertedDate = getToday()
    DayMovieDoc = LoadXML_DayMovie(insertedDate)
    TitleText = Label_DayMovie(['movieNm', 'rank', 'salesShare', 'audiAcc'])
    Image_DayMovie(TitleText)
    clickedBtn = False

    MovieChart.mainloop()


def LoadXML_DayMovie(Day):
    global firstRun
    firstRun = False
    server = "www.kobis.or.kr"
    key = "430156241533f1d058c603178cc3ca0e"
    targetDt = Day

    conn = HTTPSConnection(server)
    conn.request("GET", "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=" + \
                 key + "&targetDt=" + targetDt)

    req = conn.getresponse()
    if int(req.status) == 200:
        todaydom = parseString(req.read())
        return todaydom
    else:
        return None

def NextChart():
    global DayMovieDoc
    global FrontText
    global SecondText
    global TitleText
    global ColorText
    global ChartFlag
    global PrevList
    global NextList

    ChartFlag = False
    count = 0
    string = ''

    dailBoxOfficeList = DayMovieDoc.getElementsByTagName('dailyBoxOffice')

    for movie in dailBoxOfficeList:
        if count >= 5:
            for attr in movie.childNodes:
                for object in ['movieNm', 'rank', 'salesShare', 'audiAcc']:
                    if attr.nodeName == object:
                        if attr.hasChildNodes():
                            SecondText.append(attr.firstChild.nodeValue)
            for i in range(0, 4):
                string += FrontText[i]
                string += " : "
                string += SecondText[i]
                if i != 3:
                    string += "\n"

                label = Label(MovieChart, text=string, bg=ColorText[count % 5], fg="black", font="나눔고딕 8", width="22")
                label.place(x=55 + (180 * (count - 5)), y=330)

        string = ''
        SecondText = []
        count += 1

    PrevList = Button(MovieChart, text="<", command=PrevChart)
    PrevList.place(x=10, y=200)
    PrevList.config(width=2)
    NextList.destroy()

    Image_DayMovie(TitleText)

def PrevChart():
    global DayMovieDoc
    global FrontText
    global SecondText
    global TitleText
    global ColorText
    global ChartFlag
    global NextList
    global PrevList

    ChartFlag = True
    count = 0
    string = ''

    dailBoxOfficeList = DayMovieDoc.getElementsByTagName('dailyBoxOffice')

    for movie in dailBoxOfficeList:
        if count < 5:
            for attr in movie.childNodes:
                for object in ['movieNm', 'rank', 'salesShare', 'audiAcc']:
                    if attr.nodeName == object:
                        if attr.hasChildNodes():
                            SecondText.append(attr.firstChild.nodeValue)
            for i in range(0, 4):
                string += FrontText[i]
                string += " : "
                string += SecondText[i]
                if i != 3:
                    string += "\n"

                label = Label(MovieChart, text=string, bg=ColorText[count % 5], fg="black", font="나눔고딕 8", width="22")
                label.place(x=55 + (180 * (count)), y=330)

        string = ''
        SecondText = []
        count += 1

    NextList = Button(MovieChart, text=">", command=NextChart)
    NextList.place(x=965, y=200)
    NextList.config(width=2)
    PrevList.destroy()

    Image_DayMovie(TitleText)



def Label_DayMovie(SearchList):
    global DayMovieDoc
    global FrontText
    global SecondText
    global TitleText
    global ColorText
    global ChartFlag
    global NextList

    dailBoxOfficeList = DayMovieDoc.getElementsByTagName('dailyBoxOffice')

    string = ''
    TitleText = []
    count = 0

    ########################################
    # UI
    ########################################
    # 박스오피스 리스트 변경 버튼

    NextList = Button(MovieChart, text=">", command=NextChart)
    NextList.place(x=965, y=200)
    NextList.config(width=2)

    # 영화 검색 버튼
    searchBtn = Button(MovieChart, text="영화 검색", command=Tk_SearchMovie, font='나눔고딕 20')
    searchBtn.config(width=35)
    searchBtn.place(x=200, y=520)
    #########################################

    for movie in dailBoxOfficeList:
        for attr in movie.childNodes:
            for object in SearchList:
                if attr.nodeName == object:
                    if attr.hasChildNodes():
                        SecondText.append(attr.firstChild.nodeValue)
        for i in range(0, 4):
            if i == 1:
                TitleText.append(SecondText[i])
            string += FrontText[i]
            string += " : "
            string += SecondText[i]
            if i != 3:
                string += "\n"

        if count < 5:
            label = Label(MovieChart, text=string, bg=ColorText[count % 5], fg="black", font="나눔고딕 8", width="22")
            label.place(x=55 + (180 * count), y=330)

        string = ''
        SecondText = []
        count += 1

    ########################################
    # 20180527기준 박스오피스 & 검색 버튼
    ########################################
    global boxSubEntry, insertedDate, wrongInput
    # boxSubEntry = Entry(master, text= + " 기준 박스오피스", font='나눔고딕 16', width=8)
    boxSubEntry = Entry(MovieChart, font='나눔고딕 20', width=11)
    boxSubEntry.place(x=265, y=10)
    if firstRun is True:
        boxSubEntry.insert(0, getToday())
    elif firstRun is not True and wrongInput is not True:
        boxSubEntry.insert(0, insertedDate)


    boxSubLa = Label(MovieChart, text="기준 박스오피스", font='나눔고딕 20')
    boxSubLa.place(x=450, y=10)
    dateBtn = Button(MovieChart, text="검색", width=1, font='나눔고딕 16', command=changeDate)
    dateBtn.place(x=650, y=8)
    dateBtn.config(width=10)
    ########################################

    TheaterLa = Label(MovieChart, text="────────────────────── 영화관 바로가기 ──────────────────────", font='나눔고딕 15', fg='gray')
    TheaterLa.place(x=0, y=400)


    MEGABOXImage = Image.open("MegaBox.JPG")
    MEGABOXPhoto = ImageTk.PhotoImage(MEGABOXImage)
    MEGABOX = Button(MovieChart, image=MEGABOXPhoto, command=MEGABOXLogoButton)
    MEGABOX.image = MEGABOXPhoto
    MEGABOX.place(x=100, y=430)

    CGVImage = Image.open("CGV.PNG")
    CGVPhoto = ImageTk.PhotoImage(CGVImage)
    CGV = Button(MovieChart, image=CGVPhoto, command=CGVLogoButton)
    CGV.image = CGVPhoto
    CGV.place(x=420, y=430)

    LOTTEImage = Image.open("Lottecinema.PNG")
    LOTTEPhoto = ImageTk.PhotoImage(LOTTEImage)
    LOTTE = Button(MovieChart, image=LOTTEPhoto, command=LOTTELogoButton)
    LOTTE.image = LOTTEPhoto
    LOTTE.place(x=630, y=430)



    #path = r'E:/[Study]/2018/1학기/과제/Script_Term_Project/CGV_logo.jpg'

    # 영화 예매 사이트 링크 버튼
    #path=r'E:/[Study]/2018/1학기/과제/Script_Term_Project/롯데시네마.PNG'
    #image = Image.open(path)
    #photo = ImageTk.PhotoImage(image)

    #CGV = Button(MovieChart, image=photo, command=CGVLogoButton)
    #CGV.place(x=200, y = 50)
    #CGV.config(width=500, height=200)
    return TitleText


def Image_DayMovie(TitleText):
    global DayMovieDoc
    global MovieChart
    global ChartFlag

    ImgURL = []
    image = []

    for i in range(0, 5):
        if ChartFlag == True:
            server = "openapi.naver.com"
            client_id = "iEV22cE2b1ZJnyGDYXtc"
            client_secret = "xJB_PnOFmw"
            text = urllib.parse.quote(TitleText[i])

            conn = HTTPSConnection(server)
            conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1", None,
                         {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})

            req = conn.getresponse()
            if int(req.status) == 200:
                ImageDoc = parseString(req.read())
                ImgURL.append(getJpgURL(ImageDoc, TitleText[i]))

        else:
            server = "openapi.naver.com"
            client_id = "iEV22cE2b1ZJnyGDYXtc"
            client_secret = "xJB_PnOFmw"
            text = urllib.parse.quote(TitleText[i+5])

            conn = HTTPSConnection(server)
            conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1", None,
                         {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})

            req = conn.getresponse()
            if int(req.status) == 200:
                ImageDoc = parseString(req.read())
                ImgURL.append(getJpgURL(ImageDoc, TitleText[i+5]))

    for i in range(0, len(ImgURL)):
        #print(ImgURL[i])
        if ImgURL[i] != None:
            with urllib.request.urlopen(ImgURL[i]) as u:
                raw_data = u.read()
            tmp = Image.open(BytesIO(raw_data))
            tmp = tmp.resize((160, 208), Image.ANTIALIAS)
            tmp = ImageTk.PhotoImage(tmp)
            image.append(tmp)

            JPG = Label(MovieChart, image=image[i], bg="Black")
            JPG.place(x=55 + (180 * i), y=100)
        else:
            image.append(None)

    MovieChart.mainloop()


def getJpgURL(ImageDoc, title):
    itemList = ImageDoc.getElementsByTagName('item')

    for item in itemList:
        for attr in item.childNodes:
            if attr.nodeName == "title":
                if attr.firstChild.nodeValue.find(title):
                    pass
                else:
                    continue
            if attr.nodeName == "image":
                if attr.hasChildNodes():
                    return attr.firstChild.nodeValue
                    break
            #if attr.nodeName == "userRating":
            #    if attr.hasChildNodes():
            #        return attr.firstChild.nodeValue
            #        break


#------------------------------------------------------------------------------------------
def Tk_SearchMovie():
    global MovieList
    global SearchTitleInput
    global SearchMovieDoc
    global MovieName
    global ResultMovie
    global DetailMovieLabel
    global MovieJPG
    global SearchRelYearFromInput, SearchRelYearToInput

    global titleStrLabel
    global subtitleStrLabel
    global directorLabel
    global actorLabel
    global userRatingLabel


    MovieList = Toplevel()
    MovieList.title("SearchMovie")
    MovieList.geometry("1000x500+500+200")
    titleStrLabel = Label(MovieList)
    subtitleStrLabel = Label(MovieList)
    directorLabel = Label(MovieList)
    actorLabel = Label(MovieList)
    userRatingLabel = Label(MovieList)



    # -----------------------------------------------------------------------------
    # 상단 검색 UI
    # -----------------------------------------------------------------------------
    SearchTitleLabel = Label(MovieList, text="      제목", font="나눔고딕 20")
    SearchTitleLabel.place(x=180, y=10)

    SearchRelYearLabel = Label(MovieList, text="개봉년도", font="나눔고딕 20")
    SearchRelYearLabel.place(x=180, y=60)

    SearchTitleInput = Entry(MovieList)
    SearchTitleInput.place(x=320, y=10)
    SearchTitleInput.config(font='나눔고딕 20', width=20)

    SearchRelYearFromInput = Entry(MovieList)
    SearchRelYearFromInput.place(x=320, y=60)
    SearchRelYearFromInput.config(font='나눔고딕 20', width=5)

    SearchRelYearToInput = Entry(MovieList)
    SearchRelYearToInput.place(x=470, y=60)
    SearchRelYearToInput.config(font='나눔고딕 20', width=5)

    SearchMovieButton = Button(MovieList, text="검색", command=Button_SearchMovie, font='나눔고딕 16')
    SearchMovieButton.config(width=10,height=3)
    SearchMovieButton.place(x=690, y=10)

    #EmailMovieButton = Button(MovieList, text="이메일", command=Button_EmailMovie)
    #EmailMovieButton.config(width=15, height=4)
    #EmailMovieButton.place(x=800, y=20)

    SearchTitleLabel = Label(MovieList, text="~", font="고딕 20")
    SearchTitleLabel.place(x=425, y=60)


    divLineLabel = Label(MovieList, text="――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――", font="고딕 8")
    divLineLabel.place(x=0, y=110)
    divLineLabel.config(height=1)

    #-----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # 리스트 박스
    # -----------------------------------------------------------------------------
    ListTitleLabel = Label(MovieList, text = "검색 리스트",font="나눔고딕 14")
    ListTitleLabel.place(x=70, y=130)
    ListTitleLabel.config(height=1)
    ResultMovie = Listbox(MovieList)
    ResultMovie.place(x=10, y=170)
    ResultMovie.config(width=30, height=20)

    DetailMovieButton = Button(MovieList, text="이동", command=Button_DetailMovie)
    DetailMovieButton.place(x=250, y=170)
    DetailMovieButton.config(width=5, height= 20)
    # -----------------------------------------------------------------------------

    MovieJPG = Label(MovieList)
    DetailMovieLabel  = Label(MovieList)

    MovieList.mainloop()

def Button_SearchMovie():
    global SearchTitleInput
    global SearchMovieDoc
    global MovieName
    global MovieList
    global SearchRelYearFromInput, SearchRelYearToInput
    global RelYearTo, RelYearFrom, RelYearExist

    if SearchRelYearFromInput.get() is not None and SearchRelYearToInput.get() is not None:
        RelYearExist = True
        RelYearTo = SearchRelYearToInput.get()
        RelYearFrom = SearchRelYearFromInput.get()
    else:
        RelYearExist = False

    MovieName = SearchTitleInput.get()
    SearchMovieDoc = LoadXML_SearchMovie(MovieName)
    ListBox_SearchMovie("title")

def LoadXML_SearchMovie(title):

    server = "openapi.naver.com"
    client_id = "iEV22cE2b1ZJnyGDYXtc"
    client_secret = "xJB_PnOFmw"
    text = urllib.parse.quote(title)

    conn = HTTPSConnection(server)

    if RelYearExist is False:
        conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1", None,
                     {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
    else:
        conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1&yearfrom=" + str(RelYearFrom) + "&yearto=" + str(RelYearTo), None,
                     {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})

    req = conn.getresponse()
    if int(req.status) == 200:
        naverdom = parseString(req.read())
        print(req.read().decode('utf-8'))
        return naverdom
    else:
        return None

def ListBox_SearchMovie(title):
    global SearchMovieDoc
    global ResultMovie

    ResultMovie.delete(0, END)

    itemList = SearchMovieDoc.getElementsByTagName('item')

    for movie in itemList:
        for attr in movie.childNodes:
            if attr.nodeName == title:
                if attr.hasChildNodes():
                    tmp = str(attr.firstChild.nodeValue)
                    tmp = tmp.replace('<b>', '')
                    tmp = tmp.replace('</b>', '')
                    ResultMovie.insert(END, tmp)

def Button_DetailMovie():
    global MovieList
    global DetailMovieLabel
    global ResultMovie
    global MovieJPG
    global titleStrLabel
    global subtitleStrLabel
    global directorLabel
    global actorLabel
    global userRatingLabel
    global ResultDic

    SearchList = ['title', 'link', 'image', 'subtitle', 'pubDate', 'director', 'actor', 'userRating']
    ResultDic = dict()
    count = 0
    flag = 0

    MovieName = ResultMovie.get(ResultMovie.curselection())
    DetailMovieDoc = LoadXML_SearchMovie(MovieName)

    itemList = DetailMovieDoc.getElementsByTagName('item')

    for item in itemList:
        for attr in item.childNodes:
            if attr.nodeName == "title":
                title = attr.firstChild.nodeValue
                title = title.replace("<b>", "")
                title = title.replace("</b>", "")
                if title == MovieName:
                    flag = 1
                    break
                else:
                    continue
        if flag == 1:
            break
        count += 1

    result = itemList[count]
    for attr in result.childNodes:
        for object in SearchList:
            if attr.nodeName == object:
                if attr.hasChildNodes():
                    ResultDic[object] = attr.firstChild.nodeValue
                else:
                    ResultDic[object] = "None"

    ResultDic["title"] = ResultDic["title"].replace("<b>", "")
    ResultDic["title"] = ResultDic["title"].replace("</b>", "")
    ResultDic["actor"] = ResultDic["actor"].replace("|", ", ")
    if ResultDic["actor"] != "None":
        ResultDic["actor"] = ResultDic["actor"][:-2]
    ResultDic["director"] = ResultDic["director"].replace("|", ", ")
    if ResultDic["director"] != "None":
        ResultDic["director"] = ResultDic["director"][:-2]


    titleStrLabel.configure(text="")
    subtitleStrLabel.configure(text="")
    userRatingLabel.configure(text="")
    directorLabel.configure(text="")
    actorLabel.configure(text="")
    MovieJPG.configure(image="")

    for i in ResultDic.keys():
        print(i, " : ", ResultDic[i])


    if ResultDic["image"] != "None":
        #print(ResultDic[i])
        with urllib.request.urlopen(ResultDic["image"]) as u:
            raw_data = u.read()
        image = Image.open(BytesIO(raw_data))
        image = image.resize((160, 208), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)

        MovieJPG = Label(MovieList, image=image)
        MovieJPG.place(x=820, y=150)

    titleStr = ResultDic["title"]
    pubDateStr = ResultDic["pubDate"]
    subtitleStr = ResultDic["subtitle"]
    subtitleStr = subtitleStr + ", " + pubDateStr
    directorStr = "감독 : " + ResultDic["director"]
    actorStr = "출연진 : " + ResultDic["actor"]
    userRatingStr = "네티즌 평점 : " + ResultDic["userRating"]

    #for i in range(1, len(actorStr) // 30 + 1):
    #    index = actorStr.find(',', i * 30)
    #    if index == -1:
    #        break
    #    else:
    #        actorStr = actorStr[:index] + '\n' + actorStr[index+2:]

    actorStr = arrangeStr.enterLine(actorStr)

    titleStrLabel = Label(MovieList, text=titleStr, justify=LEFT, font="나눔고딕 20 bold")
    titleStrLabel.place(x=330, y=150)

    # "subtitle, pubdate"로 출력됨.
    subtitleStrLabel = Label(MovieList, text=subtitleStr, justify=LEFT, font="나눔고딕 12")
    subtitleStrLabel.place(x=330, y=200)

    divLineLabel1 = Label(MovieList, text="――――――――――――――――――――――――――――――――――――――――――――――――", justify=LEFT,
                          font="나눔고딕 6", fg="gray")
    divLineLabel1.place(x=330, y=230)

    userRatingLabel = Label(MovieList, text=userRatingStr, justify=LEFT, font="나눔고딕 11 bold")
    userRatingLabel.place(x=330, y=255)

    divLineLabel1 = Label(MovieList, text="――――――――――――――――――――――――――――――――――――――――――――――――", justify=LEFT,
                          font="나눔고딕 6", fg="gray")
    divLineLabel1.place(x=330, y=290)

    directorLabel = Label(MovieList, text=directorStr, justify=LEFT, font="나눔고딕 10")
    directorLabel.place(x=330, y=310)

    actorLabel = Label(MovieList, text=actorStr, justify=LEFT, font="나눔고딕 10")
    actorLabel.place(x=330, y=340)

    EmailButton = Button(MovieList, text="이메일", command=Button_EmailMovie)
    EmailButton.place(x=930, y=450)

    LinkButton = Button(MovieList, text="네이버 영화", command=Button_LinkMovie)
    LinkButton.place(x=830, y=450)

    MovieList.mainloop()


def Button_LinkMovie():
    global ResultDic
    webbrowser.open_new(ResultDic["link"])


def Button_EmailMovie():
    global SendEmailEntry
    global Email

    Email = Tk()
    Email.title("Email")
    Email.geometry("200x80+950+400")

    SendEmailLabel = Label(Email, text="Email")
    SendEmailLabel.pack()
    SendEmailEntry = Entry(Email)
    SendEmailEntry.pack()
    SendEmailButton = Button(Email, text="전송", command=SendEmail)
    SendEmailButton.pack()

def SendEmail():
    global SendEmailEntry
    global ResultDic
    global Email

    host = "smtp.gmail.com"
    port = 587
    #htmlFileName = "logo.html"

    senderAddr = "kyh140149@gmail.com"
    receiveAddr = SendEmailEntry.get()

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = ResultDic["title"] + " 꼭 보세요!!!"
    msg['From'] = senderAddr
    msg['To'] = receiveAddr

    if ResultDic["image"] != None:
        with urllib.request.urlopen(ResultDic["image"]) as u:
            img_data = u.read()
        img = MIMEImage(img_data)
        msg.attach(img)

    text = ''
    text += "제목 : " + ResultDic["title"] + "\n"
    text += "부제목 : " + ResultDic["subtitle"] + "\n"
    text += "개봉년도 : " + ResultDic["pubDate"] + "\n"
    text += "평점 : " + ResultDic["userRating"] + "\n"
    text += "감독 : " + ResultDic["director"] + "\n"
    text += "배우 : " + ResultDic["actor"] + "\n"
    text += "링크 : " + ResultDic["link"] + "\n"
    text = MIMEText(text)
    msg.attach(text)

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, "dudgus12")
    s.sendmail(senderAddr, [receiveAddr], msg.as_string())
    s.close()

    Email.destroy()

# --------------------------------------------------------------------------------------

Tk_DayMovie()
#Tk_SearchMovie()