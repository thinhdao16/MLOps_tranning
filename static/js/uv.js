document.addEventListener("DOMContentLoaded", () => {
  const openModalButton = document.getElementById("openModal");
  const closeModalButton = document.getElementById("closeModal");
  const modal = document.getElementById("modal");
  const loading = document.getElementById("loading");
  const weatherForm = document.getElementById("weatherForm");

  // Mở modal
  openModalButton.addEventListener("click", () => {
    modal.classList.remove("hidden");
  });

  // Đóng modal
  closeModalButton.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  // Hiển thị loading khi gửi form
  weatherForm.addEventListener("submit", () => {
    modal.classList.add("hidden");
    loading.classList.remove("hidden");
  });
});
