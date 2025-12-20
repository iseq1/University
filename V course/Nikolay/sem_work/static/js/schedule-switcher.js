document.addEventListener("DOMContentLoaded", function() {
    var cells = document.querySelectorAll('.inactive');
    cells.forEach(function(cell) {
        var inputStart = cell.querySelector('input[name="timeStart_Monday"]');
        var inputEnd = cell.querySelector('input[name="timeEnd_Monday"]');

        if (inputStart.value !== '00:00' || inputEnd.value !== '00:00') {
            cell.classList.remove('inactive');
        }
    });
});
