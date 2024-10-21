document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('userLoginForm');
    const loginError = document.getElementById('loginError');

    // Пример правильных данных для демонстрации
    const validEmail = 'user@example.com';
    const validPassword = 'password123';

    // Обработчик отправки формы
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем перезагрузку страницы при отправке формы

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Проверяем, введены ли правильные email и пароль
        if (email === validEmail && password === validPassword) {
            // Если email и пароль верны, перенаправляем пользователя на страницу личного кабинета
            window.location.href = 'user-dashboard.html'; // Замените на реальный URL личного кабинета
        } else {
            // Если данные неверны, показываем сообщение об ошибке
            loginError.style.display = 'block';
        }
    });
});
