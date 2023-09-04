from django.shortcuts import render

# Create your views here.

def index(request):
    title_for_test = "ЗСУ отримали нові можливості для наступу на Півдні"
    description_for_test = "Завдяки прориву першої лінії оборони росіян на Запорізькому напрямку у ЗСУ з’явилася можливість маневрувати технікою та військами під час наступу на другу лінію оборони ворога. Про це розповів речник об’єднаного пресцентру Сил оборони Таврійського напрямку Олександр Штупун."
    link_for_test = "https://real-vin.com/zsu-otrimali-novi-mozhlivosti-dlja-nastupu-na-pivdni"
    img_for_test = "https://real-vin.com/wp-content/uploads/2023/09/vsu-3-605x382.jpg"
    news = [{'title': title_for_test, 'description': description_for_test, 'link': link_for_test, 'img': img_for_test}]
    return render(request, 'news/news.html', {'news': news})

def currency(request):
    currency_courses = [{'USD': {'purchase': 37.38, 'sale': 38.10, 'nbu': 36.56}}, {'EUR': {'purchase': 40.67, 'sale': 41.61, 'nbu': 39.73}}, {'PLN': {'purchase': 8.81, 'sale': 9.35, 'nbu': 8.89}}]
    return render(request, 'news/news.html', {'currency_list': currency_courses})