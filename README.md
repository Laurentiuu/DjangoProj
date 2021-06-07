# DjangoProj
Am creat un proiec Django in care am creat serverul, am creat modelul cu componentele: airTemperature,pressure,humidity,precipitation,visibility,waterTemperature,
windDirection,windSpeed. Aceste date le-am luat din API de la coordonatele 38.7984 si 17.8081 de la data 1 ianuarie 2018. Am luat date pe 30 de zile(API-ul ia date
pentru 10 zile si am declarat 3 zile diferite(1 ianuarie, 11 ianuarie si 21 ianuarie 2018)). Am creat un DataFrame folosind pandas cu aceste date, le-am impariti in
date de train si de test si am facut preziceri folosind LinearRegresion. Afisez prezicerile pentru airTemperature, visibility si windDirection in consola.
