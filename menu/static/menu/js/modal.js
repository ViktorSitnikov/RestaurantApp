document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-bs-toggle="modal-product"]').forEach(div => {
        div.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const product = JSON.parse(this.getAttribute('data-product-json'));

            document.getElementById('productModalLabel').textContent = product.name;
            document.getElementById('modalProductImage').src = "/static/menu/img/" + product.photolink + ".jpg";
            document.getElementById('modalProductDescription').textContent = product.description;
            document.getElementById('modalProductPrice').textContent = product.price + "₽";
            document.getElementById('modalProductGrams').textContent = product.grams + "г";
            document.getElementById('modalProductStructure').textContent = product.structure;
            document.getElementById('modalProductNutrition').innerHTML = `
            Калории: ${product.kalories} ккал<br>
            Белки: ${product.protein} ккал<br>
            Жиры: ${product.fat} ккал<br>
            Углеводы: ${product.carbohydrates} ккал<br>
            `;
            document.getElementById('modalProductPriceBtn').textContent = product.price;

//          Добавляем аттрибуты к кнопке добавления в корзину в модальном окне
            document.getElementById('modalAddToCart').setAttribute("data-product-id", productId);
            document.getElementById('modalAddToCart').setAttribute("data-product-json", `{"name": "` + product.name +`", "price": "` + product.price +`"}`);

            const modal = new bootstrap.Modal(document.getElementById('productModal'));
            modal.show();
        })
    })
})


                // data-product-json='{% spaceless %}
                //  {
                //     "name": "{{ product.name|escapejs }}",
                //     "photolink": "{{ product.photolink|escapejs }}",
                //     "description": "{{ product.description|escapejs }}",
                //     "price": "{{ product.price }}",
                //     "grams": "{{ product.grams }}",
                //     "structure": "{{ product.structure|escapejs }}",
                //     "kalories": "{{ product.kalories }}",
                //     "protein": "{{ product.protein }}",
                //     "fat": "{{ product.fat }}",
                //     "carbohydrates": "{{ product.carbohydrates }}"
                //  }{% endspaceless %}' 