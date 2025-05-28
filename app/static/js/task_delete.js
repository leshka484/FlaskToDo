let currentTaskId = null;

function openModal(taskId) {
    currentTaskId = taskId;
    document.getElementById("deleteModal").style.display = "block";
}

function closeModal() {
    document.getElementById("deleteModal").style.display = "none";
    currentTaskId = null;
}

document.getElementById("confirmDeleteBtn").addEventListener("click", () => {
    fetch(`/delete/${currentTaskId}`, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        }
    }).then(response => {
        if (response.ok) {
            document.getElementById(`task-${currentTaskId}`).remove();
        } else {
            alert("Ошибка при удалении.");
        }
        closeModal();
    });
});