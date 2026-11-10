"use strict";

(() => {
  const canvas = document.getElementById("drawing-canvas");
  const context = canvas.getContext("2d");
  const status = document.getElementById("canvas-status");
  if (!context) {
    status.textContent = "Браузер не підтримує двовимірний Canvas.";
    return;
  }
  const figures = [
    { name: "Ліве коло", kind: "circle", x: -2, y: 1 },
    { name: "Праве коло", kind: "circle", x: 1, y: 1 },
    { name: "Лівий прямокутник", kind: "rect", x: -2, y: -.5, width: 2, height: 1 },
    { name: "Верхній квадрат", kind: "rect", x: 2.5, y: 1.5, width: 1, height: 1 },
    { name: "Квадрат сходинки", kind: "rect", x: 3.5, y: .5, width: 1, height: 1 },
    { name: "Нижній лівий квадрат", kind: "rect", x: .5, y: -1.5, width: 1, height: 1 },
    { name: "Нижній прямокутник", kind: "rect", x: 2, y: -2.5, width: 2, height: 1 },
    { name: "Нижній правий квадрат", kind: "rect", x: 4.5, y: -1.5, width: 1, height: 1 },
    { name: "Ромб", kind: "diamond", x: 3, y: -1 }
  ];
  const transforms = figures.map(() => ({ dx: 0, dy: 0, angle: 0, scale: 1 }));
  const form = document.getElementById("canvas-controls");
  const select = document.getElementById("figure-select");
  const fields = ["dx", "dy", "angle", "scale"];
  const logicalWidth = 780;
  const logicalHeight = 540;

  function axes() {
    context.strokeStyle = "black";
    context.fillStyle = "black";
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(38, 245); context.lineTo(736, 245);
    context.moveTo(290, 493); context.lineTo(290, 35);
    for (let x = -3; x <= 5; x++) {
      if (x === 0) continue;
      const px = 290 + 72 * x;
      context.moveTo(px, 235); context.lineTo(px, 255);
    }
    for (let y = -3; y <= 2; y++) {
      if (y === 0) continue;
      const py = 245 - 72 * y;
      context.moveTo(280, py); context.lineTo(300, py);
    }
    context.stroke();
    context.beginPath();
    context.moveTo(736, 245); context.lineTo(724, 239); context.lineTo(724, 251); context.closePath();
    context.moveTo(290, 35); context.lineTo(284, 47); context.lineTo(296, 47); context.closePath();
    context.fill();
    context.font = "23px 'Times New Roman', serif";
    context.textAlign = "center";
    for (let x = -3; x <= 5; x++) {
      if (x !== 0 && x !== -2) context.fillText(String(x), 290 + 72 * x, 274);
    }
    context.textAlign = "right";
    context.fillText("0", 278, 274);
    for (let y = -3; y <= 2; y++) {
      if (y !== 0) context.fillText(String(y), 277, 253 - 72 * y);
    }
    context.textAlign = "left";
    context.fillText("X", 748, 274); context.fillText("Y", 310, 45);
  }

  function draw() {
    const ratio = Math.min(window.devicePixelRatio || 1, 3);
    canvas.width = Math.round(logicalWidth * ratio);
    canvas.height = Math.round(logicalHeight * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.fillStyle = "white";
    context.fillRect(0, 0, logicalWidth, logicalHeight);
    context.save();
    context.translate(290, 245);
    context.scale(72, -72);
    figures.forEach((figure, index) => {
      const change = transforms[index];
      context.save();
      context.translate(figure.x + change.dx, figure.y + change.dy);
      context.rotate(change.angle * Math.PI / 180);
      context.scale(change.scale, change.scale);
      context.beginPath();
      if (figure.kind === "circle") context.arc(0, 0, 1, 0, 2 * Math.PI);
      if (figure.kind === "rect") context.rect(-figure.width / 2, -figure.height / 2, figure.width, figure.height);
      if (figure.kind === "diamond") {
        context.moveTo(-1, 0); context.lineTo(0, 1);
        context.lineTo(1, 0); context.lineTo(0, -1); context.closePath();
      }
      context.fillStyle = "#0000ff";
      context.strokeStyle = "black";
      context.lineWidth = .025;
      context.fill(); context.stroke();
      context.restore();
    });
    context.restore();
    axes();
  }

  function refreshFields() {
    const change = transforms[Number(select.value)];
    fields.forEach(name => {
      document.getElementById(name).value = String(change[name]);
    });
  }
  select.addEventListener("change", refreshFields);
  form.addEventListener("submit", event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const index = Number(select.value);
    fields.forEach(name => {
      transforms[index][name] = Number(document.getElementById(name).value);
    });
    draw();
    status.textContent = `${figures[index].name}. Зсув (${transforms[index].dx}; ${transforms[index].dy}), кут ${transforms[index].angle}°, масштаб ${transforms[index].scale}.`;
  });
  document.getElementById("canvas-reset").addEventListener("click", () => {
    transforms.forEach(change => Object.assign(change, { dx: 0, dy: 0, angle: 0, scale: 1 }));
    refreshFields(); draw();
    status.textContent = "Відновлено початкові координати всіх 9 фігур.";
  });
  window.addEventListener("resize", draw);
  form.querySelectorAll("button").forEach(button => { button.disabled = false; });
  draw();
})();
