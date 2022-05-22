import requests
import re
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'cookie':"buvid3=F2BFCBE6-FC72-38C1-0C24-8714A500900E00988infoc; i-wanna-go-back=-1; _uuid=9531035A6-8194-10426-FAE3-E96514BFFD9D01787infoc; buvid4=91C6026D-FDED-495D-1D29-6D7177B4CCB102020-022041421-boF00P1fYfj9pcRo1zaFEQ==; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO7316499790299654; nostalgia_conf=-1; blackside_state=0; rpdid=|(u))|YYkJm~0J'uYRmm~mu)l; sid=jwqv5rpb; DedeUserID=51715952; DedeUserID__ckMd5=b9e834180e079b24; SESSDATA=dbc97487,1665927473,e5826*41; bili_jct=27273c6420d5d8a8753a919e0727e49a; b_ut=5; CURRENT_QUALITY=80; hit-dyn-v2=1; fingerprint=2478a081cca1483d28605211107c3a50; buvid_fp=2478a081cca1483d28605211107c3a50; b_lsid=E316179B_180C2AD977E; innersign=1; CURRENT_FNVAL=4048; bp_video_offset_51715952=660100795108163600; PVID=9",
}
bv2av_api = 'https://api.bilibili.com/x/web-interface/view'
content_api = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&type=1&mode=3&plat=1'


def bv2av(bv:str)->str:
    response = requests.get(url=bv2av_api,params={'bvid':bv},headers=headers)
    av = str(response.json()['data']['aid'])
    return av

def scrape_url(url:str)->dict:
    bv = url.split('/')[-1]
    av = bv2av(bv)
    pattern = re.compile(r'{.*}')

    params={'jsonp':'jsonp','type':1,'oid':av,'mode':3,'plat':1}
    headers['referer'] = url
    next = 0

    with open('text','a+',encoding='utf-8') as file:
        while True:
            params['next'] = next
            response = requests.get(url=content_api,params=params,headers=headers)
            json_text = pattern.search(response.text).group(0)
            is_end = json.loads(json_text)['data']['cursor']['is_end']
            if is_end:
                break
            replies_info = json.loads(json_text)['data']['replies']
            res = []
            for i in replies_info:
                res.append(i['content']['message'])
            json.dump(res,file,indent=2,ensure_ascii=False)
            if next!=0:
                next+=1
            else:
                next+=2
    

if __name__ == '__main__':
    scrape_url('https://www.bilibili.com/video/BV1PZ4y1P7WR')
