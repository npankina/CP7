//--------------------------------------------------------------------------------------------------------------
// Обработчик дублирования товара
//--------------------------------------------------------------------------------------------------------------




//--------------------------------------------------------------------------------------------------------------
// Обработчик удаления товара
//--------------------------------------------------------------------------------------------------------------




//--------------------------------------------------------------------------------------------------------------
// Обработчик редактирования товара
document.addEventListener('DOMContentLoaded', function() {
    const editProductModal = document.getElementById('edit-product-modal');
    const closeBtns = document.querySelectorAll('.close-btn');
    const editProductBtns = document.querySelectorAll('.edit-product-btn');
    const editForm = document.getElementById('edit-product-form');

    // Открытие модального окна для редактирования
    editProductBtns.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-id');
            const productName = this.getAttribute('data-name');
            const productCategory = this.getAttribute('data-category');
            const productDescription = this.getAttribute('data-description');
            const productPrice = this.getAttribute('data-price');
            const productStock = this.getAttribute('data-stock');

            // Заполнение формы текущими данными
            document.getElementById('edit-id').value = productId;
            document.getElementById('edit-name').value = productName;
            document.getElementById('edit-category').value = productCategory;
            document.getElementById('edit-description').value = productDescription;
            document.getElementById('edit-price').value = productPrice;
            document.getElementById('edit-stock').value = productStock;

            editProductModal.style.display = 'block';
        });
    });

    // Закрытие модального окна с подтверждением
    closeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите закрыть окно без сохранения изменений?')) {
                editProductModal.style.display = 'none';
            }
        });
    });

    // Обработка отправки формы
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(editForm);

        fetch('/admin/products/edit', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Товар успешно обновлен');
                location.reload();
            } else {
                alert(data.message || 'Ошибка при обновлении товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });
});
//--------------------------------------------------------------------------------------------------------------
document.querySelectorAll('.edit-product-btn').forEach(button => {
    button.addEventListener('click', function() {
        const modal = document.getElementById('edit-product-modal');
        modal.style.display = 'block';

        // Получение данных товара
        const productId = this.getAttribute('data-id');
        const productName = this.getAttribute('data-name');
        const productCategory = this.getAttribute('data-category');
        const productDescription = this.getAttribute('data-description');
        const productPrice = this.getAttribute('data-price');
        const productStock = this.getAttribute('data-stock');

        // Заполнение формы текущими данными
        document.getElementById('edit-id').value = productId;
        document.getElementById('edit-name').value = productName;
        document.getElementById('edit-description').value = productDescription;
        document.getElementById('edit-price').value = productPrice;
        document.getElementById('edit-stock').value = productStock;

        // Загрузка категорий
        fetch('/admin/products/categories')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка при загрузке категорий');
                }
                return response.json();
            })
            .then(data => {
                const categorySelect = document.getElementById('category');
                categorySelect.innerHTML = ''; // Очистка предыдущих значений

                // Добавление пустого поля
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.disabled = true;
                defaultOption.textContent = '-- Выберите категорию --';
                categorySelect.appendChild(defaultOption);

                // Добавление загруженных категорий
                data.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id; // Убедитесь, что используете правильное поле
                    option.textContent = category.name;
                    if (category.name === productCategory) {
                        option.selected = true;
                    }
                    categorySelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Ошибка при загрузке категорий:', error);
            });
    });
});
//-----------------------------------------------------------------------------------------------------------




//--------------------------------------------------------------------------------------------------------------
// Обработчик добавления товара
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-product-form');
    const categorySelect = document.getElementById('category');
    const editCategoryInput = document.getElementById('add-category');

    // Обработчик изменения выбора категории
    categorySelect.addEventListener('change', function() {
        if (categorySelect.value) {
            editCategoryInput.removeAttribute('required');
        } else {
            editCategoryInput.setAttribute('required', 'required');
        }
    });

    form.addEventListener('submit', function(event) {
        // Предотвращаем отправку формы по умолчанию
        event.preventDefault();

        // Получаем значения полей
        const name = document.getElementById('name').value.trim();
        const category = categorySelect.value;
        const editCategory = editCategoryInput.value.trim();
        const description = document.getElementById('description').value.trim();
        const price = document.getElementById('price').value.trim();
        const stock = document.getElementById('stock').value.trim();

        // Проверка заполненности полей
        if (!name) {
            alert('Пожалуйста, введите название товара.');
            return;
        }
        if (!category && !editCategory) {
            alert('Пожалуйста, выберите категорию из списка или введите новую.');
            return;
        }
        if (!description) {
            alert('Пожалуйста, введите описание товара.');
            return;
        }
        if (!price) {
            alert('Пожалуйста, введите цену товара.');
            return;
        }
        if (!stock) {
            alert('Пожалуйста, введите количество товара в наличии.');
            return;
        }

        // Создаем FormData из формы
        const formData = new FormData(form);

        fetch('/admin/products/add', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при добавлении товара');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Товар успешно добавлен');
                location.reload();  // Обновление страницы
            } else {
                alert(data.message || 'Ошибка при добавлении товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });
});
//--------------------------------------------------------------------------------------------------------------
// Обработчик закрытия модального окна с подтверждением
document.querySelector('.close-btn_add-modal').addEventListener('click', function() {
    const modal = document.getElementById('add-product-modal');
    const confirmClose = confirm('Вы уверены, что хотите закрыть окно? Все несохраненные изменения будут потеряны.');

    if (confirmClose) {
        modal.style.display = 'none'; // Закрытие модального окна
    }
});
//--------------------------------------------------------------------------------------------------------------
// Обработчик выбора категории
document.getElementById('add-product-btn').addEventListener('click', function() {
    // Открытие модального окна для добавления нового товара
    const modal = document.getElementById('add-product-modal');
    modal.style.display = 'block';
   
    // Очистка формы
    document.getElementById('name').value = '';
    document.getElementById('category').value = '';
    document.getElementById('description').value = '';
    document.getElementById('price').value = '';
    document.getElementById('stock').value = '';
    document.getElementById('image').value = '';

    // Изменение заголовка и кнопки формы
    modal.querySelector('h2').textContent = 'Добавить новый товар';
    // modal.querySelector('.submit-btn').textContent = 'Добавить';

    // Загрузка категорий
    fetch('/admin/products/categories')
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при загрузке категорий');
            }
            return response.json();
        })
        .then(data => {
            console.log('Загруженные категории:', data); // Отладочное сообщение
            const categorySelect = document.getElementById('category');
            categorySelect.innerHTML = ''; // Очистка предыдущих значений
            
            // Добавление пустого поля
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = '-- Выберите категорию --';
            categorySelect.appendChild(defaultOption);

            // Добавление загруженных категорий
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.category_id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке категорий:', error);
        });
});
//--------------------------------------------------------------------------------------------------------------