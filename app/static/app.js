const form = document.getElementById("nickname-form");
if (form) {
  const input = document.getElementById("nickname");
  const saved = localStorage.getItem("studydeck_nickname");
  if (saved) input.value = saved;
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const nickname = input.value.trim();
    if (nickname) {
      localStorage.setItem("studydeck_nickname", nickname);
      window.location.href = `/?nickname=${encodeURIComponent(nickname)}`;
    }
  });
}
