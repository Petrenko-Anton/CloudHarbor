city_list = ["Kиїв", "Харків","Дніпро", "Одеса","Донецьк", "Запоріжжя","Львів", "Миколаїв", "Луганськ", "Вінниця", "Сімферополь", "Херсон", "Полтава", "Чернігів",
"Черкаси", "Суми", "Житомир", "Хмельницький", "Кропивницький", "Рівне", "Чернівці", "Тернопіль", "Івано-Франківськ", "Луцьк", "Ужгород"]

$(document).ready(function(){
  
  // Обробка події вибору параметра
  $('#city-list').change(function(){
    var selectedCity = $(this).val();
  
    // Очистка блоку перед оновленням
    $('#weather-details').empty();

    if(city_list.includes(selectedCity)) {
      getWeather(selectedCity);
    } 
  });

  function getWeather(selectedCity) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var weatherDetails = JSON.parse(this.responseText);
            var weatherInfo = weatherDetails[selectedCity];
            var weatherHTML = `
                <p><b>температура</b>: <span>${weatherInfo.current.temperature}</span></p>
                <p><b>вологість: </b><span>${weatherInfo.current.humidity }</span></p>
                <p><b>тиск: </b><span>${weatherInfo.current.pressure}</span></p>
                <p><b>вітер: </b><span>${weatherInfo.current.wind_speed}</span></p>
                <p><b>хмарність: </b><span>${weatherInfo.current.cloudness}</span></p>
                <p><b>опади: </b><span>${weatherInfo.current.description}</span></p>
            `;
            document.getElementById('weather-details').innerHTML = weatherHTML;
        }
      };
      xhttp.open('GET', '/news/get_weather/?city=' + encodeURIComponent(selectedCity), true);
      xhttp.send();
  }
});