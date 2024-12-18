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
            clearEditForm();
        });
        
    // Очистка формы при закрытии модального окна
    function clearEditForm() {
        document.getElementById('edit-id').value = '';
        document.getElementById('edit-name').value = '';
        document.getElementById('edit-category').value = '';
        document.getElementById('edit-description').value = '';
        document.getElementById('edit-price').value = '';
        document.getElementById('edit-stock').value = '';
        document.getElementById('edit-image').value = '';
    }
   });

    // Обработка отправки формы
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(editForm);
        const productId = document.getElementById('edit-id').value;

        fetch(`/admin/products/edit/${productId}`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Ошибка при редактировании товара.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Товар успешно отредактирован.');
                location.reload();
            } else {
                alert(data.message || 'Ошибка при редактировании товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(error.message || 'Произошла ошибка при выполнении запроса.');
        });
    });
});
//-----------------------------------------------------------------------------------------------------------



//--------------------------------------------------------------------------------------------------------------
// Обработчик добавления товара
//--------------------------------------------------------------------------------------------------------------
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

    // Единый обработчик отправки формы
    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Получаем значения полей
        const name = document.getElementById('name').value.trim();
        const category = categorySelect.value;
        const newCategory = editCategoryInput.value.trim();
        const description = document.getElementById('description').value.trim();
        const price = document.getElementById('price').value.trim();
        const stock = document.getElementById('stock').value.trim();

        // Проверка заполненности полей
        if (!name) {
            alert('Пожалуйста, введите название товара.');
            return;
        }
        if (!category && !newCategory) {
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

        // Создаем FormData для отправки данных
        const formData = new FormData(form);

        // Если есть новая категория, создаём её
        if (newCategory) {
            try {
                const categoryResult = await createNewCategory(newCategory);
                if (categoryResult.success) {
                    formData.set('category', categoryResult.category_id);
                } else {
                    alert('Ошибка при создании категории');
                    return;
                }
            } catch (error) {
                alert('Ошибка при создании категории');
                return;
            }
        }

        // Отправка данных товара
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
                location.reload();
            } else {
                alert(data.message || 'Ошибка при добавлении товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });

    // Функция создания новой категории остаётся без изменений
    async function createNewCategory(categoryName) {
        try {
            // Добавим проверку
            if (!categoryName) {
                throw new Error('Название категории не может быть пустым');
            }
    
            const requestData = {
                category_name: categoryName
            };
            
            console.log('Отправляемые данные категории:', requestData); // Отладка
    
            const response = await fetch('/admin/products/categories/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                },
                body: JSON.stringify(requestData)
            });
    
            const data = await response.json();
            console.log('Ответ сервера:', data); // Отладка
    
            if (!response.ok) {
                throw new Error(data.message || 'Ошибка при создании категории');
            }
    
            return data;
        } catch (error) {
            console.error('Ошибка при создании категории:', error);
            throw error;
        }
    }
});
//--------------------------------------------------------------------------------------------------------------
// Очистка формы при закрытии модального окна
function clearAddForm() {
    document.getElementById('name').value = '';
    document.getElementById('category').value = '';
    document.getElementById('description').value = '';
    document.getElementById('price').value = '';
    document.getElementById('stock').value = '';
    document.getElementById('image').value = '';
}
//--------------------------------------------------------------------------------------------------------------
// Обработчик закрытия модального окна с подтверждением
document.querySelector('.close-btn_add-modal').addEventListener('click', function() {
    const modal = document.getElementById('add-product-modal');
    const confirmClose = confirm('Вы уверены, что хотите закрыть окно? Все несохраненные изменения будут потеряны.');

    if (confirmClose) {
        modal.style.display = 'none'; // Закрытие модального окна
        clearAddForm();
    }
});
//--------------------------------------------------------------------------------------------------------------
// Обработчик выбора категории
document.getElementById('add-product-btn').addEventListener('click', function() {
    // Открытие модального окна для добавления нового товара
    const modal = document.getElementById('add-product-modal');
    modal.style.display = 'block';
   
    // Очистка формы
    clearAddForm();

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



//--------------------------------------------------------------------------------------------------------------
// Обработчик поиска товаров
document.getElementById('search-btn').addEventListener('click', function() {
    const searchQuery = document.getElementById('product-search').value;
    const searchType = document.getElementById('search-filter').value;

    // Если поле поиска пустое - получаем все товары
    if (!searchQuery.trim()) {
        location.reload();
        return;
    }

    fetch('/admin/products/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
        body: JSON.stringify({
            query: searchQuery,         // Изменено с search_query
            type: searchType           // Изменено с search_type
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при поиске');
        }
        return response.json();
    })
    .then(data => {
        const tableBody = document.querySelector('table tbody');
        tableBody.innerHTML = ''; // Очищаем текущие результаты

        if (data && Array.isArray(data) && data.length > 0) {  // Изменена проверка данных
            data.forEach((product, index) => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${product[0]}</td>
                        <td>${product[6] ? 
                            `<img src="/static/images/${product[6]}" alt="${product[6]}" width="150">` : 
                            '<span>Изображение отсутствует</span>'
                        }</td>
                        <td>${product[1]}</td>
                        <td>${product[2]}</td>
                        <td>${product[3]}</td>
                        <td>${product[4]} руб.</td>
                        <td>${product[5]}</td>
                        <td>
                            <div class="action-buttons">
                                <button class="edit-product-btn" 
                                    data-id="${product[0]}"
                                    data-name="${product[1]}"
                                    data-category="${product[2]}"
                                    data-description="${product[3]}"
                                    data-price="${product[4]}"
                                    data-stock="${product[5]}"
                                    data-image="${product[6] || ''}">Редактировать</button>
                                <button class="duplicate-btn" data-id="${product[0]}">Дублировать</button>
                                <button class="delete-btn" data-id="${product[0]}">Удалить</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="9">Ничего не найдено</td></tr>';
        }

        attachEventHandlers();
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при поиске');
    });
});
//--------------------------------------------------------------------------------------------------------------
// Функция для прикрепления обработчиков событий
function attachEventHandlers() {
    // Переприкрепляем обработчики для кнопок редактирования
    document.querySelectorAll('.edit-product-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Ваш существующий код обработчика редактирования
        });
    });

    // Переприкрепляем обработчики для кнопок дублирования
    document.querySelectorAll('.duplicate-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Ваш существующий код обработчика дублирования
        });
    });

    // Переприкрепляем обработчики для кнопок удаления
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Ваш существующий код обработчика удаления
        });
    });
}
//--------------------------------------------------------------------------------------------------------------
// Добавляем слушатель события input для поля поиска
document.getElementById('product-search').addEventListener('input', function() {
    // Если поле пустое
    if (!this.value.trim()) {
        // Делаем запрос к серверу для получения всех товаров
        fetch('/admin/products/get_all', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('table tbody');
            tableBody.innerHTML = ''; // Очищаем текущие результаты

            if (Array.isArray(data)) {
                data.forEach((product, index) => {
                    tableBody.innerHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${product.id}</td>
                            <td>${product.image ? 
                                `<img src="/static/images/${product.image}" alt="${product.image}" width="150">` : 
                                '<span>Изображение отсутствует</span>'
                            }</td>
                            <td>${product.name}</td>
                            <td>${product.category}</td>
                            <td>${product.description}</td>
                            <td>${product.price} руб.</td>
                            <td>${product.stock}</td>
                            <td>
                                <div class="action-buttons">
                                    <button class="edit-product-btn" data-id="${product.id}">Редактировать</button>
                                    <button class="duplicate-btn" data-id="${product.id}">Дублировать</button>
                                    <button class="delete-btn" data-id="${product.id}">Удалить</button>
                                </div>
                            </td>
                        </tr>
                    `;
                });
            }
            attachEventHandlers();
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при получении данных');
        });
    }
});
//--------------------------------------------------------------------------------------------------------------