// Автоматически скрыть flash-сообщения
document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll(".flash");
    flashMessages.forEach(msg => {
        setTimeout(() => {
        msg.classList.add("fade-out");
        setTimeout(() => msg.remove(), 500);  // Удаляем после анимации
      }, 3000);  // 3 секунды на показ
    });
    });