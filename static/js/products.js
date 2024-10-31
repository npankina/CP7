//--------------------------------------------------------------------------------------------------------------
// Обработчик дублирования товара

//--------------------------------------------------------------------------------------------------------------
// Обработчик удаления товара

//--------------------------------------------------------------------------------------------------------------
// Обработчик редактирования товара

//--------------------------------------------------------------------------------------------------------------
// Обработчик добавления товара

//--------------------------------------------------------------------------------------------------------------
// Обработчик выбора категории
document.getElementById('add-product-btn').addEventListener('click', function() {
    // Открытие модального окна для добавления нового товара
    const modal = document.getElementById('edit-product-modal');
    modal.style.display = 'block';

    // Очистка формы
    document.getElementById('edit-id').value = '';
    document.getElementById('edit-name').value = '';
    document.getElementById('edit-category').value = '';
    document.getElementById('edit-description').value = '';
    document.getElementById('edit-price').value = '';
    document.getElementById('edit-stock').value = '';
    document.getElementById('edit-image').value = '';

    // Изменение заголовка и кнопки формы
    modal.querySelector('h2').textContent = 'Добавить новый товар';
    modal.querySelector('.submit-btn').textContent = 'Добавить';

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