document.addEventListener('DOMContentLoaded', () => {
    // Найти все уведомления
    const alerts = document.querySelectorAll('.alert');

    // Функция для скрытия уведомления с плавным эффектом
    function hideAlert(alert) {
        alert.style.transition = 'opacity 0.5s ease-out';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500); // Удаление элемента после завершения анимации
    }

    // Закрыть каждое уведомление через 5 секунд
    alerts.forEach(alert => {
        setTimeout(() => hideAlert(alert), 5000);
    });
});
