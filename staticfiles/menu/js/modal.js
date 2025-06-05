// Функция для загрузки данных и показа модального окна
function showProductModal(productId) {
    fetch(`/api/products/${productId}/`)
        .then(response => response.json())
        .then(product => {
            // Заполняем модалку данными
            document.getElementById('productModalLabel').textContent = product.name;
            document.getElementById('modalProductImage').src = `/static/menu/img/${product.photolink}.jpg`;
            document.getElementById('modalProductDescription').textContent = product.description;
            document.getElementById('modalProductPrice').textContent = `${product.price}₽`;
            document.getElementById('modalProductGrams').textContent = `${product.grams}г`;
            document.getElementById('modalProductStructure').textContent = product.structure;
            document.getElementById('modalProductCategory').textContent = product.category;

            document.getElementById('modalProductKalories').textContent = `${product.kalories} ккал`;
            document.getElementById('modalProductProtein').textContent = `${product.protein} г`;
            document.getElementById('modalProductFat').textContent = `${product.fat} г`;
            document.getElementById('modalProductCarbs').textContent = `${product.carbohydrates} г`;

            document.getElementById('modalProductPriceBtn').textContent = product.price;
            document.getElementById('modalAddToCart').setAttribute("data-dish-id", productId);

            // Открытие модалки
            const modal = new bootstrap.Modal(document.getElementById('productModal'));
            modal.show();
        })
        .catch(error => {
            console.error("Ошибка при загрузке продукта:", error);
        });
}

document.addEventListener('click', function(event) {
    // Ищем ближайший элемент с data-bs-toggle="modal-product"
    const target = event.target.closest('[data-bs-toggle="modal-product"]');
    if (!target) return;  // Если клик не по нужному элементу — выходим

    const productId = target.getAttribute('data-product-id');
    if (productId) {
        showProductModal(productId);  // Показываем модалку
    }
});
