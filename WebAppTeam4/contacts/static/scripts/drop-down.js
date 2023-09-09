city_list = ["Kиїв", "Харків","Дніпро", "Одеса","Донецьк", "Запоріжжя","Львів", "Миколаїв", "Луганськ", "Вінниця", "Сімферополь", "Херсон", "Полтава", "Чернігів",
"Черкаси", "Суми", "Житомир", "Хмельницький", "Кропивницький", "Рівне", "Чернівці", "Тернопіль", "Івано-Франківськ", "Луцьк", "Ужгород"]
  

$(document).ready(function(){
  // Обробка події вибору параметра
  $('#city-list').change(function(){
    var selectedParameter = $(this).val();

    // Очистка таблиці перед оновленням
    $('#weather-details').empty();

    // Додавання нових рядків з відповідними даними
    if(city_list.includes(selectedParameter)) {
      city = selectedParameter
      $('#weather-details').append(city, ' дані: <p><b>температура: </b><span>{{ weather_info.current.temperature }}</span></p> \
      <p><b>вологість: </b><span>{{ weather_info.current.humidity }}</span></p> \
      <p><b>тиск: </b><span>{{ weather_info.current.pressure}}</span></p> \
      <p><b>вітер: </b><span>{{ weather_info.current.wind_speed}}</span></p> \
      <p><b>хмарність: </b><span>{{ weather_info.current.cloudness}}</span></p> \
      <p><b>опади: </b><span>{{ weather_info.current.description}}</span></p>');
      
      // Додайте інші рядки та дані для інших параметрів
    } 
  });
});