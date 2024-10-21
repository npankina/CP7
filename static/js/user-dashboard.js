document.addEventListener('DOMContentLoaded', function() {
    const personalInfoForm = document.getElementById('personalInfoForm');
    const notificationSettingsForm = document.getElementById('notificationSettingsForm');

    // Обработка формы личной информации
    personalInfoForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;

        console.log("Сохранение личной информации:");
        console.log("ФИО:", fullName);
        console.log("Email:", email);

        alert("Личная информация сохранена!");
    });

    // Обработка формы настроек уведомлений
    notificationSettingsForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const notifyOrders = document.getElementById('notifyOrders').checked;
        const notifyPromotions = document.getElementById('notifyPromotions').checked;

        console.log("Сохранение настроек уведомлений:");
        console.log("Уведомления о заказах:", notifyOrders);
        console.log("Уведомления о специальных предложениях:", notifyPromotions);

        alert("Настройки уведомлений сохранены!");
    });
});
