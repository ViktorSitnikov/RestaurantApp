// Массив для хранения товаров в корзине (для текущей сессии)
let cartItems = []; 

function getCSRFToken() {
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
    return csrfToken ? csrfToken[1] : null;
}

// Инициализация корзины при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Загрузить текущие товары из корзины с сервера
    loadCartFromDB();

    // Обработчики для кнопок "Добавить в корзину"
    document.querySelectorAll('[data-bs-toggle="addToCart"]').forEach(button => {
        button.addEventListener('click', function() {
            const dishId = this.getAttribute('data-dish-id');
            addToCart(dishId);  // Добавление блюда в корзину через API
        });
    });
});

// Функция для загрузки корзины с сервера
function loadCartFromDB() {
    fetch('/cart/api/cart/')
        .then(response => response.json())
        .then(data => {
            cartItems = data;  // Сохраняем товары в корзине
            updateCartUI();  // Обновляем интерфейс корзины
        });
}

function addToCart(dishId) {
    const csrfToken = getCSRFToken(); // Получаем CSRF токен из cookies

    fetch(`/cart/api/cart/add/${dishId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Добавляем CSRF токен в заголовки
        },
        body: JSON.stringify({
            'dish_id': dishId
        })
    })
    .then(response => {
        return response.json(); // Пытаемся парсить ответ как JSON
    })
    .then(data => {
        if (data.success) {
            loadCartFromDB();  // Перезагружаем корзину после добавления
        }
    })
    .catch(error => console.error('Ошибка при добавлении товара:', error));
}


// Функция для удаления товара из корзины
function removeFromCart(dishId, completely = false) {
    const csrfToken = getCSRFToken(); // Получаем CSRF токен из cookies
    if (!csrfToken) {
        console.error('CSRF токен не найден!');
        return;
    }

    fetch(`/cart/api/cart/remove/${dishId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Добавляем CSRF токен в заголовки
        },
        body: JSON.stringify({
            completely: completely  // Добавляем параметр completely в тело запроса
        })
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              loadCartFromDB();  // Перезагружаем корзину после удаления
          }
      })
      .catch(error => console.error('Ошибка при удалении товара:', error));
}