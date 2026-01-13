let menu = document.querySelector("#menu-btn");
let navbar = document.querySelector(".navbar");

menu.onclick = () => {
  menu.classList.toggle("fa-times");
  navbar.classList.toggle("active");
};

window.onscroll = () => {
  menu.classList.remove("fa-times");
  navbar.classList.remove("active");
};

async function fetchNotifications() {
  try {
    const res = await fetch("http://127.0.0.1:8000/notifications");
    const data = await res.json();
    console.log(data); // see notifications in console
  } catch (err) {
    console.error(err);
  }
}

// Refresh every 60 seconds
setInterval(fetchNotifications, 60000);
