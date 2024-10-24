import requests
from telegram import Bot
from telegram.ext import Updater
from config import API_KEY, TELEGRAM_TOKEN, GROUP_CHAT_ID, RAPIDAPI_HOST

bot = Bot(token=TELEGRAM_TOKEN)

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST
}

predicted_matches = {}

def get_live_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        if 'response' not in data:
            print(f"Error: API response does not contain 'response' key. Full response: {data}")
            return None
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching live matches: {e}")
        return None

def analyze_live_match(match):
    minute = match['fixture']['status']['elapsed']
    home_team = match['teams']['home']['name']
    away_team = match['teams']['away']['name']
    home_score = match['goals']['home']
    away_score = match['goals']['away']
    total_goals = home_score + away_score
    confidence_level = "düşük"
    half_time_prediction = ""
    full_time_prediction = ""

    # İlk yarı tahminleri
    if minute < 45:
        if total_goals >= 2:
            half_time_prediction = "İY 3,5 ÜST (İlk yarı en az 3 gol olur)"
            confidence_level = "yüksek"
        elif total_goals == 1:
            if home_score == 1 and away_score == 0:
                half_time_prediction = f"İY {home_team} kazanır (Ev sahibi önde)"
                confidence_level = "yüksek"
            elif home_score == 0 and away_score == 1:
                half_time_prediction = f"İY {away_team} kazanır (Misafir önde)"
                confidence_level = "yüksek"
            elif home_score == 1 and away_score == 1:
                half_time_prediction = "İY 0,5 ÜST (Bir gol olabilir)"
                confidence_level = "orta"
            else:
                half_time_prediction = "İY 0,5 ALT (Gol olmayabilir)"
                confidence_level = "orta"
        elif total_goals == 0:
            half_time_prediction = "İY 0,5 ALT (Gol olmayabilir)"
            confidence_level = "yüksek"

    # Tüm maç tahminleri
    if minute >= 45:
        if total_goals >= 4:
            full_time_prediction = "MS 5,5 ÜST (Maçta en az 6 gol olur)"
            confidence_level = "yüksek"
        elif total_goals == 3:
            full_time_prediction = "MS 4,5 ÜST (Maçta en az 5 gol olur)"
            confidence_level = "yüksek"
        elif total_goals == 2:
            if home_score == away_score:
                full_time_prediction = "MS 1,5 ALT (Beraberlik)"
                confidence_level = "orta"
            else:
                full_time_prediction = "MS 1,5 ÜST (En az 2 gol olur)"
                confidence_level = "orta"
        elif total_goals == 1:
            if home_score > away_score:
                full_time_prediction = f"{home_team} kazanır (Ev sahibi galip)"
                confidence_level = "yüksek"
            elif away_score > home_score:
                full_time_prediction = f"{away_team} kazanır (Misafir galip)"
                confidence_level = "yüksek"
            else:
                full_time_prediction = "MS 0,5 ALT (Gol olmayabilir)"
                confidence_level = "yüksek"

    return half_time_prediction, full_time_prediction, home_team, away_team, home_score, away_score, minute, confidence_level

def check_prediction_outcome(match):
    fixture_id = match['fixture']['id']
    if fixture_id in predicted_matches:
        home_score = match['goals']['home']
        away_score = match['goals']['away']
        total_goals = home_score + away_score
        predicted_half_time = predicted_matches[fixture_id]['half_time_prediction']
        predicted_full_time = predicted_matches[fixture_id]['full_time_prediction']

        # Yarı zaman tahmin kontrolü
        if predicted_half_time == "3.5 ÜST" and total_goals >= 2:
            return True
        if predicted_half_time == "0.5 ALT" and total_goals == 0:
            return True

        # Maç sonu tahmin kontrolü
        if predicted_full_time == "5.5 ÜST" and total_goals >= 4:
            return True
        if predicted_full_time == "4.5 ÜST" and total_goals >= 3:
            return True
        if predicted_full_time == "3.5 ÜST" and total_goals >= 2:
            return True
        if predicted_full_time.startswith("KG") and home_score > 0 and away_score > 0:
            return True
        if predicted_full_time == "KG" and total_goals == 0:
            return True
    return False

def send_predictions(context):
    live_matches = get_live_matches()
    if live_matches is None:
        print("Şu anda canlı oynanan maç yok.")
        return

    predictions_made = 0  # Tahmin sayısını takip etmek için
    max_predictions = 3  # Maksimum 3 maç tahmini yap

    for match in live_matches['response']:
        if predictions_made >= max_predictions:
            break

        fixture_id = match['fixture']['id']
        minute = match['fixture']['status']['elapsed']

        # Eğer maç için zaten tahmin yapıldıysa, tekrar tahmin yapma
        if fixture_id in predicted_matches:
            continue

        # 8 değer döndüğü için tüm değerleri alıyoruz
        half_time_prediction, full_time_prediction, home_team, away_team, home_score, away_score, minute, confidence_level = analyze_live_match(match)

        if half_time_prediction and minute < 45:
            message = (f"⚽ {home_team} - {away_team}\n"
                       f"Dk {minute}\n"
                       f"Şimdiki skor {home_score} - {away_score}\n"
                       f"İlk Yarı Tahmin: {half_time_prediction}\n"
                       f"Güven Seviyesi: {confidence_level.upper()}")
            bot.send_message(chat_id=GROUP_CHAT_ID, text=message, timeout=300)

            # Tahminleri kaydet
            predicted_matches[fixture_id] = {'half_time_prediction': half_time_prediction, 'full_time_prediction': full_time_prediction}
            predictions_made += 1

        if full_time_prediction and minute >= 45:
            message = (f"⚽ {home_team} - {away_team}\n"
                       f"Dk {minute}\n"
                       f"Şimdiki skor {home_score} - {away_score}\n"
                       f"Maç Sonu Tahmin: {full_time_prediction}\n"
                       f"Güven Seviyesi: {confidence_level.upper()}")
            bot.send_message(chat_id=GROUP_CHAT_ID, text=message, timeout=300)

        # Maç 90. dakikayı geçtiyse tahmin sonucunu kontrol et
        if minute >= 90:
            outcome_correct = check_prediction_outcome(match)
            if outcome_correct:
                bot.send_message(chat_id=GROUP_CHAT_ID, text=f"✅ Tahmin tuttu! {home_team} - {away_team}")
            else:
                bot.send_message(chat_id=GROUP_CHAT_ID, text=f"❌ Tahmin tutmadı! {home_team} - {away_team}")

            # Tahmin edilen maçı listeden çıkar
            if fixture_id in predicted_matches:
                predicted_matches.pop(fixture_id)


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    job_queue = updater.job_queue

    # 10 dakikada bir tahmin gönder
    job_queue.run_repeating(send_predictions, interval=600, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
