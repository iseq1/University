const button = document.getElementById('level-info-btn');
const block = document.getElementById('level-info-label');

const button2 = document.getElementById('level-info-btn-2');
const block2 = document.getElementById('level-info-label-2');

button.addEventListener('mouseover', function() {
  block.style.display = 'block';
});

button.addEventListener('mouseout', function() {
  block.style.display = 'none';
});

button2.addEventListener('mouseover', function() {
  block2.style.display = 'block';
});

button2.addEventListener('mouseout', function() {
  block2.style.display = 'none';
});
