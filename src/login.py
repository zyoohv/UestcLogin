import urllib.request
import http.cookiejar
import urllib.parse
import json
import os


def installOpener():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)


def loginWeb():
    with open('./configure.json', 'r') as f:
        usrInfo = json.load(f)

    print('log in attempt: ', usrInfo['username'], '...')

    values = {
        'action': 'login',
        'username': str(usrInfo['username']) + '@uestc',
        'password': usrInfo['password'],
        'ac_id': '1',
        'user_ip': '',
        'nas_ip': '',
        'user_mac': '',
        'save_me': '0',
        'ajax': '1'
    }
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
    }

    url = 'http://192.168.9.8/include/auth_action.php'

    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()

    # print(the_page)

    print('linking...')

    if the_page[0:8] == b'login_ok':
        print('sucess！')
        input('\n\n---------------------------\nclose this window please...')
        return

    print(the_page.decode(encoding='utf-8'))

    input('\n\n---------------------------\nclose this window please...')


def main():
    installOpener()
    loginWeb()

if __name__ == '__main__':
    main()
