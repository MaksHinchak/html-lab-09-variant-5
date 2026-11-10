"use strict";

const drawing = document.getElementById("animated-drawing");
const toggle = document.getElementById("toggle-animation");
const restart = document.getElementById("restart-animation");
const stateLabel = document.getElementById("animation-status");

function showState() {
  const paused = drawing.animationsPaused();
  toggle.textContent = paused ? "Продовжити" : "Пауза";
  toggle.setAttribute("aria-pressed", String(paused));
  stateLabel.textContent = paused ? "Анімацію призупинено." : "Анімація відтворюється.";
}

toggle.addEventListener("click", () => {
  if (drawing.animationsPaused()) drawing.unpauseAnimations();
  else drawing.pauseAnimations();
  showState();
});
restart.addEventListener("click", () => {
  drawing.setCurrentTime(0);
  drawing.unpauseAnimations();
  showState();
});
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) drawing.pauseAnimations();
toggle.disabled = false;
restart.disabled = false;
showState();
