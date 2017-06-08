import xml.etree.ElementTree as et
import requests
import config

slack_url = "https://%s.slack.com/api/chat.postMessage" % config.target_team

def post_view(views):

    params = {
        "token": config.key,
        "channel": config.target_channel,
        "icon_emoji": ":%s:" % config.icon,
        "text": ""
    }
    params["text"] = """キョウノ ケモノふれんず1話 ノ サイセイスウハ %d回 ダヨ
http://www.nicovideo.jp/watch/%s
""" % (views, config.target_nicovideo_id)
    return requests.post(slack_url, params)

def join_channel():
    print(config.target_channel)
    params = {
        "token": config.key,
        "name": config.target_channel,
    }
    return requests.post(slack_url, params)

def main():
    nico_res = requests.get("http://ext.nicovideo.jp/api/getthumbinfo/%s" % (config.target_nicovideo_id))
    xml_root = et.fromstring(nico_res.text)
    views = int(xml_root.find(".//view_counter").text)

    res = post_view(views)
    if not res.json()["ok"]:
        j = join_channel()
        print(j.text)
        res = post_view(views)
    print(res.text)
if __name__ == '__main__':
    main()
