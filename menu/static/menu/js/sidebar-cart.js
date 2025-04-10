let totalCost = 0.00;

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-bs-toggle="addToCart"]').forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('sidebarCart').classList.add('d-xl-block');

            const productId = this.getAttribute('data-product-id');
            const product = JSON.parse(this.getAttribute('data-product-json'));
            const price = parseFloat(product.price);



            totalCost += price;

//            document.getElementById('productModalLabel').textContent = product.name;
//            document.getElementById('modalProductImage').src = "/static/menu/img/" + product.photolink + ".jpg";
//            document.getElementById('modalProductDescription').textContent = product.description;
//            document.getElementById('modalProductPrice').textContent = product.price + "₽";
//            document.getElementById('modalProductGrams').textContent = product.grams + "г";
//            document.getElementById('modalProductStructure').textContent = product.structure;
//            document.getElementById('modalProductNutrition').innerHTML = `
//            Калории: ${product.kalories} ккал<br>
//            Белки: ${product.protein} ккал<br>
//            Жиры: ${product.fat} ккал<br>
//            Углеводы: ${product.carbohydrates} ккал<br>
//            `;
//            document.getElementById('elementPrice').textContent = product.price;



//          Вывод общей стоимости заказа в сайдбар
            document.getElementById('sidebarCartTotalCost').textContent = totalCost;


        })
    })
})



