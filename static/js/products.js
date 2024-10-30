//--------------------------------------------------------------------------------------------------------------
// Обработчик дублирования товара
document.querySelectorAll('.duplicate-btn').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-id');
        fetch(`/admin/products/duplicate/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Ошибка при дублировании товара.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Товар успешно добавлен (дублирован).');
                location.reload();
            } else {
                alert(data.message || 'Ошибка при дублировании товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });
});
//--------------------------------------------------------------------------------------------------------------
// Обработчик удаления товара
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-id');
        fetch(`/admin/products/delete/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'  // Убедитесь, что CSRF токен правильно настроен
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Товар успешно помечен как удаленный');
                location.reload();
            } else {
                alert(data.message || 'Ошибка при удалении товара');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });
});
//--------------------------------------------------------------------------------------------------------------
