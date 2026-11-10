"use strict";

(() => {
  function describe(value) {
    if (value === null) return "null";
    if (typeof value === "function") return `[функція ${value.name || "без назви"}]`;
    if (typeof value === "string") return JSON.stringify(value.length > 160 ? value.slice(0, 160) + "…" : value);
    if (typeof value !== "object") return String(value);
    return Object.prototype.toString.call(value);
  }

  document.getElementById("document-form").addEventListener("submit", event => {
    event.preventDefault();
    const names = new Set();
    for (const name in document) names.add(name);
    for (let object = document; object !== null; object = Object.getPrototypeOf(object)) {
      for (const name of Reflect.ownKeys(object)) names.add(name);
    }
    const lines = [...names].sort((a, b) => String(a).localeCompare(String(b))).map(name => {
      try { return `${String(name)} = ${describe(Reflect.get(document, name))}`; }
      catch (error) { return `${String(name)} = [недоступно: ${error.name}]`; }
    });
    document.getElementById("document-result").value =
      `Властивості document: ${names.size}\nСторінка: ${document.URL}\n\n${lines.join("\n")}`;
    document.getElementById("document-status").textContent = `Знайдено ${names.size} властивостей. Повні рядки доступні у полі нижче; довгі значення скорочено.`;
    window.LabEvents.record("Run Task", `Виведено ${names.size} властивостей document.`);
  });

  document.getElementById("search-form").addEventListener("submit", event => {
    event.preventDefault();
    const text = document.getElementById("search-text").value.normalize("NFC");
    const words = text.match(/\p{L}[\p{L}\p{M}]*(?:['’ʼ-]\p{L}[\p{L}\p{M}]*)*/gu) || [];
    const matches = words.filter(word => /^п[\s\S]*я$/iu.test(word));
    document.getElementById("search-result").value =
      `Знайдено: ${matches.length}\n${matches.length ? matches.join("\n") : "Слів на «п…я» немає."}`;
    window.LabEvents.record("Пошук", `Знайдено ${matches.length} слів на «п…я».`);
  });

  document.getElementById("array-form").addEventListener("submit", event => {
    event.preventDefault();
    const field = document.getElementById("array-input");
    field.setCustomValidity("");
    const tokens = field.value.trim().split(/[\s,;]+/u).filter(Boolean);
    const decimal = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/iu;
    if (!tokens.length || tokens.some(token => !decimal.test(token) || !Number.isFinite(Number(token)))) {
      const message = "Введіть скінченні числа через пробіл, кому або крапку з комою. Десятковий знак - крапка.";
      field.setCustomValidity(message);
      field.reportValidity();
      document.getElementById("array-result").value = message;
      return;
    }
    const a = tokens.map(Number);
    const b = a.filter(value => value !== 0);
    document.getElementById("array-result").value =
      `A = [${a.join(", ")}]\nN = ${a.length}\nB = [${b.join(", ")}]\nРозмір B = ${b.length}\nВилучено нулів: ${a.length - b.length}`;
    window.LabEvents.record("Array Task", `Із ${a.length} елементів залишено ${b.length}.`);
  });
  document.getElementById("array-input").addEventListener("input", event => event.target.setCustomValidity(""));
  document.querySelectorAll("form[data-task]").forEach(form => {
    form.querySelector("button[type=submit]").disabled = false;
    form.addEventListener("reset", () => {
      form.querySelector("textarea[readonly]").value = "";
      const status = form.querySelector("[role=status]");
      if (status) status.textContent = "";
      document.getElementById("array-input").setCustomValidity("");
    });
  });
})();
