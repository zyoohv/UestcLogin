import urllib.request, http.cookiejar, urllib.parse
import json
import os

def installOpener():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)


def base64encode(s):
    base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    out = ''
    i = 0
    l = len(s)
    while(i < l):
        i += 1
        c1 = ord(s[i - 1]) & 0xff
        if i == l:
            out += base64EncodeChars[c1 >> 2]
            out += base64EncodeChars[(c1 & 0x3) << 4]
            out += "=="
            break
        i += 1
        c2 = ord(s[i - 1])
        if i == l:
            out += base64EncodeChars[c1 >> 2]
            out += base64EncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
            out += base64EncodeChars[(c2 & 0xF) << 2]
            out += "="
            break
        i += 1
        c3 = ord(s[i - 1])
        out += base64EncodeChars[c1 >> 2]
        out += base64EncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
        out += base64EncodeChars[((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6)]
        out += base64EncodeChars[c3 & 0x3F]
    return '{B}' + out

def loginWeb():
    with open('./configure.json', 'r') as f:
        usrInfo = json.load(f)

    print('尝试登陆账号: ', usrInfo['username'], '...')
    
    values = {
        'action':'login',
        'username':str(usrInfo['username']),
        'password':base64encode(usrInfo['password']),
        'ac_id':'1',
        'user_ip':'',
        'nas_ip':'',
        'user_mac':'',
        'save_me':'0',
        'ajax':'1'
        }
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
        }

    url = 'http://192.168.9.8/include/auth_action.php'

    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()

    #print(the_page)

    print('尝试连接完成，检测连接状态...')

    if the_page[0:8] == b'login_ok':
        print('登陆成功！')
        input('\n\n---------------------------\n按任意字符关闭此窗口...')
        return 

    print(the_page.decode(encoding='utf-8'))

    input('\n\n---------------------------\n按任意字符关闭此窗口...')

def main():
    installOpener()
    loginWeb()

if __name__ == '__main__':
    main()
