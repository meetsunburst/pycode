import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua=UserAgent()

# page最多为201
def get_one_page(i):
    url = f"http://ditu.92cha.com/dizhen.php?page={i}&dizhen_ly=china&dizhen_zjs=1&dizhen_zje=10" \
          "&dizhen_riqis=2001-01-01&dizhen_riqie=2021-11-17"

    header = {'User-Agent': ua.random}
    try:
        response = requests.get(url=url, headers=header)
        print(f"爬取第{i}页成功")
        return response.text
    except Exception as e:
        print(e.args[0])
        print(f"爬取第{i}页失败")

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.findAll('tr')
    ulist = []
    for tr in trs:
        tmp = []
        flag = False
        for td in tr:
            tmp.append(td.string.strip())
        ulist.append(tmp)
    ulist.pop(0)
    return ulist

def save_contents(ulist):
    file_path = r"C:\Users\dragon\Desktop\res.csv"

    with open(file=file_path, mode='w', encoding='utf-8') as file_out:
        file_out.write('发震时间,震级,经度,维度,深度（km）,位置' + "\n")
        for page in ulist:
            for tmp in page:
                file_out.write(tmp[1] + "," + tmp[3] + "," + tmp[5] + "," + tmp[7] + "," + tmp[9] + "," + tmp[11] + "\n")

def main():
    ulist = []
    for i in range(1, 5):
        html = get_one_page(i)
        res = parse_one_page(html)
        ulist.append(res)
    save_contents(ulist)


if __name__ == '__main__':
    main()
