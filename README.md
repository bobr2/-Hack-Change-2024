# -Hack-Change-2024
Cтруктура проекта:
Фронтенд - Бэкенд
              | - по запросу обращается к моделе на python
Для работы прорграммы нужно установить библеотеки последних версий

Описание модели:
1) Kmeans с тремя кластерами, соответствующими каждому типу подписанию
Мы написали ансамбль с kmeans и деревом, написанным нами для дополнительного корректирования предсказания модели
Обучали модель на синтетических данных, посмотрев на хитмап корреляции признаков, выбрали основными следующие параметры: Кол-во организаций,  
Для нормализации данных использовали алгоритм TSNE и Standart Scaler
Метрику выбрали - Silhouette

Нужно запускать проект в IntelliJ IDEA Ultimate Edition с конфигурацией Spring Boot  
Файл нужно загрузить в папку( \src\main\java\com\suir\suir) и прописать путь в бэкнде до этого JSON файла следую инструкциям в самом коде
ссылка на демо : 
