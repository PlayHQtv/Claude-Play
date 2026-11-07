// PlayHQ "Anatomy" weapon breakdown – Remotion + GSAP.
// All motion lives in one paused GSAP master timeline that is seeked to frame/fps on every frame
// (deterministic, works with Remotion's parallel rendering). Particles/grain are drawn per frame.
import React, {useLayoutEffect, useRef, useState} from 'react';
import {AbsoluteFill, Audio, Sequence, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import gsap from 'gsap';
import {SplitText} from 'gsap/SplitText';
import {DrawSVGPlugin} from 'gsap/DrawSVGPlugin';
gsap.registerPlugin(SplitText, DrawSVGPlugin);

type Part = {ty: string; nm: string; px: number; py: number; tag: [number, number]};
type Sfx = {file: string; at: number; vol?: number};
export type Job = {
  duration: number; img: {w: number; h: number};
  kicker: string; title: string; title2: string; badge: string; source: string; header?: string;
  parts: Part[]; sfx: Sfx[]; bed?: string;
};
export const defaultJob: Job = {
  duration: 24, img: {w: 1808, h: 703}, kicker: 'MW4 MULTIPLAYER · BUILD BREAKDOWN', title: 'KASTOV 762', title2: 'ANATOMY',
  badge: 'BUILD 01 · STANDARD', source: 'BUILD: GAME8 · NOV 2026', parts: [], sfx: [],
};

const FONTS = [
  ['Anton', 'fonts/Anton-Regular.ttf'], ['RajB', 'fonts/Rajdhani-Bold.ttf'], ['Raj', 'fonts/Rajdhani-SemiBold.ttf'],
];
let fontsP: Promise<void> | null = null;
const loadFonts = () => {
  if (!fontsP) fontsP = Promise.all(FONTS.map(([n, f]) => new FontFace(n, `url(${staticFile(f)})`).load()))
    .then((fs) => { fs.forEach((f) => (document.fonts as any).add(f)); });
  return fontsP;
};

// layout constants
const RW = 1000, X0 = 40, CX = 540, CY = 900, ZC: [number, number] = [540, 860], ZS = 2.25, PS = 5.6, PD = 2.4;
const GOLD = '#FFD400';
const mono: React.CSSProperties = {fontFamily: 'DejaVu Sans Mono, monospace', fontSize: 19, letterSpacing: 2, color: 'rgba(255,212,0,.78)', whiteSpace: 'pre'};

function rng(s: number) { return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
const R1 = rng(7); const DUST = Array.from({length: 180}, () => ({x: R1() * 1080, y: R1() * 1920, z: R1(), s: R1() * 6.283, v: R1()}));
const R2 = rng(11); const BURST = Array.from({length: 240}, () => ({a: R2() * 6.283, sp: 200 + R2() * 950, sz: 1 + R2() * 3.6, l: 0.6 + R2() * 0.9}));
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));

export const Anatomy: React.FC<Job> = (job) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const RH = RW * job.img.h / job.img.w, Y0 = CY - RH / 2, K = RW / job.img.w;
  const W = (px: number, py: number): [number, number] => [X0 + K * px, Y0 + K * py];
  const parts = job.parts.map((p) => ({...p, w: W(p.px, p.py)}));
  const root = useRef<HTMLDivElement>(null);
  const tl = useRef<gsap.core.Timeline | null>(null);
  const camState = useRef({x: 0, y: 0, s: 1});
  const [handle] = useState(() => delayRender('gsap-timeline'));
  const frameRef = useRef(frame); frameRef.current = frame;
  const [dbg, setDbg] = useState('init');

  // ---------- build the master timeline once ----------
  useLayoutEffect(() => {
    let ctx: gsap.Context;
    setDbg('effect');
    loadFonts().then(() => {
      setDbg('fonts');
      try {
      ctx = gsap.context(() => {
        const q = gsap.utils.selector(root);
        const m = gsap.timeline({paused: true, defaults: {ease: 'power3.out'}});
        const at = (s: number) => s;
        gsap.set(q('#cam'), {transformOrigin: '0 0', x: 0, y: 0, scale: 1});
        gsap.set(q('#lock, #lockb'), {svgOrigin: `${CX} ${CY}`});
        gsap.set(q('#ret, #retr, #retp'), {svgOrigin: `${ZC[0]} ${ZC[1]}`});
        gsap.set(q('.card'), {transformPerspective: 900});

        // HOOK 0–2.2: laser scan draws a gold wireframe, flash, real rifle, kinetic title
        m.fromTo(q('#scan'), {x: X0 - 3}, {x: X0 + RW - 3, duration: 0.9, ease: 'power2.inOut'}, 0.15)
          .fromTo(q('#scan'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.08}, 0.12)
          .to(q('#scan'), {autoAlpha: 0, duration: 0.15}, 1.02)
          .fromTo(q('#edge'), {clipPath: 'inset(0% 100% 0% 0%)', autoAlpha: 1}, {clipPath: 'inset(0% 0% 0% 0%)', duration: 0.9, ease: 'power2.inOut'}, 0.15)
          .fromTo(q('#gridbg'), {autoAlpha: 0}, {autoAlpha: 0.5, duration: 0.5, yoyo: true, repeat: 1}, 0.2)
          .fromTo(q('#flash'), {autoAlpha: 0}, {autoAlpha: 0.9, duration: 0.05, ease: 'none'}, 1.0)
          .to(q('#flash'), {autoAlpha: 0, duration: 0.5, ease: 'power2.out'}, 1.05)
          .fromTo(q('#real, #slabs'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.12, ease: 'none'}, 1.0)
          .to(q('#edge'), {autoAlpha: 0.16, duration: 0.6}, 1.1)
          .fromTo(q('.beam'), {autoAlpha: 0}, {autoAlpha: 0.75, duration: 1.0, stagger: 0.12}, 0.95)
          .fromTo(q('.haze, #dustB'), {autoAlpha: 0}, {autoAlpha: 1, duration: 1.2}, 0.8)
          .fromTo(q('#floor, #floorglow, #refl'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.5}, 1.0)
          .fromTo(q('#rig'), {rotationY: -20, rotationX: 7, z: -260}, {rotationY: -8, rotationX: 6, z: 0, duration: 2.0, ease: 'expo.out'}, 0.6);
        const t1 = new SplitText(q('#t1'), {type: 'chars'});
        m.from(t1.chars, {yPercent: 120, scale: 1.7, autoAlpha: 0, filter: 'blur(16px)', duration: 0.42, stagger: 0.045, ease: 'back.out(2)'}, 1.08)
          .fromTo(q('#t1'), {textShadow: '10px 0 rgba(255,0,60,.8),-10px 0 rgba(0,220,255,.8)'}, {textShadow: '0px 0 rgba(255,0,60,0),0px 0 rgba(0,220,255,0)', duration: 0.5}, 1.1)
          .fromTo(q('#t2'), {clipPath: 'inset(0% 100% 0% 0%)', x: -30}, {clipPath: 'inset(0% 0% 0% 0%)', x: 0, duration: 0.5, ease: 'expo.out'}, 1.5)
          .to(q('#t2'), {keyframes: [{x: 8, duration: 0.03}, {x: -10, duration: 0.03}, {x: 5, duration: 0.03}, {x: 0, duration: 0.03}], ease: 'none'}, 1.98)
          .fromTo(q('#kicker'), {autoAlpha: 0, letterSpacing: 30}, {autoAlpha: 1, letterSpacing: 12, duration: 0.6, ease: 'expo.out'}, 1.7);

        // HERO 2.2–4.4: orbit, light sweep, lock-on ring, profile ruler
        m.to(q('#rig'), {keyframes: [{rotationY: -26, rotationX: 9, duration: 1.1, ease: 'sine.inOut'}, {rotationY: 8, rotationX: 4, duration: 1.3, ease: 'sine.inOut'}]}, 2.2)
          .fromTo(q('#sweep'), {backgroundPosition: '100% 0'}, {backgroundPosition: '0% 0', duration: 1.2, ease: 'power2.inOut'}, 2.7)
          .fromTo(q('#sweep'), {autoAlpha: 0}, {autoAlpha: 0.9, duration: 0.2, yoyo: true, repeat: 1, repeatDelay: 0.8}, 2.7)
          .fromTo(q('#lock'), {autoAlpha: 0, scale: 1.8, rotation: -40}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.7, ease: 'expo.out'}, 2.3)
          .fromTo(q('#lockb'), {autoAlpha: 0, scale: 1.3}, {autoAlpha: 1, scale: 1, duration: 0.15, ease: 'power4.out'}, 2.95)
          .to(q('#lock'), {rotation: 60, duration: 1.4, ease: 'none'}, 3.0)
          .to(q('#lock'), {autoAlpha: 0, scale: 0.8, duration: 0.3}, 4.15)
          .fromTo(q('#ruler'), {drawSVG: '0%'}, {drawSVG: '100%', duration: 0.8, ease: 'power3.inOut'}, 2.4)
          .fromTo(q('.tick'), {scaleY: 0, transformOrigin: '50% 0%'}, {scaleY: 1, duration: 0.2, stagger: 0.012}, 2.45)
          .fromTo(q('#rulerg'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, 2.4)
          .to(q('#rulerg'), {autoAlpha: 0, duration: 0.3}, 4.3)
          .fromTo(q('#hud'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, 1.8)
          .to(q('#t1, #t2, #kicker'), {autoAlpha: 0, y: -60, duration: 0.45, ease: 'power3.in', stagger: 0.05}, 4.25);

        // X-RAY 4.4–5.4: scanner right→left turns the rifle into a blueprint
        m.fromTo(q('#xscan'), {x: X0 + RW, autoAlpha: 0}, {x: X0 - 4, autoAlpha: 1, duration: 0.95, ease: 'power2.inOut'}, 4.45)
          .to(q('#xscan'), {autoAlpha: 0, duration: 0.12}, 5.38)
          .fromTo(q('#xray'), {clipPath: 'inset(0% 0% 0% 100%)', autoAlpha: 0.85}, {clipPath: 'inset(0% 0% 0% 0%)', duration: 0.95, ease: 'power2.inOut'}, 4.45)
          .to(q('#real'), {autoAlpha: 0.38, duration: 0.9}, 4.5)
          .to(q('#edge'), {autoAlpha: 0.55, duration: 0.9}, 4.5)
          .to(q('#gridbg'), {autoAlpha: 0.9, duration: 0.8}, 4.5)
          .to(q('#rig'), {rotationY: 0, rotationX: 0, duration: 0.8, ease: 'power3.inOut'}, 4.6)
          .to(q('#floor, #floorglow, #refl'), {autoAlpha: 0, duration: 0.6}, 4.6)
          .to(q('.beam'), {autoAlpha: 0.35, duration: 0.8}, 4.6)
          .to(q('#hud'), {autoAlpha: 0, duration: 0.3}, 5.1)
          .fromTo(q('#hdr'), {autoAlpha: 0, x: -80}, {autoAlpha: 1, x: 0, duration: 0.5, ease: 'expo.out'}, 5.2);

        // BREAKDOWN: per part a camera push, reticle lock, drawn callout, glass card with typed name
        const camTo = (wx: number, wy: number, s: number, c: [number, number]) => ({x: c[0] - wx * s, y: c[1] - wy * s, scale: s});
        let prev = [CX, CY, 1];
        parts.forEach((p, i) => {
          const s0 = PS + i * PD, mv = i === 0 ? 5.15 : s0 - 0.45, dur = i === 0 ? 0.6 : 0.6;
          m.to(q('#cam'), {...camTo(p.w[0], p.w[1], ZS, ZC), duration: dur, ease: 'expo.inOut'}, mv)
            .to(q('#cam'), {keyframes: [{filter: 'blur(9px)', duration: dur * 0.5, ease: 'power2.in'}, {filter: 'blur(0px)', duration: dur * 0.5, ease: 'power2.out'}]}, mv)
            .fromTo(q('#ret'), {autoAlpha: 0, scale: 3}, {autoAlpha: 1, scale: 1, duration: 0.38, ease: 'expo.out'}, s0 + 0.12)
            .fromTo(q('#retp'), {autoAlpha: 0.9, scale: 1}, {autoAlpha: 0, scale: 2.8, duration: 0.5, ease: 'power2.out'}, s0 + 0.45)
            .fromTo(q('#retr'), {rotation: 0}, {rotation: 180, duration: 2.2, ease: 'none'}, s0 + 0.12)
            .fromTo(q('#call'), {drawSVG: '0%', autoAlpha: 1}, {drawSVG: '100%', duration: 0.45, ease: 'power3.out'}, s0 + 0.3)
            .fromTo(q(`#card${i}`), {autoAlpha: 0, y: 70, rotationX: -25, scale: 1.12, filter: 'blur(12px)'}, {autoAlpha: 1, y: 0, rotationX: 0, scale: 1, filter: 'blur(0px)', duration: 0.5, ease: 'expo.out'}, s0 + 0.5)
            .fromTo(q(`#card${i} .bar`), {scaleX: 0}, {scaleX: 1, duration: 1.4, ease: 'none', transformOrigin: '0% 50%'}, s0 + 0.7)
            .fromTo(q(`#card${i} .ix`), {autoAlpha: 0, x: -30}, {autoAlpha: 0.95, x: 0, duration: 0.4, ease: 'expo.out'}, s0 + 0.55)
            .fromTo(q('#sweep'), {backgroundPosition: '100% 0', autoAlpha: 0.85}, {backgroundPosition: '0% 0', duration: 0.8, ease: 'power2.inOut'}, s0 + 0.15)
            .to(q('#sweep'), {autoAlpha: 0, duration: 0.1}, s0 + 0.95);
          const nm = new SplitText(q(`#card${i} .nm`), {type: 'chars'});
          m.from(nm.chars, {autoAlpha: 0, duration: 0.01, stagger: 0.028, ease: 'none'}, s0 + 0.62)
            .to(q(`#card${i}`), {autoAlpha: 0, y: -24, filter: 'blur(10px)', duration: 0.3, ease: 'power2.in'}, s0 + 2.0)
            .to(q('#ret, #call'), {autoAlpha: 0, duration: 0.25}, s0 + 2.0);
          prev = [p.w[0], p.w[1], ZS];
        });

        // ASSEMBLY 17.5–21: back to full view, reverse scan to the real rifle, all callouts at once
        const tA = PS + parts.length * PD - 0.05;
        m.to(q('#cam'), {x: 0, y: 0, scale: 1, duration: 0.7, ease: 'expo.inOut'}, tA)
          .to(q('#cam'), {keyframes: [{filter: 'blur(8px)', duration: 0.35}, {filter: 'blur(0px)', duration: 0.35}]}, tA)
          .to(q('#hdr'), {autoAlpha: 0, duration: 0.3}, tA)
          .fromTo(q('#xscan'), {x: X0 - 4, autoAlpha: 1}, {x: X0 + RW, duration: 0.7, ease: 'power2.inOut'}, tA)
          .to(q('#xscan'), {autoAlpha: 0, duration: 0.1}, tA + 0.7)
          .to(q('#xray'), {clipPath: 'inset(0% 0% 0% 100%)', duration: 0.7, ease: 'power2.inOut'}, tA)
          .to(q('#real'), {autoAlpha: 1, duration: 0.6}, tA + 0.1)
          .to(q('#edge'), {autoAlpha: 0.12, duration: 0.6}, tA + 0.1)
          .to(q('#gridbg'), {autoAlpha: 0.15, duration: 0.6}, tA + 0.1)
          .to(q('#floor, #floorglow, #refl'), {autoAlpha: 1, duration: 0.6}, tA + 0.3)
          .to(q('.beam'), {autoAlpha: 0.75, duration: 0.8}, tA + 0.2)
          .fromTo(q('#badge'), {autoAlpha: 0, scale: 1.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: 'expo.out'}, tA + 0.75)
          .to(q('#rig'), {keyframes: [{rotationY: -7, rotationX: 4, duration: 1.0, ease: 'sine.inOut'}, {rotationY: 6, rotationX: 2, duration: 1.8, ease: 'sine.inOut'}]}, tA + 0.7)
          .fromTo(q('#sweep'), {backgroundPosition: '100% 0', autoAlpha: 0.85}, {backgroundPosition: '0% 0', duration: 1.2, ease: 'power2.inOut'}, tA + 1.7)
          .to(q('#sweep'), {autoAlpha: 0, duration: 0.1}, tA + 2.9)
          .fromTo(q('.tagline'), {drawSVG: '0%'}, {drawSVG: '100%', duration: 0.5, stagger: 0.12, ease: 'power2.out'}, tA + 0.9)
          .fromTo(q('.tagdot'), {scale: 0, transformOrigin: '50% 50%'}, {scale: 1, duration: 0.4, stagger: 0.12, ease: 'back.out(3)'}, tA + 0.85)
          .fromTo(q('.tag'), {autoAlpha: 0, y: 20}, {autoAlpha: 1, y: 0, duration: 0.45, stagger: 0.12, ease: 'expo.out'}, tA + 1.0)
          .fromTo(q('#hud'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, tA + 0.9);

        // OUTRO 21–24: rifle flies off, burst, SAVE THIS BUILD, logo
        const tO = tA + 3.5;
        m.to(q('.tag, #tags svg, #badge, #hud'), {autoAlpha: 0, duration: 0.25}, tO - 0.3)
          .to(q('#rig'), {x: 1500, rotationY: 45, filter: 'blur(14px)', duration: 0.8, ease: 'power3.in'}, tO)
          .to(q('#refl, #floor, #floorglow'), {autoAlpha: 0, duration: 0.5}, tO)
          .fromTo(q('#flash'), {autoAlpha: 0}, {autoAlpha: 0.7, duration: 0.05}, tO - 0.05)
          .to(q('#flash'), {autoAlpha: 0, duration: 0.5}, tO);
        const s1 = new SplitText(q('#save1'), {type: 'chars'});
        m.from(s1.chars, {scale: 2.4, autoAlpha: 0, filter: 'blur(16px)', duration: 0.4, stagger: 0.03, ease: 'expo.out'}, tO + 0.2)
          .fromTo(q('#save2'), {scale: 2.6, autoAlpha: 0, filter: 'blur(18px)'}, {scale: 1, autoAlpha: 1, filter: 'blur(0px)', duration: 0.45, ease: 'expo.out'}, tO + 0.45)
          .fromTo(q('#logo'), {autoAlpha: 0, rotation: -260, scale: 0.3}, {autoAlpha: 1, rotation: 0, scale: 1, duration: 0.8, ease: 'back.out(1.6)'}, tO + 0.9)
          .fromTo(q('#lring'), {autoAlpha: 0, scale: 1.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: 'expo.out'}, tO + 0.9)
          .fromTo(q('#lring'), {rotation: 0}, {rotation: 90, duration: 3, ease: 'none'}, tO + 0.9)
          .fromTo(q('#follow'), {autoAlpha: 0, letterSpacing: 30}, {autoAlpha: 1, letterSpacing: 10, duration: 0.6, ease: 'expo.out'}, tO + 1.4)
          .fromTo(q('#src'), {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, tO + 1.7);

        // ambient loops (seek-safe): beams sway, haze drift, rifle float during hook/hero/assembly
        m.to(q('#b1'), {rotation: -11, duration: 4, yoyo: true, repeat: 7, ease: 'sine.inOut'}, 0)
          .to(q('#b3'), {rotation: 19, duration: 3.3, yoyo: true, repeat: 7, ease: 'sine.inOut'}, 0)
          .to(q('#hz1'), {x: 120, y: 60, duration: 12, yoyo: true, repeat: 1, ease: 'sine.inOut'}, 0)
          .to(q('#hz2'), {x: -140, y: -40, duration: 10, yoyo: true, repeat: 2, ease: 'sine.inOut'}, 0)
          .fromTo(q('#float'), {y: -6}, {y: 6, duration: 1.3, yoyo: true, repeat: 3, ease: 'sine.inOut'}, 0)
          .to(q('#float'), {y: 0, duration: 0.4}, 5.2)
          .fromTo(q('#float'), {y: 0}, {y: 5, duration: 1.2, yoyo: true, repeat: 1, ease: 'sine.inOut'}, tA + 0.8);
        m.to({}, {duration: 0.01}, job.duration);
        tl.current = m;
        m.seek(frameRef.current / fps, false);
        const el = document.querySelector('#save1') as HTMLElement; const sc = document.querySelector('#scan') as HTMLElement;
        setDbg('built ' + m.duration().toFixed(2) + ' q=' + q('#save1').length + '/' + q('#scan').length + ' rootcur=' + (root.current ? root.current.tagName : 'null') + ' docN=' + document.querySelectorAll('#save1').length + ' saveOp=' + (el && el.style.opacity) + ' scanTf=' + (sc && sc.style.transform) + ' kids=' + m.getChildren(false).length);
      }, root);
      } catch (e: any) { console.error('TIMELINE ERROR', e); setDbg('ERR ' + (e && (e.stack || e.message) || String(e)).slice(0, 300)); }
      continueRender(handle);
    }).catch((e: any) => { console.error('FONT ERROR', e); setDbg('FONTERR ' + String(e)); continueRender(handle); });
    return () => ctx && ctx.revert();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ---------- per frame: seek + canvases ----------
  const dustB = useRef<HTMLCanvasElement>(null), dustF = useRef<HTMLCanvasElement>(null);
  useLayoutEffect(() => {
    if (tl.current) tl.current.seek(t, false);
    const cam = root.current?.querySelector('#cam') as HTMLElement | null;
    let cs = 1, cx = 0, cy = 0;
    if (cam) { cs = Number(gsap.getProperty(cam, 'scale')) || 1; cx = Number(gsap.getProperty(cam, 'x')) || 0; cy = Number(gsap.getProperty(cam, 'y')) || 0; }
    camState.current = {x: cx, y: cy, s: cs};
    const draw = (cv: HTMLCanvasElement | null, front: boolean) => {
      if (!cv) return; const g = cv.getContext('2d')!; g.clearRect(0, 0, 1080, 1920);
      for (const d of DUST) {
        if ((d.z > 0.72) !== front) continue; const par = front ? 0.35 : 0.12;
        let x = d.x + Math.sin(t * 0.4 + d.s) * 30 + t * 16 * (d.v - 0.5) + cx * par;
        let y = d.y - t * (14 + 30 * d.z) + cy * par * 0.3;
        x = ((x % 1080) + 1080) % 1080; y = ((y % 1920) + 1920) % 1920;
        const r = (front ? (2 + d.z * 5) * (1 + 0.3 * (cs - 1)) : 0.6 + d.z * 2.2) * (front ? 2.2 : 1.8);
        const a = front ? 0.1 + 0.12 * Math.sin(t * 2 + d.s) ** 2 : 0.25 + 0.5 * Math.sin(t * 1.3 + d.s) ** 2;
        const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(255,226,150,${a})`); gr.addColorStop(1, 'rgba(255,200,80,0)');
        g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 6.283); g.fill();
      }
      const tO = PS + parts.length * PD - 0.05 + 3.5, bt = t - tO;
      if (front && bt > 0 && bt < 2.4) for (const p of BURST) {
        const k = 1 - Math.pow(1 - clamp(bt / 1.6), 4); const x = 540 + Math.cos(p.a) * p.sp * k, y = 880 + Math.sin(p.a) * p.sp * k * 0.8 + bt * bt * 40;
        g.fillStyle = `rgba(255,${200 + Math.floor(p.sz * 10)},90,${clamp(1 - bt / p.l / 1.8)})`; g.beginPath(); g.arc(x, y, p.sz, 0, 6.283); g.fill();
      }
    };
    draw(dustB.current, false); draw(dustF.current, true);
  }, [frame]);

  const pi = clamp(Math.floor((t - PS) / PD), 0, Math.max(0, parts.length - 1));
  const ry = root.current ? Number(gsap.getProperty(root.current.querySelector('#rig') as any, 'rotationY')) || 0 : 0;
  const ticks = Array.from({length: 51}, (_, i) => i);
  const tA = PS + parts.length * PD - 0.05;
  const hudL = t < 4.4 ? 'TARGET ACQUIRED ▸ ' + job.title.replace(/\s/g, '-') : t < 5.5 ? `X-RAY SCAN ▸ ${Math.round(clamp((t - 4.45) / 0.95) * 100)}%` : `ASSEMBLY ▸ ${parts.length}/${parts.length} PARTS`;

  return (
    <AbsoluteFill ref={root as any} style={{background: 'radial-gradient(120% 70% at 50% 46%,#16120a 0%,#070604 45%,#000 80%)', overflow: 'hidden'}}>
      <style>{`
        .abs{position:absolute}
        .beam{top:-300px;width:300px;height:2400px;background:linear-gradient(to bottom,rgba(255,206,90,.55),rgba(255,190,60,.12) 45%,transparent 75%);filter:blur(40px);mix-blend-mode:screen;transform-origin:50% 0}
        .haze{width:1600px;height:900px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,200,120,.10),transparent);filter:blur(30px)}
        .slab{position:absolute;left:0;top:0;width:${RW}px;height:${RH}px;filter:brightness(.18) contrast(1.2)}
        .lay{position:absolute;left:0;top:0;width:${RW}px;height:${RH}px}
        .card{left:70px;top:1236px;width:820px;height:230px;border:1px solid rgba(255,212,0,.55);background:linear-gradient(135deg,rgba(40,34,18,.74),rgba(8,8,8,.74));backdrop-filter:blur(14px);clip-path:polygon(0 0,calc(100% - 34px) 0,100% 34px,100% 100%,34px 100%,0 calc(100% - 34px));transform-origin:20% 50%}
        .card .ix{position:absolute;left:26px;top:14px;font-family:Anton;font-size:178px;line-height:1;color:transparent;-webkit-text-stroke:2px ${GOLD}}
        .card .ty{position:absolute;left:250px;top:40px;font-family:RajB;font-size:30px;letter-spacing:9px;color:#a9a191}
        .card .nm{position:absolute;left:250px;top:80px;font-family:Anton;line-height:1.05;color:#fff;white-space:nowrap}
        .card .barbg{position:absolute;left:250px;top:182px;width:520px;height:4px;background:rgba(255,255,255,.12)}
        .card .bar{position:absolute;left:0;top:0;width:520px;height:4px;background:${GOLD};box-shadow:0 0 12px ${GOLD}}
        .card .tk{position:absolute;right:16px;top:12px;width:46px;height:4px;background:${GOLD}}
        .tag{width:290px}
        .tag .ty{font-family:RajB;font-size:22px;letter-spacing:6px;color:#a9a191}
        .tag .nm{font-family:Anton;font-size:33px;color:#fff;line-height:1.1;white-space:nowrap}
        .tag .ix{font-family:Anton;font-size:22px;color:${GOLD};margin-right:8px}
      `}</style>
      <div id="gridbg" className="abs" style={{inset: 0, opacity: 0, backgroundImage: 'linear-gradient(rgba(120,200,255,.10) 1px,transparent 1px),linear-gradient(90deg,rgba(120,200,255,.10) 1px,transparent 1px),linear-gradient(rgba(120,200,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(120,200,255,.05) 1px,transparent 1px)', backgroundSize: '120px 120px,120px 120px,24px 24px,24px 24px'}} />
      <div id="hz1" className="abs haze" style={{left: -300, top: 600}} /><div id="hz2" className="abs haze" style={{left: -100, top: 1000}} />
      <div id="b1" className="abs beam" style={{left: 150, transform: 'rotate(-15deg)'}} /><div id="b2" className="abs beam" style={{left: 470, transform: 'rotate(4deg)'}} /><div id="b3" className="abs beam" style={{left: 760, transform: 'rotate(15deg)'}} />
      <canvas id="dustB" ref={dustB} width={1080} height={1920} className="abs" style={{left: 0, top: 0}} />
      <div id="cam" className="abs" style={{left: 0, top: 0, width: 1080, height: 1920}}>
        <div id="floorglow" className="abs" style={{left: 90, top: Y0 + RH - 35, width: 900, height: 110, borderRadius: '50%', background: 'radial-gradient(closest-side,rgba(255,200,60,.35),transparent)', filter: 'blur(10px)'}} />
        <img id="refl" className="abs" src={staticFile('rifle.png')} style={{left: X0, top: Y0 + RH + 10, width: RW, height: RH, transform: 'scaleY(-1)', opacity: 0.16, WebkitMaskImage: 'linear-gradient(to top,rgba(0,0,0,.9),transparent 55%)', filter: 'blur(2px)'}} />
        <div id="floor" className="abs" style={{left: -100, top: Y0 + RH + 6, width: 1280, height: 3, background: `linear-gradient(90deg,transparent,${GOLD} 30%,#fff3b0 50%,${GOLD} 70%,transparent)`, boxShadow: '0 0 30px 6px rgba(255,212,0,.35)'}} />
        <div className="abs" style={{left: 0, top: 0, width: 1080, height: 1920, perspective: 1700, perspectiveOrigin: `${CX}px ${CY}px`}}>
          <div id="float" className="abs" style={{left: 0, top: 0, width: 1080, height: 1920, transformStyle: 'preserve-3d'}}>
            <div id="rig" className="abs" style={{left: X0, top: Y0, width: RW, height: RH, transformStyle: 'preserve-3d', transformOrigin: `${RW / 2}px ${RH / 2}px`}}>
              <div id="slabs">{Array.from({length: 14}, (_, i) => <img key={i} className="slab" src={staticFile('rifle.png')} style={{transform: `translateZ(${-(i + 1) * 1.6}px)`}} />)}</div>
              <img id="real" className="lay" src={staticFile('rifle.png')} style={{opacity: 0}} />
              <img id="xray" className="lay" src={staticFile('xray.png')} style={{opacity: 0, mixBlendMode: 'screen'}} />
              <img id="edge" className="lay" src={staticFile('edge.png')} style={{opacity: 0}} />
              <div id="sweep" className="lay" style={{opacity: 0, background: 'linear-gradient(100deg,transparent 42%,rgba(255,236,190,0) 44%,rgba(255,236,190,.95) 50%,rgba(255,236,190,0) 56%,transparent 58%)', backgroundSize: '300% 100%', WebkitMaskImage: `url(${staticFile('rifle.png')})`, WebkitMaskSize: '100% 100%', mixBlendMode: 'screen'}} />
            </div>
          </div>
        </div>
      </div>
      <div id="xscan" className="abs" style={{left: 0, top: 560, width: 4, height: 700, opacity: 0, background: '#bff4ff', boxShadow: '0 0 24px 8px rgba(120,220,255,.8),0 0 90px 30px rgba(80,180,255,.35)'}} />
      <div id="scan" className="abs" style={{left: 0, top: 0, width: 6, height: 1920, opacity: 0, background: '#fff6c8', boxShadow: '0 0 30px 10px rgba(255,212,0,.8),0 0 120px 40px rgba(255,180,0,.35)'}} />
      {/* screen-space overlays */}
      <svg className="abs" width={1080} height={1920} style={{left: 0, top: 0, overflow: 'visible'}}>
        <g id="lock" style={{opacity: 0, transformOrigin: `${CX}px ${CY}px`}}>
          <circle id="lockc" cx={CX} cy={CY} r={240} fill="none" stroke={GOLD} strokeWidth={2} strokeDasharray="40 18 6 18" />
          <circle cx={CX} cy={CY} r={258} fill="none" stroke="rgba(255,212,0,.35)" strokeWidth={1} strokeDasharray="2 10" />
          <path id="lockb" d={`M${CX - 270} ${CY - 60} v-40 h40 M${CX + 270} ${CY - 60} v-40 h-40 M${CX - 270} ${CY + 60} v40 h40 M${CX + 270} ${CY + 60} v40 h-40`} stroke={GOLD} strokeWidth={3} fill="none" style={{transformOrigin: `${CX}px ${CY}px`}} />
        </g>
        <g id="rulerg" style={{opacity: 0}}>
          <path id="ruler" d={`M${X0} 1190 H${X0 + RW}`} stroke="rgba(255,212,0,.7)" strokeWidth={1.5} />
          {ticks.map((i) => <path key={i} className="tick" d={`M${X0 + i * 20} 1190 v${i % 10 === 0 ? 26 : i % 5 === 0 ? 16 : 8}`} stroke="rgba(255,212,0,.6)" strokeWidth={1.5} />)}
          <text x={X0} y={1260} fill="rgba(255,212,0,.75)" fontFamily="DejaVu Sans Mono" fontSize={19} letterSpacing={2}>PROFILE SCAN ▸ {Math.round(clamp((t - 2.4) / 0.8) * 100)}%</text>
        </g>
        <g id="ret" style={{opacity: 0, transformOrigin: `${ZC[0]}px ${ZC[1]}px`}}>
          <circle cx={ZC[0]} cy={ZC[1]} r={52 * (1 + 0.1 * Math.sin(t * 10))} fill="none" stroke={GOLD} strokeWidth={2.5} />
          <g id="retr" style={{transformOrigin: `${ZC[0]}px ${ZC[1]}px`}}><circle cx={ZC[0]} cy={ZC[1]} r={88} fill="none" stroke="rgba(255,212,0,.45)" strokeWidth={1} strokeDasharray="4 8" /></g>
          <circle cx={ZC[0]} cy={ZC[1]} r={7} fill={GOLD} />
          <path d={`M${ZC[0] - 82} ${ZC[1]} h22 M${ZC[0] + 60} ${ZC[1]} h22 M${ZC[0]} ${ZC[1] - 82} v22 M${ZC[0]} ${ZC[1] + 60} v22`} stroke={GOLD} strokeWidth={3} />
          <circle id="retp" cx={ZC[0]} cy={ZC[1]} r={52} fill="none" stroke="rgba(255,240,200,.9)" strokeWidth={2} style={{transformOrigin: `${ZC[0]}px ${ZC[1]}px`}} />
        </g>
        <path id="call" d={`M${ZC[0]} ${ZC[1] + 60} L${ZC[0] - 140} ${ZC[1] + 230} L170 ${ZC[1] + 230} L170 1236`} fill="none" stroke={GOLD} strokeWidth={2.5} style={{opacity: 0, filter: `drop-shadow(0 0 6px ${GOLD})`}} />
      </svg>
      <canvas id="dustF" ref={dustF} width={1080} height={1920} className="abs" style={{left: 0, top: 0}} />
      {/* titles */}
      <div id="kicker" className="abs" style={{left: 0, width: 1080, top: 262, textAlign: 'center', fontFamily: 'RajB', fontSize: 34, letterSpacing: 12, color: '#d9d2bf', opacity: 0}}>{job.kicker}</div>
      <div id="t1" className="abs" style={{left: 0, width: 1080, top: 300, textAlign: 'center', fontFamily: 'Anton', fontSize: 178, lineHeight: 1, color: '#fff', whiteSpace: 'nowrap'}}>{job.title}</div>
      <div id="t2" className="abs" style={{left: 0, width: 1080, top: 480, textAlign: 'center', fontFamily: 'Anton', fontSize: 178, lineHeight: 1, color: GOLD, letterSpacing: 6, whiteSpace: 'nowrap', clipPath: 'inset(0% 100% 0% 0%)', textShadow: '0 0 40px rgba(255,212,0,.35)'}}>{job.title2}</div>
      <div id="hdr" className="abs" style={{left: 70, top: 200, opacity: 0}}>
        <div style={{fontFamily: 'Anton', fontSize: 64, color: '#fff', whiteSpace: 'nowrap'}}>{job.title} <span style={{color: GOLD}}>// {job.title2}</span></div>
        <div style={{...mono, marginTop: 2}}>{`PART ${String(pi + 1).padStart(2, '0')}/${String(parts.length).padStart(2, '0')} · X-RAY MODE · ZOOM ${camState.current.s.toFixed(2)}x`}</div>
      </div>
      {parts.map((p, i) => (
        <div key={i} id={`card${i}`} className="abs card" style={{opacity: 0}}>
          <div className="tk" /><div className="ix">{String(i + 1).padStart(2, '0')}</div><div className="ty">{p.ty}</div>
          <div className="nm" style={{fontSize: p.nm.length > 15 ? 64 : 76}}>{p.nm}</div>
          <div className="barbg"><div className="bar" /></div>
        </div>
      ))}
      <div id="tags">
        <svg className="abs" width={1080} height={1920} style={{left: 0, top: 0}}>
          {parts.map((p, i) => {
            const [lx, ly] = p.tag; const above = ly < CY; const ey = above ? ly + 86 : ly - 8;
            return (<g key={i}><path className="tagline" d={`M${p.w[0]} ${p.w[1]} L${p.w[0]} ${ey} L${lx + 6} ${ey}`} stroke={GOLD} strokeWidth={1.6} fill="none" />
              <circle className="tagdot" cx={p.w[0]} cy={p.w[1]} r={7} fill={GOLD} /><circle className="tagdot" cx={p.w[0]} cy={p.w[1]} r={16} fill="none" stroke="rgba(255,212,0,.5)" /></g>);
          })}
        </svg>
        {parts.map((p, i) => (
          <div key={i} className="abs tag" style={{left: p.tag[0], top: p.tag[1], opacity: 0}}>
            <div className="ty"><span className="ix">{String(i + 1).padStart(2, '0')}</span>{p.ty}</div><div className="nm">{p.nm}</div>
          </div>
        ))}
      </div>
      <div id="badge" className="abs" style={{left: 0, width: 1080, top: 214, textAlign: 'center', opacity: 0}}>
        <span style={{display: 'inline-block', border: `1px solid ${GOLD}`, padding: '8px 22px', fontFamily: 'RajB', fontSize: 28, letterSpacing: 8, color: GOLD, background: 'rgba(255,212,0,.08)'}}>{job.badge}</span>
      </div>
      <div id="save1" className="abs" style={{left: 0, width: 1080, top: 330, textAlign: 'center', fontFamily: 'Anton', fontSize: 200, lineHeight: 1, color: '#fff', whiteSpace: 'nowrap'}}>SAVE THIS</div>
      <div id="save2" className="abs" style={{left: 0, width: 1080, top: 530, textAlign: 'center', fontFamily: 'Anton', fontSize: 200, lineHeight: 1, color: GOLD, opacity: 0, whiteSpace: 'nowrap'}}>BUILD</div>
      <svg id="lring" className="abs" width={360} height={360} style={{left: 360, top: 960, opacity: 0}}>
        <circle cx={180} cy={180} r={160} fill="none" stroke={GOLD} strokeWidth={3} strokeDasharray="14 12" />
        <circle cx={180} cy={180} r={174} fill="none" stroke="rgba(255,212,0,.35)" strokeWidth={1} />
      </svg>
      <img id="logo" className="abs" src={staticFile('logo.png')} style={{left: 410, top: 1010, width: 260, height: 260, opacity: 0}} />
      <div id="follow" className="abs" style={{left: 0, width: 1080, top: 1320, textAlign: 'center', fontFamily: 'RajB', fontSize: 54, letterSpacing: 10, color: '#fff', opacity: 0}}>FOLLOW <span style={{color: GOLD}}>@PLAYHQTV</span></div>
      <div id="src" className="abs" style={{...mono, left: 0, width: 1080, top: 1404, textAlign: 'center', color: 'rgba(255,255,255,.45)', opacity: 0}}>{job.source}</div>
      <div id="hud" className="abs" style={{left: 0, top: 0, width: 1080, opacity: 0}}>
        <div className="abs" style={{...mono, left: 70, top: 192}}>{hudL}</div>
        <div className="abs" style={{...mono, right: 70, top: 192, textAlign: 'right'}}>{`F ${String(frame).padStart(4, '0')}  RY ${ry.toFixed(1)}°`}</div>
      </div>
      <div id="flash" className="abs" style={{inset: 0, opacity: 0, background: 'radial-gradient(60% 40% at 50% 47%,#fff8dc,rgba(255,220,120,.4) 50%,transparent 80%)', mixBlendMode: 'screen'}} />
      <div className="abs" style={{inset: 0, opacity: 0.07, mixBlendMode: 'overlay', backgroundImage: `url(${staticFile(`grain${frame % 4}.png`)})`, backgroundSize: '1080px 1920px'}} />
      <div className="abs" style={{inset: 0, background: 'radial-gradient(130% 85% at 50% 48%,transparent 50%,rgba(0,0,0,.85) 100%)'}} />
      {(job as any).debug ? <div className="abs" style={{left: 20, top: 1600, width: 1040, color: '#f0f', fontSize: 26, fontFamily: 'DejaVu Sans Mono', whiteSpace: 'pre-wrap', zIndex: 99}}>{dbg + ' tl=' + (tl.current ? tl.current.time().toFixed(2) : 'none')}</div> : null}
      {job.bed ? <Audio src={staticFile(job.bed)} volume={0.9} /> : null}
      {job.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.at * fps)} layout="none"><Audio src={staticFile('sfx/' + s.file)} volume={s.vol ?? 0.7} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
