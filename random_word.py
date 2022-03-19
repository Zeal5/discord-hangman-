import requests
#api for random word

url = "https://random-words-api.vercel.app/word"


#function that choose value of kep/wprd pair
def word():
    r = requests.get("https://random-words-api.vercel.app/word")
    json_data = r.json()
    return(json_data[0]['word'])




randomword = word()




