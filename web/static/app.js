/* ============================================================================
   PyBook front end.
   Alpine components (stepper, quiz, playground) + vanilla glue for the shell:
   theme, command palette, CodeMirror, charts, toasts, scroll spy.
   Everything talks to this origin only.
   ========================================================================== */
(function () {
  "use strict";

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------ utils */
  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
  }

  async function post(path, body) {
    try {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
        body: JSON.stringify(body || {}),
        credentials: "same-origin",
      });
      const data = await response.json().catch(() => ({ ok: false, error: "Bad response" }));
      data._status = response.status;
      return data;
    } catch (error) {
      return { ok: false, error: "Network error: " + error.message };
    }
  }

  function toast(message, kind) {
    const host = $("#toasts");
    if (!host) return;
    const el = document.createElement("div");
    el.className = "toast " + (kind || "");
    el.textContent = message;
    host.appendChild(el);
    setTimeout(() => {
      el.style.transition = "opacity .3s, transform .3s";
      el.style.opacity = "0";
      el.style.transform = "translateY(6px)";
      setTimeout(() => el.remove(), 320);
    }, 3200);
  }
  window.pybookToast = toast;

  function burst() {
    if (typeof window.confetti !== "function" || reduced) return;
    window.confetti({ particleCount: 90, spread: 74, startVelocity: 34, origin: { y: 0.72 }, scalar: 0.9 });
    setTimeout(() => window.confetti({ particleCount: 40, spread: 100, origin: { y: 0.6 }, scalar: 0.7 }), 180);
  }

  function cssVar(name, fallback) {
    const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return value || fallback;
  }

  /* ------------------------------------------------------------------ theme */
  const THEME_KEY = "pybook.theme";

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) { /* private mode */ }
    document.dispatchEvent(new CustomEvent("pybook:theme", { detail: theme }));
  }

  (function initTheme() {
    let saved = null;
    try { saved = localStorage.getItem(THEME_KEY); } catch (e) { /* ignore */ }
    const preferred = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    applyTheme(saved || preferred);
  })();

  document.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-theme-toggle]");
    if (!toggle) return;
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    toast(next === "dark" ? "Dark mode" : "Light mode");
  });

  /* ------------------------------------------------------------- rail toggle */
  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-rail-toggle]")) {
      document.body.classList.toggle("rail-open");
      return;
    }
    if (document.body.classList.contains("rail-open") && !event.target.closest("#rail")) {
      document.body.classList.remove("rail-open");
    }
  });

  /* ---------------------------------------------------------------- palette */
  const navData = (() => {
    const node = $("#nav-data");
    if (!node) return [];
    try { return JSON.parse(node.textContent); } catch (e) { return []; }
  })();

  const palette = $("#palette");
  const paletteInput = $("#palette-q");
  const paletteList = $("#palette-list");
  let paletteItems = [];
  let paletteIndex = 0;

  function renderPalette(query) {
    const q = (query || "").trim().toLowerCase();
    paletteItems = navData
      .filter((lesson) => !q || lesson.title.toLowerCase().includes(q) || lesson.id.includes(q))
      .slice(0, 40);
    paletteIndex = 0;
    paletteList.innerHTML = paletteItems
      .map((lesson, index) => {
        const label = lesson.u
          ? '<a href="/lesson/' + lesson.id + '">'
          : '<span>';
        const end = lesson.u ? "</a>" : "</span>";
        return (
          '<li class="' + (lesson.u ? "" : "locked ") + (index === 0 ? "sel" : "") + '">' +
          label +
          "<span>" + (lesson.u ? "○" : "🔒") + "</span>" +
          "<span>" + escapeHtml(lesson.title) + "</span>" +
          '<span class="pid">' + lesson.id + "</span>" +
          end +
          "</li>"
        );
      })
      .join("");
    if (!paletteItems.length) {
      paletteList.innerHTML = '<li><span class="muted">No lesson matches that.</span></li>';
    }
  }

  function escapeHtml(text) {
    return String(text == null ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function openPalette() {
    if (!palette || !navData.length) return;
    palette.hidden = false;
    paletteInput.value = "";
    renderPalette("");
    setTimeout(() => paletteInput.focus(), 30);
  }

  function closePalette() {
    if (!palette) return;
    palette.hidden = true;
  }

  function movePalette(delta) {
    if (!paletteItems.length) return;
    paletteIndex = (paletteIndex + delta + paletteItems.length) % paletteItems.length;
    $$("li", paletteList).forEach((li, index) => li.classList.toggle("sel", index === paletteIndex));
    const active = $$("li", paletteList)[paletteIndex];
    if (active) active.scrollIntoView({ block: "nearest" });
  }

  function choosePalette() {
    const lesson = paletteItems[paletteIndex];
    if (!lesson) return;
    if (!lesson.u) {
      toast("That lesson is still locked — finish the one before it.", "bad");
      return;
    }
    window.location.href = "/lesson/" + lesson.id;
  }

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-open-palette]")) {
      event.preventDefault();
      openPalette();
    }
    if (palette && !palette.hidden && event.target === palette) closePalette();
  });

  if (paletteInput) {
    paletteInput.addEventListener("input", () => renderPalette(paletteInput.value));
    paletteInput.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") { event.preventDefault(); movePalette(1); }
      else if (event.key === "ArrowUp") { event.preventDefault(); movePalette(-1); }
      else if (event.key === "Enter") { event.preventDefault(); choosePalette(); }
      else if (event.key === "Escape") { closePalette(); }
    });
  }

  document.addEventListener("keydown", (event) => {
    const meta = event.ctrlKey || event.metaKey;
    if (meta && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openPalette();
      return;
    }
    if (event.key === "Escape" && palette && !palette.hidden) closePalette();
    if (meta && event.key === "Enter") {
      const editor = event.target.closest(".editor, .CodeMirror");
      if (editor) {
        event.preventDefault();
        const article = editor.closest(".exercise") || editor.closest("section");
        const button = article && $('[data-act="check"], [data-play-run]', article);
        if (button) button.click();
      }
    }
  });

  /* --------------------------------------------------------------- language */
  const language = $("#language");
  if (language) {
    language.addEventListener("change", async () => {
      await post("/api/language", { language: language.value });
      window.location.reload();
    });
  }

  /* ----------------------------------------------------------------- course */
  const courseSwitch = $("[data-course-switch]");
  if (courseSwitch) {
    const initialCourse = courseSwitch.value;
    courseSwitch.addEventListener("change", async () => {
      if (courseSwitch.value === initialCourse) return;
      const response = await fetch("/switch/" + encodeURIComponent(courseSwitch.value), {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
      });
      if (response.ok) window.location.href = "/learn";
    });
  }

  /* --------------------------------------------------------------- CodeMirror */
  function makeEditor(textarea, options) {
    if (!window.CodeMirror) return null;
    const cm = window.CodeMirror.fromTextArea(textarea, Object.assign({
      mode: "python",
      theme: "material-darker",
      lineNumbers: true,
      lineWrapping: false,
      indentUnit: 4,
      tabSize: 4,
      autoCloseBrackets: true,
      matchBrackets: true,
      styleActiveLine: true,
      viewportMargin: Infinity,
      extraKeys: {
        Tab: (editor) => editor.execCommand("indentMore"),
        "Shift-Tab": (editor) => editor.execCommand("indentLess"),
        "Ctrl-Enter": () => {
          const article = cm.getWrapperElement().closest(".exercise, section");
          const button = article && $('[data-act="check"], [data-play-run]', article);
          if (button) button.click();
        },
      },
    }, options || {}));
    textarea._cm = cm;
    return cm;
  }

  function editorValue(element) {
    if (element._cm) return element._cm.getValue();
    return element.value;
  }

  function setEditorValue(element, value) {
    if (element._cm) element._cm.setValue(value);
    else element.value = value;
  }

  function bootEditors() {
    $$(".editor").forEach((textarea) => makeEditor(textarea));
  }

  /* ------------------------------------------------------------ run / check */
  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-act]");
    if (!button) return;
    const act = button.dataset.act;
    const exercise = button.closest(".exercise");

    if (act === "check" && exercise) {
      const host = $(".result", exercise);
      const editor = $(".editor", exercise);
      button.disabled = true;
      button.textContent = "Checking…";
      const data = await post("/api/check/" + exercise.dataset.exercise, {
        code: editorValue(editor),
      });
      button.disabled = false;
      button.textContent = "Check my code";
      host.hidden = false;
      host.className = "result " + (data.passed ? "ok" : "bad");
      if (!data.ok && data.error) {
        host.innerHTML = "<h4>Your code raised an error</h4><pre class=\"code-wrap\"><code>" +
          escapeHtml(data.error) + "</code></pre>";
        toast("Not yet — read the error above", "bad");
        return;
      }
      const list = (data.checks || [])
        .map((check) =>
          '<li class="' + (check.ok ? "pass" : "fail") + '">' +
          (check.ok ? "✓" : "✗") + " check " + check.n +
          (check.error ? " — " + escapeHtml(check.error) : "") + "</li>")
        .join("");
      host.innerHTML =
        "<h4>" + (data.passed ? "All checks passed 🎉" : "Not correct yet") + "</h4>" +
        '<ul class="check-list">' + list + "</ul>" +
        (data.passed ? "" : '<p class="small muted">Hint: ' + escapeHtml(data.hint || "") + "</p>");
      if (data.passed) {
        burst();
        toast("Exercise solved", "ok");
        exercise.classList.add("is-done");
        const state = $("[data-state]", exercise);
        if (state) state.textContent = "solved ✓";
        const pill = $("#practice-pill");
        if (pill && data.practice) {
          pill.textContent = data.practice.done + "/" + data.practice.total + " solved";
          pill.classList.toggle("strong", data.practice.done === data.practice.total);
        }
        if (data.ready) {
          window.dispatchEvent(new CustomEvent("pybook:practice"));
          toast("Required practice complete — quiz unlocked", "ok");
        }
      }
      return;
    }

    if (act === "hint" && exercise) {
      const hint = $(".hint-text", exercise);
      if (hint) hint.hidden = !hint.hidden;
      return;
    }

    if (act === "reset") {
      if (!window.confirm("Erase all your progress on this machine? This cannot be undone.")) return;
      await post("/api/reset", {});
      window.location.reload();
      return;
    }
  });

  /* --------------------------------------------------------------- snippets */
  const SNIPPETS = {
    loop: 'for i in range(1, 6):\n    print(i, "x 7 =", i * 7)\n',
    dict: 'ages = {"asha": 21, "ravi": 24}\nfor name, age in ages.items():\n    print(f"{name} is {age}")\n',
    func: 'def area(width, height=2):\n    return width * height\n\nprint(area(5))\nprint(area(5, 4))\n',
    class: 'class Counter:\n    def __init__(self):\n        self.n = 0\n\n    def add(self):\n        self.n += 1\n        return self.n\n\nc = Counter()\nprint(c.add(), c.add())\n',
    try: 'raw = "abc"\ntry:\n    print(int(raw))\nexcept ValueError as error:\n    print("not a number:", error)\nfinally:\n    print("done")\n',
  };

  document.addEventListener("click", (event) => {
    const chip = event.target.closest("[data-snippet]");
    if (!chip) return;
    const editor = $("#play-code");
    if (!editor) return;
    setEditorValue(editor, SNIPPETS[chip.dataset.snippet] || "");
  });

  /* ------------------------------------------------------------- scroll spy */
  function bootScrollSpy() {
    const nav = $("#step-nav");
    if (!nav) return;
    const links = $$("a", nav);
    const sections = links
      .map((link) => $(link.getAttribute("href")))
      .filter(Boolean);
    if (!sections.length || !("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          links.forEach((link) =>
            link.classList.toggle("on", link.getAttribute("href") === "#" + entry.target.id)
          );
        });
      },
      { rootMargin: "-90px 0px -60% 0px", threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
  }

  /* --------------------------------------------------------------- filters */
  function bootFilters() {
    const buttons = $$("[data-filter]");
    if (!buttons.length) return;
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        buttons.forEach((other) => other.classList.toggle("on", other === button));
        const want = button.dataset.filter;
        $$("#module-table .tr[data-state]").forEach((row) => {
          row.classList.toggle("hidden", want !== "all" && row.dataset.state !== want);
        });
      });
    });
  }

  /* ---------------------------------------------------------------- charts */
  let charts = [];

  function buildCharts() {
    if (typeof window.Chart !== "function") return;
    const node = $("#stats-data");
    if (!node) return;
    let stats;
    try { stats = JSON.parse(node.textContent); } catch (e) { return; }

    charts.forEach((chart) => chart.destroy());
    charts = [];

    const accent = cssVar("--accent", "#4f46e5");
    const accent2 = cssVar("--accent-2", "#0ea5e9");
    const green = cssVar("--green", "#0f9d58");
    const line = cssVar("--line", "#e4e9f2");
    const ink = cssVar("--ink", "#0b1220");
    const muted = cssVar("--muted", "#5a6b85");
    const surface = cssVar("--surface", "#fff");

    window.Chart.defaults.font.family = cssVar("--sans", "system-ui");
    window.Chart.defaults.color = muted;

    const donut = $("#chart-donut");
    if (donut) {
      charts.push(new window.Chart(donut, {
        type: "doughnut",
        data: {
          labels: ["Passed", "Remaining"],
          datasets: [{
            data: [stats.lessons_done, Math.max(0, stats.lessons_total - stats.lessons_done)],
            backgroundColor: [accent, line],
            borderColor: surface,
            borderWidth: 2,
            hoverOffset: 6,
          }],
        },
        options: {
          cutout: "72%",
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { enabled: true } },
        },
      }));
    }

    const modules = $("#chart-modules");
    if (modules) {
      charts.push(new window.Chart(modules, {
        type: "bar",
        data: {
          labels: stats.modules.map((module) => module.title),
          datasets: [
            {
              label: "Average lesson score %",
              data: stats.modules.map((module) => module.avg),
              backgroundColor: stats.modules.map((module) =>
                module.passed ? green : module.unlocked ? accent : line
              ),
              borderRadius: 6,
              maxBarThickness: 34,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, max: 100, ticks: { stepSize: 25 }, grid: { color: line } },
            x: { grid: { display: false }, ticks: { maxRotation: 0, autoSkip: true } },
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                afterLabel: (item) => {
                  const module = stats.modules[item.dataIndex];
                  return module.done + "/" + module.total + " lessons · exam " +
                    (module.exam || 0) + "% · skip " + (module.skip || 0) + "%";
                },
              },
            },
          },
          onClick: (event, elements) => {
            if (!elements.length) return;
            const module = stats.modules[elements[0].index];
            window.location.href = "/learn#" + module.id;
          },
        },
      }));
    }

    const activity = $("#chart-activity");
    if (activity) {
      charts.push(new window.Chart(activity, {
        type: "line",
        data: {
          labels: stats.activity.map((day) => day.label),
          datasets: [{
            label: "Activity",
            data: stats.activity.map((day) => day.count),
            borderColor: accent2,
            backgroundColor: "color-mix(in srgb, " + accent2 + " 22%, transparent)",
            fill: true,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: accent2,
          }],
        },
        options: {
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: line } },
            x: { grid: { display: false }, ticks: { maxRotation: 0, autoSkip: true } },
          },
          plugins: { legend: { display: false } },
        },
      }));
    }

    void ink;
  }

  document.addEventListener("pybook:theme", () => buildCharts());

  /* ------------------------------------------------------------ animations */
  function animateIn() {
    if (!window.gsap || reduced) return;
    const targets = $$("[data-animate]");
    if (!targets.length) return;
    window.gsap.from(targets, {
      y: 16,
      opacity: 0,
      duration: 0.55,
      stagger: 0.055,
      ease: "power2.out",
      clearProps: "all",
    });
  }

  /* ------------------------------------------------------------------- boot */
  function boot() {
    bootEditors();
    bootScrollSpy();
    bootFilters();
    buildCharts();
    animateIn();

    const current = $(".trail-item.current");
    const rail = $("#rail");
    if (current && rail) {
      const top = current.offsetTop - rail.clientHeight / 2 + current.offsetHeight / 2;
      rail.scrollTo({ top: Math.max(0, top) });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  /* ====================================================== Alpine components */
  document.addEventListener("alpine:init", () => {
    const Alpine = window.Alpine;
    if (!Alpine) return;

    Alpine.data("stepper", () => ({
      lesson: "",
      number: 1,
      lines: [],
      steps: [],
      stdout: "",
      error: "",
      ok: true,
      ran: false,
      busy: false,
      index: 0,
      playing: false,
      timer: null,

      init(number, codeText) {
        this.number = number;
        this.lesson = (this.$el.dataset && this.$el.dataset.lesson) || "";
        this.lines = String(codeText || "").replace(/\n$/, "").split("\n");
      },

      get step() {
        return this.steps[this.index] || { line: 0, vars: {}, out: 0 };
      },
      get vars() {
        const values = this.step.vars || {};
        return Object.keys(values).map((name) => ({ name: name, value: values[name] }));
      },
      get out() {
        return (this.stdout || "").slice(0, this.step.out || 0);
      },
      get display() {
        if (this.ok) return this.stdout || "nothing was printed";
        return this.error + (this.error_line ? "\n(line " + this.error_line + ")" : "");
      },

      async run() {
        this.busy = true;
        const data = await post("/api/run", { code: this.lines.join("\n") });
        this.busy = false;
        this.ok = !!data.ok;
        this.stdout = data.stdout || "";
        this.error = data.error || "";
        this.error_line = data.error_line;
        this.ran = true;
        if (!data.ok) toast("That raised an error", "bad");
      },

      async trace() {
        this.busy = true;
        const data = await post("/api/trace/" + this.lesson + "/" + this.number, {});
        this.busy = false;
        if (!data.ok) {
          toast(data.error || "Could not trace that example", "bad");
          return;
        }
        this.steps = data.steps || [];
        this.stdout = data.stdout || "";
        this.index = 0;
        this.ran = false;
        if (!this.steps.length) toast("Nothing to step through here", "bad");
      },

      prev() { this.stop(); this.index = Math.max(0, this.index - 1); },
      next() { this.stop(); this.index = Math.min(this.steps.length - 1, this.index + 1); },
      stop() {
        this.playing = false;
        if (this.timer) { clearInterval(this.timer); this.timer = null; }
      },
      toggle() {
        if (this.playing) { this.stop(); return; }
        if (!this.steps.length) return;
        this.playing = true;
        this.timer = setInterval(() => {
          if (this.index >= this.steps.length - 1) { this.stop(); return; }
          this.index += 1;
        }, 700);
      },
    }));

    Alpine.data("playground", () => ({
      lines: [],
      steps: [],
      stdout: "",
      error: "",
      ok: true,
      ran: false,
      busy: false,
      index: 0,
      playing: false,
      timer: null,

      get step() {
        return this.steps[this.index] || { line: 0, vars: {}, out: 0 };
      },
      get vars() {
        const values = this.step.vars || {};
        return Object.keys(values).map((name) => ({ name: name, value: values[name] }));
      },
      get out() {
        return (this.stdout || "").slice(0, this.step.out || 0);
      },
      get display() {
        if (this.ok) return this.stdout || "nothing was printed";
        return this.error + (this.error_line ? "\n(line " + this.error_line + ")" : "");
      },

      code() {
        const editor = $("#play-code");
        if (!editor) return "";
        return editorValue(editor);
      },
      syncLines(code) {
        this.lines = String(code || "").replace(/\n$/, "").split("\n");
      },
      async run() {
        if (this.busy) return;
        this.busy = true;
        const code = this.code();
        this.syncLines(code);
        const data = await post("/api/run", { code: code });
        this.busy = false;
        this.ok = !!data.ok;
        this.stdout = data.stdout || "";
        this.error = data.error || "";
        this.error_line = data.error_line;
        this.steps = [];
        this.playing = false;
        this.ran = true;
        if (!data.ok) toast("That raised an error", "bad");
      },
      async trace() {
        if (this.busy) return;
        this.busy = true;
        const code = this.code();
        this.syncLines(code);
        const data = await post("/api/run", { code: code, trace: true });
        this.busy = false;
        if (!data.ok) {
          toast(data.error || "Could not trace that", "bad");
          return;
        }
        this.steps = data.steps || [];
        this.stdout = data.stdout || "";
        this.index = 0;
        this.ran = false;
        this.playing = false;
        if (!this.steps.length) toast("Nothing to step through — try code with statements", "bad");
      },
      clear() {
        const editor = $("#play-code");
        if (editor) setEditorValue(editor, "");
        this.steps = [];
        this.stdout = "";
        this.error = "";
        this.error_line = null;
        this.ran = false;
        this.playing = false;
      },
      prev() { this.stop(); this.index = Math.max(0, this.index - 1); },
      next() { this.stop(); this.index = Math.min(this.steps.length - 1, this.index + 1); },
      stop() {
        this.playing = false;
        if (this.timer) { clearInterval(this.timer); this.timer = null; }
      },
      toggle() {
        if (this.playing) { this.stop(); return; }
        if (!this.steps.length) return;
        this.playing = true;
        this.timer = setInterval(() => {
          if (this.index >= this.steps.length - 1) { this.stop(); return; }
          this.index += 1;
        }, 700);
      },
    }));

    Alpine.data("drill", () => ({
      id: "",
      kind: "",
      title: "",
      prompt: "",
      code: "",
      pool: [],
      options: [],
      hint: "",
      xp: 5,
      typed: "",
      sequence: [],
      used: [],
      passed: false,
      busy: false,
      message: "",
      showHint: false,
      lesson: "",

      init(payload) {
        Object.assign(this, payload || {});
        const host = this.$el.closest("[data-lesson]");
        this.lesson = host ? host.dataset.lesson : "";
        if (this.kind === "order") this.sequence = [];
      },

      add(line) {
        if (this.passed || this.used.includes(line.id)) return;
        this.used.push(line.id);
        this.sequence.push(line);
      },
      removeAt(index) {
        const line = this.sequence.splice(index, 1)[0];
        if (line) this.used = this.used.filter((id) => id !== line.id);
      },
      payload() {
        if (this.kind === "order") return this.sequence.map((line) => line.text);
        return this.typed;
      },
      async check() {
        if (this.busy || this.passed) return;
        if (this.kind === "order" && !this.sequence.length) {
          this.message = "Add at least one line first.";
          return;
        }
        this.busy = true;
        const data = await post("/api/drill/" + this.lesson, {
          drill_id: this.id,
          answer: this.payload(),
        });
        this.busy = false;
        this.message = data.message || data.error || "";
        if (data.passed) {
          this.passed = true;
          burst();
          toast("+" + data.xp + " XP · " + this.title, "ok");
          window.dispatchEvent(new CustomEvent("pybook:xp", { detail: data.xp_total }));
        }
      },
    }));

    Alpine.data("quiz", (config) => ({
      config: config || {},
      answers: {},
      result: null,
      busy: false,
      ready: !!(config && config.ready),

      init() {
        window.addEventListener("pybook:practice", () => {
          this.ready = true;
        });
      },

      get answered() {
        return Object.values(this.answers).filter(Boolean).length;
      },

      optionClass(name, letter) {
        if (!this.result || !this.result.ok) return "";
        const number = Number(String(name).replace("q", ""));
        const missed = (this.result.detail || []).find((entry) => entry.number === number);
        const chosen = this.answers[name];
        if (!missed) return chosen === letter ? "correct" : "";
        if (letter === missed.answer) return "correct";
        if (letter === chosen) return "wrong";
        return "";
      },

      async submit() {
        if (this.busy) return;
        if (!this.ready) {
          toast("Finish the required practice first", "bad");
          return;
        }
        this.busy = true;
        const isExam = this.config.exam;
        const url = isExam ? "/api/exam/" + this.config.exam : "/api/quiz/" + this.config.lesson;
        const body = isExam
          ? { answers: this.answers, skip: !!this.config.skip }
          : this.answers;
        const data = await post(url, body);
        this.busy = false;
        this.result = data;
        if (!data.ok) {
          toast(data.message || data.error || "Could not submit", "bad");
          return;
        }
        if (data.passed) {
          burst();
          toast(isExam ? "Module passed" : "Lesson passed", "ok");
        } else {
          toast("Not yet — read the explanations", "bad");
        }
      },
    }));
  });
})();
