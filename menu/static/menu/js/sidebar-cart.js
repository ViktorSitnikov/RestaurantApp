// Хранение данных корзины
let cartItems = []; // Массив объектов {id, product, quantity}
let totalCost = 0.00;

// DOM элементы
const sidebarCart = document.getElementById('sidebarCart');
const itemsHolder = document.getElementById('sidebarCartItemsHolder');
const totalCostElement = document.getElementById('sidebarCartTotalCost');

// Инициализация корзины
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок "Добавить в корзину"
    document.querySelectorAll('[data-bs-toggle="addToCart"]').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const product = JSON.parse(this.getAttribute('data-product-json'));

            addToCart(productId, product);
        });
    });
});

// Добавление товара в корзину
// когда добавляется новый товар с новым id 
// то выполняется снова и передает снова все товары из корзины из-за это получается такая сумма
function addToCart(productId, product) {

    // Проверяем, есть ли уже такой товар в корзине
    const existingItemIndex = cartItems.findIndex(item => item.id === productId);

    if (existingItemIndex !== -1) {
        // Увеличиваем количество
        cartItems[existingItemIndex].quantity += 1;
    } else {
        // Добавляем новый товар
        cartItems.push({
            id: productId,
            product: product,
            quantity: 1
        });
    }

    updateCartUI();
}

// Удаление товара из корзины
function removeFromCart(productId, completely = false) {
    const itemIndex = cartItems.findIndex(item => item.id === productId);

    if (itemIndex !== -1) {
        if (completely || cartItems[itemIndex].quantity <= 1) {
            // Удаляем товар полностью
            cartItems.splice(itemIndex, 1);
            updateCartUI(-1);
        } else {
            // Уменьшаем количество
            cartItems[itemIndex].quantity -= 1;
            updateCartUI(-1);
        }
    }


}

// Обновление интерфейса корзины
function updateCartUI(totalCostReduce = 1) {
    // Очищаем корзину
    document.getElementById('sidebarCartItemsHolder').innerHTML = '';

    totalCost = 0;


    

    // Добавляем все товары здесь как понял передаются все снова уникальные товары в корзине и суммируются 
    cartItems.forEach(item => {
        const template = document.getElementById('menuCartElement');
        const clone = template.content.cloneNode(true);

        // Рассчитываем стоимость позиции
        const positionPrice = parseFloat(item.product.price) * parseFloat(item.quantity);
        totalCost += positionPrice;

        // Заполняем данные
        clone.querySelector('.sidebar-cart-position-name').textContent =
            `${item.product.name}${item.quantity > 1 ? ` ×${item.quantity}` : ''}`;

        clone.querySelector('.sidebar-cart-position-price').textContent =
            `${positionPrice.toFixed(2)}₽`;

        // Обработчики для кнопок управления количеством
        clone.querySelector('.btn-increase').addEventListener('click', () => {
            addToCart(item.id, item.product);
        });

        clone.querySelector('.btn-decrease').addEventListener('click', () => {
            removeFromCart(item.id);
        });

        clone.querySelector('.btn-remove').addEventListener('click', () => {
            removeFromCart(item.id, true);
        });

        document.getElementById('sidebarCartItemsHolder').appendChild(clone);
    });

    // Обновляем общую стоимость
    document.getElementById('sidebarCartTotalCost').textContent = totalCost.toFixed(2);
}