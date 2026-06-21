/**
 * pitch.js — v5
 * Controles:
 *   Espaço → próximo elemento; quando todos exibidos, avança a tela
 *   →      → pula para a próxima tela
 *   ←      → volta para a tela anterior
 *   R      → reinicia a seleção de roteiro (volta à página 1)
 *
 * Cada página define window.PITCH com:
 *   { next, prev, page, total, init(gsap), steps: [{animate(gsap), subtitle}] }
 * As legendas são sobrescritas pelo roteiro selecionado em window.ROTEIROS.
 */

(function () {
  const GSAP_CDN     = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js';
  const ROTEIROS_SRC = 'roteiros.js';

  /* ── Loaders ────────────────────────────────────────────────── */
  function loadScript(src, cb) {
    const s = document.createElement('script');
    s.src = src;
    s.onload = cb;
    s.onerror = cb; // fail gracefully
    document.head.appendChild(s);
  }

  function loadGSAP(cb) {
    if (window.gsap) { cb(); return; }
    loadScript(GSAP_CDN, cb);
  }

  /* ── Progress bar ───────────────────────────────────────────── */
  function createProgressBar(cfg, roteiroNome) {
    const track = document.createElement('div');
    track.style.cssText = 'position:fixed;bottom:0;left:0;width:100%;height:3px;background:rgba(90,219,148,0.08);z-index:9999;box-shadow:0 -1px 0 rgba(90,219,148,0.08);';
    const fill = document.createElement('div');
    fill.style.cssText = 'height:100%;width:0%;background:linear-gradient(90deg,#5adb94,#0ba18c);border-radius:0 2px 2px 0;transition:width 0.4s ease;box-shadow:0 0 14px rgba(90,219,148,0.45);';
    track.appendChild(fill);
    document.body.appendChild(track);

    const info = document.createElement('div');
    info.style.cssText = 'position:fixed;bottom:7px;left:0;right:0;display:flex;justify-content:space-between;align-items:center;padding:0 16px;z-index:9999;pointer-events:none;';
    const st = 'font:10px/1 system-ui,sans-serif;letter-spacing:1px;color:rgba(195,178,228,0.34);';
    const rotLabel = roteiroNome
      ? `<span style="${st}color:rgba(90,219,148,0.45);">${roteiroNome.toUpperCase()}</span>`
      : '';
    info.innerHTML = `
      <span style="${st}">← → navegar &nbsp;·&nbsp; <strong style="color:rgba(90,219,148,0.6)">ESPAÇO</strong> próximo &nbsp;·&nbsp; R roteiro</span>
      <span id="_p_num" style="${st}color:rgba(255,255,255,0.35);letter-spacing:3px;">${cfg.page} / ${cfg.total}</span>
      <span style="display:flex;gap:10px;align-items:center;">${rotLabel}<span id="_p_steps" style="${st}font-variant-numeric:tabular-nums;"></span></span>
    `;
    document.body.appendChild(info);
    return { fill, stepsLabel: document.getElementById('_p_steps') };
  }

  /* ── Subtitle panel ─────────────────────────────────────────── */
  function createSubtitlePanel(steps, roteiroNome) {
    const panel = document.createElement('div');
    panel.id = '_sub_panel';
    panel.style.cssText = [
      'position:fixed', 'right:14px', 'bottom:30px',
      'width:300px', 'max-height:340px',
      'background:rgba(16,4,28,0.94)',
      'border:1px solid rgba(90,219,148,0.18)',
      'border-left:3px solid #5adb94',
      'border-radius:8px',
      'z-index:9990',
      'font-family:system-ui,sans-serif',
      'backdrop-filter:blur(18px) saturate(145%)',
      '-webkit-backdrop-filter:blur(18px) saturate(145%)',
      'box-shadow:0 18px 46px rgba(0,0,0,0.48), 0 0 28px rgba(90,219,148,0.08)',
      'display:flex', 'flex-direction:column',
      'overflow:hidden',
    ].join(';');

    const header = document.createElement('div');
    header.style.cssText = 'padding:9px 14px 8px;border-bottom:1px solid rgba(90,219,148,0.12);display:flex;justify-content:space-between;align-items:center;flex-shrink:0;background:rgba(14,3,26,0.5);';
    const rotTag = roteiroNome
      ? `<span style="font-size:8px;font-weight:700;color:rgba(90,219,148,0.6);letter-spacing:1px;">${roteiroNome.toUpperCase()}</span>`
      : '';
    header.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:9px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:#5adb94;">LEGENDA</span>
        ${rotTag}
      </div>
      <span id="_step_ctr" style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:1.5px;">0 / ${steps.length}</span>
    `;
    panel.appendChild(header);

    const body = document.createElement('div');
    body.style.cssText = 'padding:10px 14px 8px;overflow-y:auto;flex:1;scrollbar-width:thin;scrollbar-color:rgba(90,219,148,0.24) transparent;';

    steps.forEach((step, i) => {
      const line = document.createElement('div');
      line.id = '_sub_line_' + i;
      line.style.cssText = [
        'font-size:12.5px', 'line-height:1.6',
        'color:rgba(195,178,228,0.34)',
        'padding:5px 0',
        'transition:color 0.3s ease',
        i < steps.length - 1 ? 'border-bottom:1px solid rgba(90,219,148,0.08)' : '',
        i < steps.length - 1 ? 'margin-bottom:4px' : '',
      ].filter(Boolean).join(';');
      line.innerHTML = step.subtitle || '';
      body.appendChild(line);
    });

    panel.appendChild(body);

    const footer = document.createElement('div');
    footer.style.cssText = 'padding:6px 14px 9px;border-top:1px solid rgba(90,219,148,0.1);flex-shrink:0;background:rgba(14,3,26,0.35);';
    footer.innerHTML = `<span id="_sub_hint" style="font-size:9px;color:rgba(255,255,255,0.2);">[ESPAÇO] próximo &nbsp;·&nbsp; [→] próxima tela</span>`;
    panel.appendChild(footer);

    document.body.appendChild(panel);

    return {
      counter: document.getElementById('_step_ctr'),
      hint:    document.getElementById('_sub_hint'),
      getLine(i) { return document.getElementById('_sub_line_' + i); },
    };
  }

  /* ── Roteiro selector overlay ───────────────────────────────── */
  function showRoteiroSelector(onSelect) {
    const meta = (window.ROTEIROS && window.ROTEIROS.meta) || {
      1: { nome: 'Roteiro 1', desc: 'Versão padrão.' },
      2: { nome: 'Roteiro 2', desc: 'Versão alternativa.' },
      3: { nome: 'Roteiro 3', desc: 'Versão narrativa.' },
    };

    const overlay = document.createElement('div');
    overlay.style.cssText = [
      'position:fixed', 'inset:0', 'z-index:99999',
      'background:#0c0017',
      'background-image:radial-gradient(ellipse 60% 50% at 8% 0%, rgba(138,3,77,0.22) 0%, transparent 65%), radial-gradient(ellipse 45% 40% at 92% 100%, rgba(90,219,148,0.12) 0%, transparent 65%), radial-gradient(ellipse 50% 45% at 50% 50%, rgba(55,0,100,0.28) 0%, transparent 75%)',
      'display:flex', 'align-items:center', 'justify-content:center',
      'flex-direction:column', 'gap:34px',
      'font-family:system-ui,sans-serif',
      'opacity:0', 'transition:opacity 0.5s ease',
    ].join(';');

    const titleEl = document.createElement('div');
    titleEl.style.cssText = 'text-align:center;';
    titleEl.innerHTML = `
      <div style="font-size:10px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#5adb94;margin-bottom:16px;">
        Compatibilidade Conversacional com IA
      </div>
      <div style="font-size:34px;font-weight:800;color:rgba(255,255,255,0.92);margin-bottom:10px;">
        Selecione o Roteiro
      </div>
      <div style="font-size:14px;color:rgba(255,255,255,0.38);line-height:1.6;">
        Roteiro final para gravação do pitch.
      </div>
    `;
    overlay.appendChild(titleEl);

    const row = document.createElement('div');
    row.style.cssText = 'display:flex;gap:20px;';

    const COLORS = {
      1: { accent: '#5adb94', border: 'rgba(90,219,148,0.4)',  bg: 'rgba(90,219,148,0.05)'  },
      2: { accent: '#0ba18c', border: 'rgba(11,161,140,0.4)',  bg: 'rgba(11,161,140,0.05)'  },
      3: { accent: '#e8448a', border: 'rgba(232,68,138,0.35)', bg: 'rgba(138,3,77,0.07)'    },
    };

    Object.keys(meta).map(Number).forEach(n => {
      const m = meta[n];
      const c = COLORS[n];

      const card = document.createElement('div');
      card.style.cssText = [
        'width:220px', 'padding:24px 22px',
        `background:linear-gradient(145deg, ${c.bg}, rgba(18,4,32,0.88) 46%)`,
        `border:1px solid ${c.border}`,
        'border-radius:8px',
        'cursor:pointer',
        'transition:transform 0.2s ease, box-shadow 0.2s ease',
        'display:flex', 'flex-direction:column', 'gap:12px',
        'box-shadow:0 18px 46px rgba(0,0,0,0.36)',
        'backdrop-filter:blur(18px) saturate(145%)',
      ].join(';');

      card.innerHTML = `
        <div style="font-size:10px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:${c.accent};">
          ROTEIRO 0${n}
        </div>
        <div style="font-size:21px;font-weight:800;color:rgba(255,255,255,0.92);line-height:1.2;">
          ${m.nome}
        </div>
        <div style="font-size:12px;color:rgba(255,255,255,0.45);line-height:1.65;flex:1;">
          ${m.desc}
        </div>
        <div style="
          margin-top:4px;padding:8px 0;border-radius:8px;
          background:${c.bg};border:1px solid ${c.border};
          color:${c.accent};font-size:11px;font-weight:700;
          text-align:center;letter-spacing:1.5px;
        ">SELECIONAR →</div>
      `;

      card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
        card.style.boxShadow = `0 16px 48px ${c.border}`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.boxShadow = '';
      });
      card.addEventListener('click', () => {
        gsap.to(overlay, {
          autoAlpha: 0, duration: 0.35, ease: 'power2.in',
          onComplete() { overlay.remove(); onSelect(n); }
        });
      });

      row.appendChild(card);
    });

    overlay.appendChild(row);
    document.body.appendChild(overlay);
    requestAnimationFrame(() => { overlay.style.opacity = '1'; });
  }

  /* ── Apply roteiro subtitles to cfg.steps ───────────────────── */
  function applyRoteiro(num, cfg) {
    if (!window.ROTEIROS || !num) return;
    const pageData = window.ROTEIROS[num] && window.ROTEIROS[num][cfg.page];
    if (!pageData) return;
    cfg.steps.forEach((step, i) => {
      if (pageData[i] !== undefined) step.subtitle = pageData[i];
    });
  }

  /* ── Start presentation after roteiro is chosen ─────────────── */
  function startPresentation(cfg) {
    const roteiroNum  = parseInt(sessionStorage.getItem('pitchRoteiro')) || 1;
    const roteiroNome = window.ROTEIROS && window.ROTEIROS.meta && window.ROTEIROS.meta[roteiroNum]
      ? window.ROTEIROS.meta[roteiroNum].nome
      : null;

    const steps = Array.isArray(cfg.steps) ? cfg.steps : [];
    const { fill, stepsLabel } = createProgressBar(cfg, roteiroNome);
    const sub = createSubtitlePanel(steps, roteiroNome);

    if (typeof cfg.init === 'function') cfg.init(gsap);

    function navigate(url) {
      if (!url) return;
      gsap.to(document.body, {
        opacity: 0, duration: 0.9, ease: 'power2.inOut',
        onComplete() { window.location.href = url; }
      });
    }

    function updateProgress(stepIdx) {
      const pct = steps.length > 0 ? ((stepIdx + 1) / steps.length) * 100 : 0;
      fill.style.width = pct + '%';
      stepsLabel.textContent = (stepIdx + 1) + ' / ' + steps.length;
    }

    let currentStep = -1;
    let activeTargets = [];

    function setActiveTargets(targetSpec) {
      activeTargets.forEach(el => el.classList && el.classList.remove('pitch-step-active'));
      activeTargets = [];

      if (!targetSpec) return;

      let els = [];
      if (typeof targetSpec === 'string') {
        els = Array.from(document.querySelectorAll(targetSpec));
      } else if (Array.isArray(targetSpec)) {
        targetSpec.forEach(sel => {
          if (!sel) return;
          if (typeof sel === 'string') els.push(...document.querySelectorAll(sel));
          else if (sel && sel.nodeType === 1) els.push(sel);
        });
      } else if (targetSpec && targetSpec.nodeType === 1) {
        els = [targetSpec];
      }

      els = els.filter(Boolean);
      els.forEach(el => el.classList && el.classList.add('pitch-step-active'));
      activeTargets = els;
    }

    function runNextStep() {
      if (currentStep >= steps.length - 1) return;

      if (currentStep >= 0) {
        const prev = sub.getLine(currentStep);
        if (prev) {
          prev.style.color = 'rgba(255,255,255,0.22)';
          prev.classList && prev.classList.remove('pitch-sub-active');
        }
      }

      currentStep++;
      const step = steps[currentStep];

      if (typeof step.animate === 'function') step.animate(gsap);
      setActiveTargets(step.focus);

      const line = sub.getLine(currentStep);
      if (line) {
        line.style.color = 'rgba(255,255,255,0.88)';
        line.classList && line.classList.add('pitch-sub-active');
        line.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      sub.counter.textContent = (currentStep + 1) + ' / ' + steps.length;
      updateProgress(currentStep);

      if (currentStep === steps.length - 1) {
        sub.hint.innerHTML = '[ESPAÇO] ou [→] próxima tela';
        sub.hint.style.color = 'rgba(90,219,148,0.5)';
      }
    }

    /* Revela todos os steps restantes de uma vez */
    function revealAll() {
      while (currentStep < steps.length - 1) {
        if (currentStep >= 0) {
          const prev = sub.getLine(currentStep);
          if (prev) {
            prev.style.color = 'rgba(255,255,255,0.22)';
            prev.classList && prev.classList.remove('pitch-sub-active');
          }
        }
        currentStep++;
        const step = steps[currentStep];
        if (typeof step.animate === 'function') step.animate(gsap);
        setActiveTargets(step.focus);
        const line = sub.getLine(currentStep);
        if (line) {
          line.style.color = 'rgba(255,255,255,0.88)';
          line.classList && line.classList.add('pitch-sub-active');
        }
      }
      sub.counter.textContent = steps.length + ' / ' + steps.length;
      updateProgress(currentStep);
      const lastLine = sub.getLine(currentStep);
      if (lastLine) lastLine.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      sub.hint.innerHTML = '[ESPAÇO] ou [→] próxima tela';
      sub.hint.style.color = 'rgba(90,219,148,0.5)';
    }

    document.addEventListener('keydown', e => {
      const k = e.key;
      if (k === ' ') {
        e.preventDefault();
        if (currentStep < steps.length - 1) {
          runNextStep();
        } else {
          navigate(cfg.next);
        }
      }
      if (k === 'ArrowRight') {
        e.preventDefault();
        if (currentStep < steps.length - 1) {
          revealAll();
        } else {
          navigate(cfg.next);
        }
      }
      if (k === 'ArrowLeft') {
        navigate(cfg.prev || cfg.next);
      }
      if (k === 'r' || k === 'R') {
        sessionStorage.removeItem('pitchRoteiro');
        navigate('pagina-1.html');
      }
    });
  }

  /* ── Main init ─────────────────────────────────────────────── */
  function init() {
    const cfg = window.PITCH;
    if (!cfg) return;

    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.9s ease';
    requestAnimationFrame(() => { document.body.style.opacity = '1'; });

    const saved = sessionStorage.getItem('pitchRoteiro');

    if (cfg.page === 1 && !saved) {
      showRoteiroSelector(function (num) {
        sessionStorage.setItem('pitchRoteiro', num);
        applyRoteiro(num, cfg);
        startPresentation(cfg);
      });
    } else {
      applyRoteiro(parseInt(saved) || 1, cfg);
      startPresentation(cfg);
    }
  }

  /* ── Bootstrap ─────────────────────────────────────────────── */
  loadScript(ROTEIROS_SRC, function () {
    loadGSAP(function () {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
      } else {
        init();
      }
    });
  });

})();
