from bs4 import BeautifulSoup
import requests
import pymysql

headers_user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (HTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def get_lotto_numbers(key_word):
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={key_word}%ED%9A%8C%20%EB%A1%9C%EB%98%90%EB%8B%B9%EC%B2%A8%EB%B2%88%ED%98%B8"
    req = requests.get(url, headers=headers_user)
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    win = soup.select(".winning_number")
    bonus = soup.select(".bonus_number")

    if win and bonus:
        winning_numbers = [num.strip() for num in win[0].text.split()]
        return winning_numbers, bonus[0].text.strip()
    else:
        return None

def result(purchased_numbers, winning_numbers, bonus_number):
    match_count = len(set(purchased_numbers) & set(winning_numbers))
    bonus_matched = bonus_number in purchased_numbers

    if match_count == 6:
        return "1등! 모든 번호가 일치합니다!"
    elif match_count == 5 and bonus_matched:
        return "2등! 5개 번호 및 보너스 번호가 일치합니다!"
    elif match_count == 5:
        return "3등! 5개 번호가 일치합니다!"
    elif match_count == 4:
        return "4등! 4개 번호가 일치합니다!"
    elif match_count == 3:
        return "5등! 3개 번호가 일치합니다!"
    else:
        return "아쉽게도 당첨되지 않았습니다."

def save(round_number, purchased_numbers, winning_numbers, bonus_number):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='aaaa',
        db='mydatabase',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lotto(round_number, purchased_numbers, winning_numbers, bonus_number) VALUES (%s, %s, %s, %s)",
                           (round_number, ', '.join(map(str, purchased_numbers)), ', '.join(map(str, winning_numbers)), bonus_number))
        connection.commit()
    finally:
        connection.close()

def main():
    key_word = input("로또 회차를 입력하세요: ")
    purchased_numbers = list(map(int, input("로또 번호 6개를 띄어쓰기로 구분하여 입력하세요: ").split()))

    winning_numbers, bonus_number = get_lotto_numbers(key_word)

    if winning_numbers:
        print(f"\n당첨 번호: {winning_numbers}, 보너스 번호: {bonus_number}")
        print(result(purchased_numbers, list(map(int, winning_numbers)), int(bonus_number)))

        save(key_word, purchased_numbers, winning_numbers, int(bonus_number))

    else:
        print("로또 회차를 찾을 수 없어요")

if __name__ == "__main__":
    main()