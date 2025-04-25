document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-bs-toggle="modal-product"]').forEach(div => {
        div.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');

            fetch(`/api/products/${productId}/`)
                .then(response => response.json())
                .then(product => {
                    document.getElementById('productModalLabel').textContent = product.name;
            document.getElementById('modalProductImage').src = "/static/menu/img/" + product.photolink + ".jpg";
            document.getElementById('modalProductDescription').textContent = product.description;
            document.getElementById('modalProductPrice').textContent = product.price + "₽";
            document.getElementById('modalProductGrams').textContent = product.grams + "г";
            document.getElementById('modalProductStructure').textContent = product.structure;
            
            document.getElementById('modalProductKalories').textContent = product.kalories + " ккал";
            document.getElementById('modalProductProtein').textContent = product.protein + " г";
            document.getElementById('modalProductFat').textContent = product.fat + " г"; 
            document.getElementById('modalProductCarbs').textContent = product.carbohydrates + " г";

            document.getElementById('modalProductPriceBtn').textContent = product.price;

//          Добавляем аттрибуты к кнопке добавления в корзину в модальном окне
            document.getElementById('modalAddToCart').setAttribute("data-product-id", productId);

            const modal = new bootstrap.Modal(document.getElementById('productModal'));
            modal.show();
                })
        })
    })
})