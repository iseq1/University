function openbox(id, link) {
  var allTabs = document.querySelectorAll(".tab_profile");
  var allContents = document.querySelectorAll(".tabs-content__profile");

  // Удаление класса active у всех ссылок
  allTabs.forEach(tab => {
    tab.classList.remove('active');
  });

  // Установка класса active для выбранной ссылки
  link.parentNode.classList.add('active');

  // Показывание выбранного содержимого, скрытие остальных
  allContents.forEach(content => {
    if (content.id === id) {
      content.style.display = 'block';
    } else {
      content.style.display = 'none';
    }
  });
}


function openshedulebox(id, link) {
  var allTabs = document.querySelectorAll(".tab_profile-bot");
  var allContents = document.querySelectorAll(".shedule-week__box");

  // Удаление класса active у всех ссылок
  allTabs.forEach(tab => {
    tab.classList.remove('active');
  });

  // Установка класса active для выбранной ссылки
  link.parentNode.classList.add('active');

  // Показывание выбранного содержимого, скрытие остальных
  allContents.forEach(content => {
    if (content.id === id) {
      content.style.display = 'block';
    } else {
      content.style.display = 'none';
    }
  });
}