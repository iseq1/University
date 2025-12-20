const popup = document.getElementById("popup");
function openPopup(){
    popup.classList.add("open-popup");
}
function closePopup(){
    popup.classList.remove("open-popup");
}

function addToCart(drinkName) {
    $.ajax({
        type: 'POST',
        url: '/add_to_cart',
        data: {drink_name: drinkName},
        success: function(response) {
            // После успешного добавления товара в корзину, вызываем функцию открытия pop-up окна
            openPopup();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
