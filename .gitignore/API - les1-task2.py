import requests, json
header = requests.get('https://home.openweathermap.org/users/sign_in', headers={'Autorization':'Basic b2RpbWFyaWtAZ21haWwuY29tOjEyMzQ1Njc4OQ=='})
print(header.headers)
print(header.text)