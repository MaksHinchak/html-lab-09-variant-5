"use strict";

(() => {
  const recordings = {
    audio: [
      { file: "ready", title: "Сигнал готовності", description: "Три висхідні ноти. Власний синтезований сигнал." },
      { file: "sequence", title: "Послідовність частот", description: "Шість послідовних тонів. Власний синтезований приклад." }
    ],
    video: [
      { file: "movement", title: "Переміщення фігур", description: "Коло й верхній квадрат змінюють положення. Власний ролик, 4 секунди, без звукової доріжки." },
      { file: "transforms", title: "Обертання та масштаб", description: "Ромб обертається, праве коло змінює розмір. Власний ролик, 4 секунди, без звукової доріжки." }
    ]
  };
  const players = [document.getElementById("audio-player"), document.getElementById("video-player")];

  for (const kind of ["audio", "video"]) {
    const player = document.getElementById(`${kind}-player`);
    const select = document.getElementById(`${kind}-select`);
    const status = document.getElementById(`${kind}-status`);
    const form = document.getElementById(`${kind}-menu`);
    const message = text => { status.textContent = text; };
    function selectRecording() {
      const recording = recordings[kind][Number(select.value)];
      player.pause();
      const sources = player.querySelectorAll("source");
      sources[0].src = `assets/media/${recording.file}.${kind === "audio" ? "mp3" : "mp4"}`;
      if (kind === "video") {
        sources[1].src = `assets/media/${recording.file}.webm`;
        player.poster = `assets/media/${recording.file}-poster.png`;
      }
      document.getElementById(`${kind}-caption`).textContent = `${recording.title}. ${recording.description}`;
      document.getElementById(`${kind}-download`).href = sources[0].src;
      player.load();
      message(`Обрано «${recording.title}». Натисніть «Відтворити».`);
    }
    select.addEventListener("change", selectRecording);
    form.addEventListener("submit", async event => {
      event.preventDefault();
      try {
        await player.play();
      } catch (error) {
        message(error.name === "NotAllowedError" ? "Натисніть кнопку відтворення на самому програвачі." : "Не вдалося відтворити ресурс. Перевірте доступність файлу та підтримку формату.");
      }
    });
    player.addEventListener("play", () => {
      players.forEach(other => { if (other !== player) other.pause(); });
      message("Відтворення розпочато.");
    });
    player.addEventListener("pause", () => { if (!player.ended) message("Відтворення призупинено."); });
    player.addEventListener("ended", () => message("Відтворення завершено."));
    player.addEventListener("error", () => message("Файл не завантажився або його формат не підтримується."));
    form.querySelector("button[type=submit]").disabled = false;
  }
  document.getElementById("stop-media").addEventListener("click", () => {
    players.forEach(player => {
      player.pause();
      if (Number.isFinite(player.duration)) player.currentTime = 0;
    });
    document.getElementById("library-status").textContent = "Обидва програвачі зупинено й повернуто на початок.";
  });
  document.getElementById("stop-media").disabled = false;
})();
