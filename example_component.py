from simple_slack_bot.simple_slack_bot import SimpleSlackBot
import random
import requests
import re
import pyjosa
import time
import threading
from bs4 import BeautifulSoup

simple_slack_bot = SimpleSlackBot(debug=True)


@simple_slack_bot.register("hello")
def hello_callback(request):
    request.write("너하-! 난 너굴맨이라구 필요한게 있으면 불러달라구:racoon_man:")


def manage_cnt_after_time(user, sec):
    time.sleep(sec)
    if user_call_dict[user]['request_cnt'] > 0:
        user_call_dict[user]['request_cnt'] -= 1


# 타이핑 할 때마다 이벤트 발생
# @simple_slack_bot.register("user_typing")
# def user_typing_callback(request):
#     user_id = simple_slack_bot.helper_user_id_to_user_name(request._slack_event.event['user'])
#     request.write(f"I see you typing {user_id}")
#

# global var
user_list = simple_slack_bot.helper_get_user_ids()
user_dict = {}
user_call_dict = {}

for user in user_list:
    user_dict[user] = 0
    user_call_dict[user] = {
        'last_order': '',
        'request_cnt': 0
    }


@simple_slack_bot.register("message")
def racoon_message(request):
    count = 0
    if request.channel == 'CLWDPD2KY':
        if random.randrange(1, 50) > 45 and request.user != 'UECK50ENB' and user_dict[request.user] < 0:
            request.reply(f'고문 해버린다구,@{simple_slack_bot.helper_user_id_to_user_name(request.user)}')

    if request.message:
        recv_msg = request.message
        if recv_msg.find("너굴맨") != -1:

            request_cnt = manage_request_cnt(request.user)
            if request_cnt > 10:
                threading.Thread(target=manage_cnt_after_time, args=(request.user, 600))
                return
            elif request_cnt == 10:
                threading.Thread(target=manage_cnt_after_time, args=(request.user, 300))
                return request.write(f'@{simple_slack_bot.helper_user_id_to_user_name(request.user)} 괴롭힌다 너굴맨! 너굴맨 무시한다 당신!')
            elif request_cnt >= 5:
                threading.Thread(target=manage_cnt_after_time, args=(request.user, 120))
                return request.write(f'바쁜데 계속 말걸지말라구 @{simple_slack_bot.helper_user_id_to_user_name(request.user)}')

            if recv_msg.find("잘못") != -1 or recv_msg.find("미안") != -1:
                if random.choice([True, False]):
                    return request.write(plus_like_percent(request.user))
                else:
                    return request.write(minus_like_percent(request.user, 1))

            if (recv_msg.find("호감도") != -1 or recv_msg.find("친밀도") != -1) and recv_msg.find("보여") != -1:
                return request.write(get_like_percent(request.user))

            if user_dict.get(request.user) is not None:
                if user_dict[request.user] >= -14:
                    pass
                else:
                    if random.choice([True, False]):
                        return request.write('흥이라구')
                    else:
                        return request.write('싹싹빌라구')

            if recv_msg.find("어디") != -1:
                count += 1
                return request.write(
                    f'너굴맨은 #{simple_slack_bot.helper_channel_id_to_channel_name(request.channel)}에 있다구')

            if recv_msg.find("난") != -1 and recv_msg.find("누구") != -1:
                count += 1
                return request.write(f'@{simple_slack_bot.helper_user_id_to_user_name(request.user)} 라구')

            if recv_msg.find("될까") != -1 \
                    or recv_msg.find("할까") != -1 \
                    or recv_msg.find("있을까") != -1 \
                    or recv_msg.find("갈까") != -1 \
                    or recv_msg.find("살까") != -1:
                if random.choice([True, False]):
                    rst = '응이라구'
                else:
                    rst = "아니라구"

                count += 1
                return request.write(rst)

            if recv_msg.find("미세먼지") != -1:
                count += 1
                return request.write(mise_switch())

            if (recv_msg.find("뭐") != -1 and recv_msg.find("먹을까") != -1) \
                    or recv_msg.find("점심추천") != -1 \
                    or recv_msg.find("뭐먹지") != -1 \
                    or recv_msg.find("배고파") != -1:
                lunch_list = ['와규', '설렁탕', '쌈밥', '김치찌개', '예윤', '이자까야', '플레이티드', '등갈비 찜', '쌀국수', '부대찌개']
                count += 1
                return request.write(random.choice(lunch_list) + ' 어떠냐구')

            if recv_msg.find("처치") != -1:
                count += 1
                if recv_msg.find("사악한") != -1:
                    p = re.compile('사악한 [\u3131-\u3163\uac00-\ud7a3A-Za-z0-9]+ 처치')
                    if len(p.findall(recv_msg)) > 0:
                        re_result = p.findall(recv_msg)[0] \
                            .replace('처치', '') \
                            .replace('사악한', '') \
                            .replace('을', '') \
                            .replace('를', '')
                        if re_result.find('너굴맨') != -1:
                            return request.write(f'너굴맨은 처치할수없다구 널 처치할거라구')
                        elif re_result.find('세하') != -1:
                            return request.write(f'주인님을 처치할수 없다구')
                        else:
                            msg = u'사악한' + re_result + '(은)는 이 너굴맨이 처치했으니 안심하라구!'
                            return request.write(pyjosa.replace_josa(msg))
                    else:
                        return request.write(f'처치해버린다구, @{simple_slack_bot.helper_user_id_to_user_name(request.user)}')
                else:
                    if random.choice([True, False]):
                        return request.write("이 너굴맨이 처치했으니 안심하라구!:racoon_man:")
                    else:
                        return request.write("너굴맨 휴무라구 알아서 하라구")

            if recv_msg.find("도와줘요") != -1:
                count += 1
                msg = '`너굴맨 점심추천해줘, 너굴맨 처치해줘, 너굴맨 미세먼지, 너굴맨 날씨` 를 도와줄수 있다구!'
                return request.write(msg)

            if recv_msg.find("안녕") != -1 and request.user is not None:
                if user_dict[request.user] > 5:
                    user_dict[request.user] += 1
                    return request.write(
                        f"반갑다구 @{simple_slack_bot.helper_user_id_to_user_name(request.user)}:racoon_man:")

                else:
                    user_dict[request.user] += 1
                    return request.write("너-하 라구!")

            if recv_msg.find("안될까") != -1:
                msg = '싫다구'
                count += 1
                return request.write(msg)

            if (recv_msg.find("오늘") != -1
                or recv_msg.find("현재") != -1
                or recv_msg.find("지금") != -1) \
                    and recv_msg.find("날씨") != -1:
                count += 1
                soup = weather_init_soup()
                request.write(get_thermal(soup))
                return request.write(get_weather(soup))

            if recv_msg.find("게임추천") != -1 or recv_msg.find("궨트") != -1:
                count += 1
                if random.choice([True, False]):
                    return request.write('궨트 츄라이해보라구 갓겜이라구:racoon_man:')
                else:
                    return request.write("엥 그거 갓겜아니냐구 갓겜을 쌈에싸서 드셔보시라구:racoon_man:")

            if recv_msg.find("히오스") != -1:
                count += 1
                return request.write('시공의폭풍이라구')

            if recv_msg.find("돌겜") != -1 or recv_msg.find("하스스톤") != -1 \
                    or recv_msg.find("하스") != -1:
                count += 1
                return request.write('돌겜은 너나 하라구')

            if recv_msg.find("지금") != -1 and recv_msg.find("비와") != -1:
                count += 1
                if get_weather(weather_init_soup()).find('비') != -1:
                    return request.write('비가온다구!!')
                else:
                    return request.write('안온다구')

            if recv_msg.find("졸려") != -1 or recv_msg.find("졸립다") != -1:
                count += 1
                if random.choice([True, False]):
                    return request.write('너굴맨도 졸립다구')
                else:
                    return request.write('너굴맨 집가고 싶다구')

            if recv_msg.find("댓글") != -1:
                count += 1
                msg = recv_msg.replace("댓글", "").replace("너굴맨", "")
                return request.reply(msg)

            if recv_msg.find("칭찬해") != -1:
                count += 1
                user_dict[request.user] += 1
                return request.write('잘했다구')

            if count > 1:
                request.write(minus_like_percent(request.user, count))


def manage_request_cnt(user_id):
    return_cnt = 0
    for u in user_list:
        if u == user_id:
            user_call_dict[u]['request_cnt'] += 1
            return_cnt = user_call_dict[u]['request_cnt']
        elif user_call_dict[u]['request_cnt'] != 0:
            user_call_dict[u]['request_cnt'] -= 1
    return return_cnt


def minus_like_percent(user_id, num):
    user_dict[user_id] -= num
    return f'괴롭히지 말라구, @{simple_slack_bot.helper_user_id_to_user_name(user_id)}'


def plus_like_percent(user_id):
    user_dict[user_id] += 1
    return f'잘하라구, @{simple_slack_bot.helper_user_id_to_user_name(user_id)}'


def get_like_percent(user_id):
    return f'{user_dict[user_id]} 라구'


def weather_init_soup():
    weather_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EC%84%B1%EB%8F%99%EA%B5%AC+%EB%82%A0%EC%94%A8'
    response = requests.get(weather_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_thermal(soup):
    now_ther = soup.find('span', {'class', 'todaytemp'}).text
    min_ther = soup.find('span', {'class', 'min'}).find('span', {'class', 'num'}).text
    max_ther = soup.find('span', {'class', 'max'}).find('span', {'class', 'num'}).text
    msg = f'현재 기온은 *{now_ther}*, 최저:{min_ther} 최고:{max_ther} ! '
    return msg


def get_weather(soup):
    now_weather = soup.find('span', {'class', 'ico_state2'}).text
    if now_weather == '비':
        msg = '지금은 비가온다구 *우산*을 챙겨달라구 :umbrella:'
    else:
        msg = f'지금은 {now_weather}이라구 :racoon_man:'
    return msg


def mise_switch():
    result = []
    mise_status = ''
    chomise_status = ''

    for query in ('성동구 미세먼지', '성동구 초미세먼지'):
        response = requests.get(
            url='https://search.naver.com/search.naver',
            params={'sm': 'tab_hty.top', 'where': 'nexearch', 'query': query, 'oquery': '성수동'}
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        get_data = soup.find('em', {'class': 'main_figure'})
        result.append(int(get_data.text))

    if len(result) == 2:
        if result[0] <= 30:
            mise_status = '좋음'
        elif result[0] <= 80:
            mise_status = '보통'
        elif result[0] <= 150:
            mise_status = '나쁨'
        else:
            mise_status = '매우나쁨'

        if result[1] <= 15:
            chomise_status = '좋음'
        elif result[1] <= 35:
            chomise_status = '보통'
        elif result[1] <= 75:
            chomise_status = '나쁨'
        else:
            chomise_status = '매우나쁨'
    return f"성동구 미세먼지 {mise_status} {result[0]}, 초미세먼지 {chomise_status} {result[1]} 라구"


def main():
    simple_slack_bot.start()


if __name__ == "__main__":
    main()
