"use strict";

const form = document.getElementById("order-form");
const product = document.getElementById("product");
const quantity = document.getElementById("quantity");
const search = document.getElementById("product-search");
const progress = document.getElementById("form-progress");
const meter = document.getElementById("stock-meter");
const result = document.getElementById("order-result");
const status = document.getElementById("validation-status");
const requiredFields = [...form.querySelectorAll("[required]")];
const options = [...product.querySelectorAll("option[data-price]")];
const currency = new Intl.NumberFormat("uk-UA", { maximumFractionDigits: 0 });
const money = value => `${currency.format(value)} грн`;

function checkText() {
  for (const id of ["customer", "request"]) {
    const field = document.getElementById(id);
    field.setCustomValidity(field.value && field.value.trim().length < field.minLength
      ? `Введіть щонайменше ${field.minLength} символів без урахування крайніх пробілів.` : "");
  }
}

function refresh() {
  checkText();
  const selected = product.selectedOptions[0];
  const stock = Number(selected?.dataset.stock || 30);
  const price = Number(selected?.dataset.price || 0);
  quantity.max = String(stock);
  const count = Number(quantity.value);
  const validCount = quantity.validity.valid && Number.isInteger(count);
  document.getElementById("total").value = money(validCount ? price * count : 0);
  document.getElementById("stock-hint").textContent = price
    ? `У наявності ${stock} шт. Можна замовити від 1 до ${stock}.`
    : "Оберіть модель, щоб побачити залишок.";
  meter.max = stock;
  meter.high = Math.ceil(stock * .8);
  meter.value = price && Number.isFinite(count) ? Math.max(0, Math.min(count, stock)) : 0;
  meter.textContent = `${meter.value} із ${stock}`;
  progress.max = requiredFields.length;
  progress.value = requiredFields.filter(field => field.validity.valid).length;
  document.getElementById("progress-text").textContent = `${progress.value} із ${progress.max}`;
}

function filterProducts() {
  const query = search.value.trim().toLocaleLowerCase("uk-UA");
  let visible = 0;
  for (const option of options) {
    const matches = option.textContent.toLocaleLowerCase("uk-UA").includes(query);
    option.hidden = !matches;
    option.disabled = !matches;
    if (matches) visible++;
  }
  for (const group of product.querySelectorAll("optgroup")) {
    group.hidden = [...group.children].every(option => option.hidden);
  }
  if (product.selectedOptions[0]?.disabled) product.value = "";
  document.getElementById("search-status").textContent = visible
    ? `Знайдено моделей: ${visible}.` : "Збігів немає. Змініть пошуковий запит.";
}

form.addEventListener("input", event => {
  if (event.target === search) filterProducts();
  result.hidden = true;
  status.textContent = "";
  refresh();
});
form.addEventListener("change", () => { result.hidden = true; refresh(); });
form.addEventListener("invalid", () => {
  result.hidden = true;
  status.textContent = "Перевірте обов’язкові поля та формат введених даних.";
}, true);
form.addEventListener("submit", event => {
  event.preventDefault();
  refresh();
  if (!form.reportValidity()) return;
  const selected = product.selectedOptions[0];
  const entries = [
    ["Покупець", form.elements.customer.value.trim()],
    ["Email", form.elements.email.value],
    ["Телефон", form.elements.phone.value],
    ["Товар", selected.textContent.split(" — ")[0]],
    ["Кількість", `${quantity.value} шт.`],
    ["Вартість товарів", money(Number(selected.dataset.price) * Number(quantity.value))],
    ["Отримання", form.elements.delivery.selectedOptions[0].textContent],
    ["Тиждень", form.elements.week.value || "Не вказано"],
    ["Місяць", form.elements.month.value || "Не вказано"],
    ["Сайт компанії", form.elements.website.value || "Не вказано"],
    ["Пакування для перероблення", form.elements.packaging.checked ? "Так" : "Ні"],
    ["Побажання", form.elements.request.value.trim()]
  ];
  const details = document.getElementById("result-details");
  details.replaceChildren();
  for (const [label, value] of entries) {
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value;
    details.append(term, description);
  }
  document.getElementById("result-message").textContent = "Форма заповнена правильно. Це локальний підсумок: дані не надіслано на сервер.";
  status.textContent = "";
  result.hidden = false;
  result.scrollIntoView({ behavior: "smooth", block: "start" });
});
form.addEventListener("reset", () => {
  result.hidden = true;
  status.textContent = "";
  setTimeout(() => { filterProducts(); refresh(); }, 0);
});
for (const id of ["submit-order", "preview-order"]) document.getElementById(id).disabled = false;
refresh();
