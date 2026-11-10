"use strict";

(() => {
  const key = "bytemarket-lab7-events";
  let entries = [];
  try {
    const saved = JSON.parse(sessionStorage.getItem(key) || "[]");
    if (Array.isArray(saved)) entries = saved.filter(item => typeof item === "string").slice(-40);
  } catch { /* Журнал працює і без доступу до сховища. */ }

  function render() {
    const list = document.getElementById("event-log");
    if (!list) return;
    list.replaceChildren(...entries.slice().reverse().map(entry => {
      const item = document.createElement("li");
      item.textContent = entry;
      return item;
    }));
  }

  function record(type, message) {
    const time = new Date().toLocaleTimeString("uk-UA");
    const page = location.pathname.split("/").pop() || "index.html";
    entries.push(`${time} · ${page} · ${type}: ${message}`);
    entries = entries.slice(-40);
    try { sessionStorage.setItem(key, JSON.stringify(entries)); } catch { /* Необов’язкове сховище. */ }
    render();
    const status = document.getElementById("interaction-status");
    if (status) status.textContent = `${type}: ${message}`;
  }

  window.LabEvents = { record };
  if (!document.body.hasAttribute("onload")) {
    window.addEventListener("load", () => record("load", "Сторінку повністю завантажено."));
    window.addEventListener("pagehide", () => record("pagehide", "Вихід зі сторінки."));
  }
  document.querySelectorAll("h1, h2, h3, h4, h5, h6, b, i").forEach(element => {
    element.classList.add("event-text");
    element.tabIndex = 0;
    const name = `${element.tagName.toLowerCase()} «${element.textContent.trim().slice(0, 45)}»`;
    element.addEventListener("mouseenter", () => {
      element.classList.add("event-hover");
      record("mouseenter", `Курсор над ${name}.`);
    });
    element.addEventListener("mouseleave", () => {
      element.classList.remove("event-hover", "event-pressed");
      record("mouseleave", `Курсор залишив ${name}.`);
    });
    element.addEventListener("mousedown", () => element.classList.add("event-pressed"));
    element.addEventListener("mouseup", () => element.classList.remove("event-pressed"));
    const toggle = () => {
      element.classList.toggle("event-selected");
      record("click", `Змінено виділення ${name}.`);
    };
    element.addEventListener("click", toggle);
    element.addEventListener("dblclick", () => {
      element.classList.toggle("event-alternate");
      record("dblclick", `Змінено оформлення ${name}.`);
    });
    element.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggle();
      }
    });
  });

  document.querySelectorAll("img[data-mouse-demo], img.main-image").forEach(image => {
    image.classList.add("event-image");
    image.tabIndex = 0;
    image.setAttribute("role", "button");
    image.setAttribute("aria-pressed", "false");
    image.setAttribute("aria-label", `${image.alt}. Натисніть, щоб змінити масштаб.`);
    const toggle = () => {
      const selected = image.classList.toggle("image-selected");
      image.setAttribute("aria-pressed", String(selected));
      record("image click", `${image.alt}: ${selected ? "збільшено" : "початковий розмір"}.`);
    };
    image.addEventListener("mouseenter", () => record("image mouseenter", `Наведення: ${image.alt}.`));
    image.addEventListener("mouseleave", () => record("image mouseleave", `Курсор залишив зображення: ${image.alt}.`));
    image.addEventListener("click", toggle);
    image.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); toggle(); }
    });
  });

  document.getElementById("clear-events")?.addEventListener("click", () => {
    entries = [];
    try { sessionStorage.removeItem(key); } catch { /* Необов’язкове сховище. */ }
    render();
    document.getElementById("interaction-status").textContent = "Журнал очищено.";
  });
  render();
})();
