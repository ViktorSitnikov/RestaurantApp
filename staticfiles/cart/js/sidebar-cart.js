// Функция для обновления UI корзины
function updateCartUI() {
    // Очищаем корзину
    if (document.getElementById('sidebarCartItemsHolder') != null) {
        itemsHolder = document.getElementById('sidebarCartItemsHolder');
        totalCostElement = document.getElementById('sidebarCartTotalCost');
    } else {
        itemsHolder = document.getElementById('order-items-holder');
        totalCostElement = document.getElementById('cart-total-cost');
    }

    
    
    itemsHolder.innerHTML = '';
    totalCostElement.textContent = '';
    totalCost = 0;



    if (cartItems.length === 0) {
        updateCartBadge(true);

        itemsHolder.innerHTML = `
            <li class="list-group-item d-flex justify-content-center align-items-center my-1 flex-grow-1">
                <div class="text-center">
                    <i class="fas fa-shopping-basket fa-2x mb-2" style="color: #6A994E;"></i>
                    <p class="text-muted mb-1">Ваша корзина пуста</p>
                    <small class="text-muted">Добавьте что-нибудь вкусненькое!</small>
                </div>
            </li>
        `;
    } else if (document.getElementById('sidebarCartItemsHolder') != null) {
        // Добавляем товары из корзины в UI
        cartItems.forEach(item => {
            updateSidebarCart(item);
            updateCartBadge(false);

        });
    } else {
        
        cartItems.forEach(item => {
            updateOrderCart(item);
            updateCartBadge(false);
        });
    }

    // Обновляем общую стоимость корзины
    totalCostElement.textContent = `${totalCost.toFixed(2)}₽`;
}

function updateSidebarCart(item){
    const template = document.getElementById('menuCartElement');  // Шаблон для товара в корзине
            const clone = template.content.cloneNode(true);

            // Рассчитываем стоимость позиции
            const positionPrice = parseFloat(item.cost);
            totalCost += positionPrice * item.quantity;

            // Заполняем данные в шаблоне
            clone.querySelector('.sidebar-cart-position-name').textContent = item.product_name;
            clone.querySelector('.sidebar-cart-position-price').textContent = `${positionPrice.toFixed(2)}₽`;
            clone.querySelector('.quantity').textContent = `${item.quantity}`;

            // Обработчики для кнопок изменения количества
            clone.querySelector('.btn-increase').addEventListener('click', () => {
                addToCart(item.product_id);  // Увеличиваем количество
            });

            clone.querySelector('.btn-decrease').addEventListener('click', () => {
                removeFromCart(item.product_id);  // Уменьшаем количество
            });

            clone.querySelector('.btn-remove').addEventListener('click', () => {
                removeFromCart(item.product_id, true);  // Удаляем товар полностью
            });

            // Добавляем товар в список корзины
            itemsHolder.appendChild(clone);
}

function updateOrderCart(item){
    const template = document.getElementById('orderCartElement');  // Шаблон для товара в корзине
            const clone = template.content.cloneNode(true);
            console.log('Название:', item.product_name);


            // Рассчитываем стоимость позиции
            const positionPrice = parseFloat(item.cost);
            totalCost += positionPrice * item.quantity;
            console.log(item);
            console.log(item.product_image);

            // Заполняем данные в шаблоне
            clone.querySelector('.order-cart-position-img-container').setAttribute('data-product-id', item.product_id);
            clone.querySelector('.order-cart-position-img').setAttribute('src', `${STATIC_URL}${item.product_image}.jpg`);
            clone.querySelector('.order-cart-position-name').textContent = item.product_name;
            clone.querySelector('.order-cart-position-price').textContent = `${positionPrice.toFixed(2)}`
            clone.querySelector('.order-cart-position-grams').textContent = `${item.product_grams}`;
            clone.querySelector('.quantity').textContent = `${item.quantity}`;

            // Обработчики для кнопок изменения количества
            clone.querySelector('.btn-increase').addEventListener('click', () => {
                addToCart(item.product_id);  // Увеличиваем количество
            });

            clone.querySelector('.btn-decrease').addEventListener('click', () => {
                removeFromCart(item.product_id);  // Уменьшаем количество
            });

            clone.querySelector('.btn-remove').addEventListener('click', () => {
                removeFromCart(item.product_id, true);  // Удаляем товар полностью
            });

            // Добавляем товар в список корзины
            itemsHolder.appendChild(clone);
}

function updateCartBadge(noItems = false){
    const cartBadge = document.getElementById('cart-badge');
    if(noItems){
        cartBadge.textContent = '';
    }else{
        cartBadge.textContent = `${cartItems.length}`;
    }
}



