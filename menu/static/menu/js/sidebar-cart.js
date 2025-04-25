// Хранение данных корзины
let cartItems = []; // Массив объектов {id, product, quantity}

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
            // const product = JSON.parse(this.getAttribute('data-product-json'));

            fetch(`api/products/${productId}/`)
                .then(response => response.json())
                .then(product => {
                    addToCart(productId, product);
                });

            
        });
    });
    updateCartUI();
});

// Добавление товара в корзину
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
        } else {
            // Уменьшаем количество
            cartItems[itemIndex].quantity -= 1;
        }
    }

    updateCartUI();
}

// Обновление интерфейса корзины
function updateCartUI() {


    let totalCost = 0;

    // Очищаем корзину
    document.getElementById('sidebarCartItemsHolder').innerHTML = '';

    if (cartItems.length === 0) {
        document.getElementById('sidebarCartItemsHolder').innerHTML = `
            <li class="list-group-item d-flex justify-content-center align-items-center my-1 flex-grow-1">
                <div class="text-center">
                    <i class="fas fa-shopping-basket fa-2x mb-2" style="color: #6A994E;"></i>
                    <p class="text-muted mb-1">Ваша корзина пуста</p>
                    <small class="text-muted">Добавьте что-нибудь вкусненькое!</small>
                </div>
            </li>
        `;
    }
    else {
    // Добавляем все товары
    cartItems.forEach(item => {
        const template = document.getElementById('menuCartElement');
        const clone = template.content.cloneNode(true);

        // Рассчитываем стоимость позиции
        const positionPrice = parseFloat(item.product.price) * parseFloat(item.quantity);
        totalCost += positionPrice;

        // Заполняем данные
        clone.querySelector('.sidebar-cart-position-name').textContent =
            `${item.product.name}`;

        clone.querySelector('.sidebar-cart-position-price').textContent =
            `${positionPrice.toFixed(2)}₽`;

        clone.querySelector('.quantity').textContent =
            `${item.quantity}`;
            
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
    }

    // Обновляем общую стоимость
    document.getElementById('sidebarCartTotalCost').textContent = totalCost.toFixed(2);
}