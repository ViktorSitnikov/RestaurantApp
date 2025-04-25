// Ожидаем полной загрузки DOM перед выполнением скрипта
document.addEventListener('DOMContentLoaded', function() {
    // Получаем ссылку на модальное окно регистрации
    const registerModal = document.getElementById('registerModal');
    if (registerModal) {
        // Добавляем обработчик события при открытии модального окна
        registerModal.addEventListener('show.bs.modal', function() {
            // Отправляем GET запрос для получения формы регистрации
            fetch(REGISTER_URL)
                .then(response => response.json())
                .then(data => {
                    // Находим контейнер для формы и вставляем HTML
                    const formContainer = registerModal.querySelector('.form-container');
                    formContainer.innerHTML = `
                        <form method="POST" action="${REGISTER_URL}" id="registerForm" class="p-3">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${data.csrf_token}">
                            <div class="form-group mb-2">
                                <label for="id_username" class="form-label text-success">Имя пользователя</label>
                                <input type="text" name="username" id="id_username" class="form-control" placeholder="Имя пользователя" required>
                            </div>
                            <div class="form-group mb-2">
                                <label for="id_email" class="form-label text-success">Email</label>
                                <input type="email" name="email" id="id_email" class="form-control" placeholder="Email" required>
                            </div>
                            <div class="form-group mb-2">
                                <label for="id_password1" class="form-label text-success">Пароль</label>
                                <input type="password" name="password1" id="id_password1" class="form-control" required>
                            </div>
                            <div class="form-group mb-4">
                                <label for="id_password2" class="form-label text-success">Подтверждение пароля</label>
                                <input type="password" name="password2" id="id_password2" class="form-control" required>
                            </div>
                            <div id="loginErrors" class="alert alert-danger d-none"></div>
                            <button type="submit" class="btn btn-success w-100">Зарегистрироваться</button>
                        </form>
                    `;
                    
                    // Добавляем обработчик отправки формы
                    const form = formContainer.querySelector('#registerForm');
                    form.addEventListener('submit', function(e) {
                        e.preventDefault(); // Предотвращаем стандартную отправку формы
                        const formData = new FormData(form);
                        
                        // Отправляем POST запрос с данными формы
                        fetch(form.action, {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': data.csrf_token
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                // При успешной регистрации перезагружаем страницу
                                window.location.reload();
                            } else {
                                // Отображаем ошибки, если они есть
                                const errorDiv = document.querySelector('#loginErrors');
                                errorDiv.classList.remove('d-none');
                                errorDiv.innerHTML = '';
                                if (data.errors) {
                                    // Выводим все полученные ошибки
                                    for (const [field, error] of Object.entries(data.errors)) {
                                        errorDiv.innerHTML += `<p class="mb-2">${error}</p>`;
                                    }
                                } else {
                                    // Выводим общее сообщение об ошибке
                                    errorDiv.innerHTML = '<p class="mb-0">Произошла ошибка при регистрации</p>';
                                }
                            }
                        })
                        .catch(error => {
                            // Обработка ошибок при отправке формы
                            console.error('Error:', error);
                            const errorDiv = document.querySelector('#loginErrors');
                            errorDiv.classList.remove('d-none');
                            errorDiv.innerHTML = '<p class="mb-0">Произошла ошибка при отправке формы</p>';
                        });
                    });
                })
                .catch(error => {
                    // Обработка ошибок при загрузке формы
                    console.error('Error loading form:', error);
                    const formContainer = registerModal.querySelector('.form-container');
                    formContainer.innerHTML = '<div class="alert alert-danger">Ошибка при загрузке формы регистрации</div>';
                });
        });
    }
});