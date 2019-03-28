#!进入到登录界面，以获取登录需要的data----此次获取登录信息后，采用带着登录信息访问数据指定网页进行爬取
from bs4 import BeautifulSoup
import requests
from PIL import Image
import pytesseract,os

session = requests.Session()    #记录登录信息，session对象
logined_flag=0  #记录是否登录成功的标志
#访问不同页面，设定不同的访问头信息
logoinout_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer':'http://www.klha.net/User.do?method=toApplition'
}
authcode_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer':'http://www.klha.net/User.do?method=loginout'
}
login_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer':'http://www.klha.net/User.do?method=toApplition'
}

username='jiejiaotech'  #登录需要的信息，通过fiddler获取的
password='klha123456'
authcode=''
button=''

def get_login_data():
    global username, password, authcode, button #定义使用全局变量
    login_url = 'http://www.klha.net/User.do?method=loginout'  # 登录页面
    login_rs = session.get(login_url,headers=logoinout_headers)  # 获取response
    login_rs.encoding = 'utf-8'  # 指定encoding
    login_html = login_rs.text  # 获取登录页面源码
    # print(login_html)          #打印输出源码
    bs = BeautifulSoup(login_html, 'html.parser')  # 通过bs解析html源码
    '''为了获取登录所需的验证码，需要从原网址爬取验证码图片的地址，获取图片后在解析其验证码'''
    image_tag = bs.find_all('img')  # 通过看源代码发现，只有一个img tag   ###注意此时为list对象，元素才是tag对象
    # print(image_tag)
    image_src = image_tag[0].get('src') #从list中取出img tag，然后获取其src属性
    # print(image_src)
    base_url = r'http://www.klha.net'
    image_url = base_url + image_src    #通过拼接，获取完整的image地址
    #print(image_url)
    authcode = get_authcode(image_url)  # 调用get_authcode方法，获取验证码
    #######################################################################根据fiddler，登录信息还需要button
    button_tag=bs.select("input[class='wlwbtn1']")    #获取button的tag obj，通过css选择器
    button=button_tag[0].get('value')   #list下获取tag obj，从而获取指定value
    login_data = {
        'loginname': username,
        'password': password,
        'code': authcode,
        'button': button
    }
    return login_data

# def get_authcode(image_url):    #manual
#     response=session.get(image_url,headers=authcode_header) #访问验证码地址
#     #print(response.content)
#     with open(r'F:\PYTHON\projects\klha\authcode.png', 'wb') as f:    #打开文件地址
#         f.write(response.content)   #以二进制的方式保存图片
#         f.flush()
#         f.close()
#     authcode = input('input captcha:')  #输入图片验证码
#     return authcode #返回输入的验证码

def get_authcode(image_url): #自动获取验证码,返回验证码的字符串
    response = session.get(image_url, headers=authcode_header)  # 访问验证码地址
    # with open(r'/tmp/pycharm_project_101/authcode.jpg', 'wb') as f:  # 打开文件地址，将图片进行保存
    with open(os.path.join(os.getcwd(),'authcode.jpg'), 'wb') as f:
        f.write(response.content)  # 以二进制的方式保存图片
        f.flush()
        f.close()
    img = Image.open(os.path.join(os.getcwd(),'authcode.jpg'))  #读取图片
    gray = img.convert('L') #转换成灰度图
    # gray.show()
    #  setup a converting table with constant threshold
    threshold = 55  #设定阈值
    pixels = []
    for i in range(256):    #遍历整个图片数组，通过阈值将图片置0或置1，从而实现二值化
        if i < threshold:
            pixels.append(0)
        else:
            pixels.append(1)
    #  convert to binary image by the table
    binary = gray.point(pixels, '1')    #获取二值化的图像
    code_image_crop = binary.crop((4, 2, 58, 18)).resize((120, 60)) #根据图片的大小，做调整从而去除不必要的边框等干扰；可以根据实际图片进行选择是否需要
    # code_image_crop.show()
    str = pytesseract.image_to_string(code_image_crop)  #获取图片中的验证码，返回为str
    #print(str)
    # if str is None:
    #     print('failed to process !')
    #     # img.show()
    # else:
    #     print('the code is:', str)
    return str

def get_login():    #通过fiddler 查看登录需要的信息，并进行保存，从而在请求登录地址的时候，传送对应的参数即可
    global logined_flag
    data=get_login_data()   #调用该方法，获取登录需要的信息，为一个dict
    #login_url='http://www.klha.net/User.do?method=toApplition'  # 登录页面
    login_url_post='http://www.klha.net/User.do?method=login'   #通过fiddler获取其post时的url
    reponse = session.post(login_url_post, data=data, headers=login_header)   #通过post请求登录，并传输对应数据
    logined_html=reponse.text   #登录后的界面
    logined_bs = BeautifulSoup(logined_html, 'html.parser')  # 通过bs解析html源码
    #print(logined_html)
    logined_text=logined_bs.get_text()
    if '退出登录' in logined_text:  #通过登录后界面中的一个文本信息，确定是否登录成功
        # print('Logined sucessfully!!!')
        logined_flag = 1    #如果成功，标志位置1
        return logined_html
    else:
        # print('Failed to login in!!!')
        logined_flag = 0    #如果失败，标志位置0
    return None     #将第一层登录的界面返回，从而方便后续跳转等操作

def login_to_logined():
    global logined_flag,session
    while True:
        logined_html = get_login()
        if logined_flag == 0:
            print('Try again!!!')
        else:
            print('Logined !!!')
            # print(logined_html)
            logined_flag = 0
            return session

if __name__ == '__main__':
    login_to_logined()
