// // 
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {
//     const modal = document.getElementById("editModal");
//     const closeModal = document.querySelector(".close");
//     const editForm = document.getElementById("editForm");
// //--------------------------------------------------------------------------------------------------------------
//     // Функция для открытия модального окна
//     function openModal(productId, productName, productCategory, productPrice) {
//         document.getElementById("productId").value = productId;
//         document.getElementById("productName").value = productName;
//         document.getElementById("productCategory").value = productCategory;
//         document.getElementById("productPrice").value = productPrice;
//         modal.style.display = "block";
//     }
// //--------------------------------------------------------------------------------------------------------------
//     // Закрытие модального окна
//     closeModal.onclick = function() {
//         modal.style.display = "none";
//     }
// //--------------------------------------------------------------------------------------------------------------
//     window.onclick = function(event) {
//         if (event.target == modal) {
//             modal.style.display = "none";
//         }
//     }
// //--------------------------------------------------------------------------------------------------------------
//     // Добавляем обработчики нажатия на кнопку "Редактировать"
//     document.querySelectorAll(".edit-btn").forEach(function(button) {
//         button.addEventListener("click", function(event) {
//             event.preventDefault();
//             const row = event.target.closest("tr");
//             const productId = row.dataset.id;
//             const productName = row.querySelector(".product-name").textContent;
//             const productCategory = row.querySelector(".product-category").textContent;
//             const productPrice = row.querySelector(".product-price").textContent;

//             openModal(productId, productName, productCategory, productPrice);
//         });
//     });
// //--------------------------------------------------------------------------------------------------------------
//     // Обработчик сохранения формы редактирования
//     editForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const productId = document.getElementById("productId").value;
//         const productName = document.getElementById("productName").value;
//         const productCategory = document.getElementById("productCategory").value;
//         const productPrice = document.getElementById("productPrice").value;

//         // Обновляем данные в таблице
//         const row = document.querySelector(`tr[data-id='${productId}']`);
//         row.querySelector(".product-name").textContent = productName;
//         row.querySelector(".product-category").textContent = productCategory;
//         row.querySelector(".product-price").textContent = productPrice;

//         // Закрываем модальное окно
//         modal.style.display = "none";
//     });
// });
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {
//     // Получаем элементы
//     const modal = document.getElementById('add-product-modal');
//     const openModalBtn = document.getElementById('add-product-btn');
//     const closeModalBtn = document.querySelector('.close-btn');

//     // Открытие модального окна
//     openModalBtn.addEventListener('click', function() {
//         modal.style.display = 'block';
//     });

//     // Закрытие модального окна
//     closeModalBtn.addEventListener('click', function() {
//         modal.style.display = 'none';
//     });

//     // Закрытие модального окна при клике вне его
//     window.addEventListener('click', function(event) {
//         if (event.target === modal) {
//             modal.style.display = 'none';
//         }
//     });
// });
// //--------------------------------------------------------------------------------------------------------------
// // модальное окно для редактирования товара
// document.addEventListener('DOMContentLoaded', function() {
//     // Модальное окно редактирования
//     const editModal = document.getElementById('edit-product-modal');
//     const closeEditModalBtn = editModal.querySelector('.close-btn');
//     const editForm = document.getElementById('edit-product-form');

//     // Обработка кнопки редактирования
//     const editButtons = document.querySelectorAll('.edit-product-btn');
//     editButtons.forEach(button => {
//         button.addEventListener('click', function() {
//             // Заполнение формы текущими данными товара
//             document.getElementById('edit-id').value = this.getAttribute('data-id');
//             document.getElementById('edit-name').value = this.getAttribute('data-name');
//             document.getElementById('edit-category').value = this.getAttribute('data-category');
//             document.getElementById('edit-description').value = this.getAttribute('data-description');
//             document.getElementById('edit-price').value = this.getAttribute('data-price');
//             document.getElementById('edit-stock').value = this.getAttribute('data-stock');

//             // Открытие модального окна
//             editModal.style.display = 'block';
//         });
//     });

//     // Закрытие модального окна редактирования
//     closeEditModalBtn.addEventListener('click', function() {
//         editModal.style.display = 'none';
//     });

//     // Закрытие модального окна при клике вне его
//     window.addEventListener('click', function(event) {
//         if (event.target === editModal) {
//             editModal.style.display = 'none';
//         }
//     });
// });
// //--------------------------------------------------------------------------------------------------------------




// //--------------------------------------------------------------------------------------------------------------
// // Функция для переключения боковой панели
// function toggleSidebar() {
//     const sidebar = document.getElementById('sidebar');
//     const tableContainer = document.querySelector('.table-container');

//     if (sidebar.classList.contains('collapsed')) {
//         sidebar.classList.remove('collapsed');
//         tableContainer.style.marginLeft = '200px';
//     } else {
//         sidebar.classList.add('collapsed');
//         tableContainer.style.marginLeft = '0';
//     }
// }
// //--------------------------------------------------------------------------------------------------------------
// // Функция для показа/скрытия боковой панели
// function toggleSidebar() {
//     const sidebar = document.getElementById('sidebar');
//     sidebar.classList.toggle('active');
// }
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {
//     const hamburger = document.getElementById('hamburger');
//     const sidebar = document.getElementById('sidebar');

//     if (hamburger && sidebar) {
//         hamburger.addEventListener('click', function() {
//             sidebar.classList.toggle('hidden');
//         });
//     }
// });
// //--------------------------------------------------------------------------------------------------------------




// // Кнопка удаления товара
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function () {
//     // Обработчик кнопки удаления
//     document.querySelectorAll('.delete-btn').forEach(function (button) {
//         button.addEventListener('click', function () {
//             const productId = this.getAttribute('data-id');
//             if (confirm('Вы уверены, что хотите удалить этот товар?')) {
//                 deleteProduct(productId);
//             }
//         });
//     });
// });

// function deleteProduct(productId) {
//     fetch(`/admin/products/delete`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ id: productId })
//     })
//     .then(response => {
//         if (response.ok) {
//             alert('Товар успешно удален!');
//             document.getElementById(`product-${productId}`).remove(); // Удаление карточки из DOM
//         } else {
//             alert('Ошибка при удалении товара.');
//         }
//     })
//     .catch(error => console.error('Ошибка:', error));
// }
// //--------------------------------------------------------------------------------------------------------------




// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {
//     const statusModal = document.getElementById("statusModal");
//     const viewOrderModal = document.getElementById("viewOrderModal");
//     const closeModalButtons = document.querySelectorAll(".close");

//     const statusForm = document.getElementById("statusForm");
//     const orderDetails = document.getElementById("orderDetails");

//     // Функция для открытия модального окна изменения статуса заказа
//     function openStatusModal(orderId, currentStatus) {
//         document.getElementById("orderId").value = orderId;
//         document.getElementById("orderStatus").value = currentStatus;
//         statusModal.style.display = "block";
//     }
// //--------------------------------------------------------------------------------------------------------------
//     // Функция для открытия модального окна просмотра деталей заказа
//     function openViewOrderModal(orderId) {
//         // Здесь вы можете загрузить данные о заказе через AJAX или заполнить их статически
//         // Для примера данные заполняются вручную
//         const detailsHtml = `
//             <p><strong>Номер заказа:</strong> ${orderId}</p>
//             <p><strong>Покупатель:</strong> Иван Иванов</p>
//             <p><strong>Дата:</strong> 2024-10-10</p>
//             <p><strong>Сумма:</strong> 12 500 руб.</p>
//             <p><strong>Товары:</strong></p>
//             <ul>
//                 <li>Ноутбук ASUS - 1 шт.</li>
//                 <li>Мышь Logitech - 1 шт.</li>
//             </ul>
//         `;
//         orderDetails.innerHTML = detailsHtml;
//         viewOrderModal.style.display = "block";
//     }
// //--------------------------------------------------------------------------------------------------------------
//     // Закрытие модальных окон
//     closeModalButtons.forEach(function(button) {
//         button.onclick = function() {
//             statusModal.style.display = "none";
//             viewOrderModal.style.display = "none";
//         };
//     });
// //--------------------------------------------------------------------------------------------------------------
//     window.onclick = function(event) {
//         if (event.target == statusModal) {
//             statusModal.style.display = "none";
//         }
//         if (event.target == viewOrderModal) {
//             viewOrderModal.style.display = "none";
//         }
//     };
// //--------------------------------------------------------------------------------------------------------------
//     // Добавляем обработчики на кнопку "Изменить статус"
//     document.querySelectorAll(".edit-status").forEach(function(button) {
//         button.addEventListener("click", function(event) {
//             event.preventDefault();
//             const row = event.target.closest("tr");
//             const orderId = row.dataset.id;
//             const currentStatus = row.querySelector(".order-status").textContent;

//             openStatusModal(orderId, currentStatus);
//         });
//     });
// //--------------------------------------------------------------------------------------------------------------
//     // Добавляем обработчики на кнопку "Просмотр"
//     document.querySelectorAll(".view-order").forEach(function(button) {
//         button.addEventListener("click", function(event) {
//             event.preventDefault();
//             const row = event.target.closest("tr");
//             const orderId = row.dataset.id;

//             openViewOrderModal(orderId);
//         });
//     });
// //--------------------------------------------------------------------------------------------------------------
//     // Обработка формы изменения статуса
//     statusForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const orderId = document.getElementById("orderId").value;
//         const newStatus = document.getElementById("orderStatus").value;

//         // Обновляем статус заказа в таблице
//         const row = document.querySelector(`tr[data-id='${orderId}']`);
//         row.querySelector(".order-status").textContent = newStatus;

//         // Закрываем модальное окно
//         statusModal.style.display = "none";
//     });
// });
// //--------------------------------------------------------------------------------------------------------------




// // Настройки админ-панели
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {

//     // Обработчик формы основных настроек
//     const basicSettingsForm = document.getElementById("basicSettingsForm");
//     basicSettingsForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const storeName = document.getElementById("storeName").value;
//         const storeEmail = document.getElementById("storeEmail").value;

//         console.log("Сохранение основных настроек:");
//         console.log("Название магазина:", storeName);
//         console.log("Email магазина:", storeEmail);

//         alert("Основные настройки сохранены!");
//     });

//     // Обработчик формы настроек доставки
//     const shippingSettingsForm = document.getElementById("shippingSettingsForm");
//     shippingSettingsForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const shippingCost = document.getElementById("shippingCost").value;
//         const freeShippingThreshold = document.getElementById("freeShippingThreshold").value;

//         console.log("Сохранение настроек доставки:");
//         console.log("Стоимость доставки:", shippingCost);
//         console.log("Бесплатная доставка от суммы:", freeShippingThreshold);

//         alert("Настройки доставки сохранены!");
//     });

//     // Обработчик изменения темы оформления
//     const themeSettingsForm = document.getElementById("themeSettingsForm");
//     themeSettingsForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const selectedTheme = document.getElementById("themeSelect").value;

//         console.log("Применение темы:", selectedTheme);

//         // Применение выбранной темы
//         if (selectedTheme === "dark") {
//             document.body.style.backgroundColor = "#333";
//             document.body.style.color = "white";
//         } else {
//             document.body.style.backgroundColor = "white";
//             document.body.style.color = "black";
//         }

//         alert("Тема изменена на " + (selectedTheme === "dark" ? "темную" : "светлую"));
//     });

//     // Обработчик настроек уведомлений
//     const notificationSettingsForm = document.getElementById("notificationSettingsForm");
//     notificationSettingsForm.addEventListener("submit", function(event) {
//         event.preventDefault();
//         const notifyOrders = document.getElementById("notifyOrders").checked;
//         const notifyUsers = document.getElementById("notifyUsers").checked;

//         console.log("Сохранение настроек уведомлений:");
//         console.log("Уведомления о новых заказах:", notifyOrders);
//         console.log("Уведомления о новых пользователях:", notifyUsers);

//         alert("Настройки уведомлений сохранены!");
//     });

// });
// //--------------------------------------------------------------------------------------------------------------




// // Настройки выхода из админ-панели
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {

//     // Обработчик для кнопки подтверждения выхода
//     const confirmLogoutBtn = document.getElementById('confirmLogout');
//     confirmLogoutBtn.addEventListener('click', function() {
//         // Здесь можно добавить логику для завершения сессии и перенаправления
//         console.log("Выход выполнен");
//         alert("Вы вышли из системы!");

//         // Перенаправление на страницу входа или главную страницу
//         window.location.href = "login.html"; // Замените на URL страницы входа
//     });

//     // Обработчик для кнопки отмены выхода
//     const cancelLogoutBtn = document.getElementById('cancelLogout');
//     cancelLogoutBtn.addEventListener('click', function() {
//         // Вернуться в админ-панель
//         window.location.href = "admin-dashboard.html"; // Замените на URL админ-панели
//     });

// });
// //--------------------------------------------------------------------------------------------------------------




// // Login
// //--------------------------------------------------------------------------------------------------------------
// document.addEventListener('DOMContentLoaded', function() {
//     const loginForm = document.getElementById('loginForm');
//     const loginError = document.getElementById('loginError');

//     // Пример правильных данных для демонстрации
//     const validUsername = 'admin';
//     const validPassword = 'admin123';

//     // Обработчик отправки формы
//     loginForm.addEventListener('submit', function(event) {
//         event.preventDefault(); // Предотвращаем перезагрузку страницы при отправке формы

//         const username = document.getElementById('username').value;
//         const password = document.getElementById('password').value;

//         // Проверяем, введены ли правильные логин и пароль
//         if (username === validUsername && password === validPassword) {
//             // Если логин и пароль верны, перенаправляем пользователя в админ-панель
//             window.location.href = 'admin-dashboard.html'; // Замените на реальный URL админ-панели
//         } else {
//             // Если данные неверны, показываем сообщение об ошибке
//             loginError.style.display = 'block';
//         }
//     });
// });
// //--------------------------------------------------------------------------------------------------------------
