
function openbox(id) {
  var allTabs = document.querySelectorAll(".tabs__item a");
  var allContents = document.querySelectorAll(".tabs-content");
  var allTtitle = document.querySelectorAll(".espresso-title");
  var allLists = document.querySelectorAll(".coffe-water-ratio");

  // Удаление класса active у всех ссылок
  allTabs.forEach(tab => {
    tab.classList.remove('active');
    if (tab.getAttribute('href').slice(1) === id) {
      tab.classList.add('active');
    }
  });

  // Показывание выбранного содержимого, скрытие остальных
  for (var i = 0; i < allContents.length; i++) {
    if (allContents[i].id == id) {
      if (allContents[i].style.display !== 'block') {
        allContents[i].style.display = 'block';
      }
    } else {
      allContents[i].style.display = 'none';
    }
  }

  for (var i = 0; i < allTtitle.length; i++) {
    if (allTtitle[i].id == id) {
      if (allTtitle[i].style.display !== 'block') {
        allTtitle[i].style.display = 'block';
      }
    } else {
      allTtitle[i].style.display = 'none';
    }
  }

  for (var i = 0; i < allLists.length; i++) {
    if (allLists[i].id == id) {
      if (allLists[i].style.display !== 'block') {
        allLists[i].style.display = 'block';
      }
    } else {
      allLists[i].style.display = 'none';
    }
  }
}