/* MYSense × Velora — behaviour layer (vanilla, no deps) */
(function(){
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- menu ---- */
  const menu=$('.menu'), burger=$('.burger'), close=$('.menu__close');
  const setMenu=o=>{ if(!menu) return; menu.classList.toggle('is-open',o); document.body.classList.toggle('menu-open',o); burger&&burger.setAttribute('aria-expanded',o); };
  burger&&burger.addEventListener('click',()=>setMenu(true));
  close&&close.addEventListener('click',()=>setMenu(false));
  document.addEventListener('keydown',e=>{ if(e.key==='Escape') setMenu(false); });
  $$('.menu__links a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));

  /* ---- scroll reveal (template: opacity 0 → 1, translateY 150 → 0, 1.2s) ---- */
  const io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }),{rootMargin:'0px 0px -8% 0px',threshold:0.05});
  $$('.rv,.words').forEach(el=>{ if(reduce){el.classList.add('in');} else io.observe(el); });
  /* staggered children */
  $$('[data-stagger]').forEach(g=>{ const step=parseFloat(g.dataset.stagger)||0.1; $$(':scope > .rv',g).forEach((c,i)=>c.style.transitionDelay=(i*step)+'s'); });
  /* word-by-word reveal */
  $$('.words').forEach(w=>{ if(w.dataset.split) return; const words=w.textContent.trim().split(/\s+/); w.innerHTML=words.map((t,i)=>`<span${w.classList.contains('scrub')?'':` style="transition-delay:${(i*0.03).toFixed(2)}s"`}>${t}</span>`).join(' '); w.dataset.split='1'; });

  /* ---- accordions (services panel + FAQ) ---- */
  $$('.acc').forEach(acc=>{
    $$('.acc__item',acc).forEach(item=>{
      const btn=$('.acc__title',item);
      btn&&btn.addEventListener('click',()=>{
        const open=item.classList.contains('is-open');
        $$('.acc__item',acc).forEach(i=>{ i.classList.remove('is-open'); $('.acc__title',i)?.setAttribute('aria-expanded','false'); });
        if(!open){ item.classList.add('is-open'); btn.setAttribute('aria-expanded','true'); }
      });
    });
  });
  $$('.faq__item').forEach(item=>{
    const q=$('.faq__q',item);
    q&&q.addEventListener('click',()=>{ const o=item.classList.toggle('is-open'); q.setAttribute('aria-expanded',o); });
  });

  /* ---- testimonial slider (arrows + drag, spring-like ease, infinite loop) ---- */
  $$('.slider').forEach(sl=>{
    const track=$('.slider__track',sl); if(!track) return;
    const cards=$$('.tcard',track); if(cards.length<2) return;
    const per=()=>innerWidth<810?1:innerWidth<1200?2:3;
    // clone for infinite feel
    cards.forEach(c=>track.appendChild(c.cloneNode(true)));
    cards.slice().reverse().forEach(c=>track.insertBefore(c.cloneNode(true),track.firstChild));
    const n=cards.length; let idx=n; let dragging=false,startX=0,startT=0,cur=0;
    const step=()=>{ const c=$('.tcard',track); return c.getBoundingClientRect().width+10; };
    const go=(i,anim=true)=>{ idx=i; if(!anim) track.classList.add('dragging'); track.style.transform=`translateX(${-idx*step()}px)`; if(!anim){ track.offsetHeight; track.classList.remove('dragging'); } };
    const norm=()=>{ if(idx>=2*n){ go(idx-n,false);} if(idx<n-per()){ go(idx+n,false);} };
    track.addEventListener('transitionend',norm);
    const prev=$('.arrows [data-prev]',sl.parentElement)||$('.arrows [data-prev]',sl.closest('section')), next=$('.arrows [data-next]',sl.parentElement)||$('.arrows [data-next]',sl.closest('section'));
    prev&&prev.addEventListener('click',()=>go(idx-1)); next&&next.addEventListener('click',()=>go(idx+1));
    go(n,false); addEventListener('resize',()=>go(idx,false));
    // drag
    const pd=e=>{ dragging=true; startX=e.clientX; startT=-idx*step(); track.classList.add('dragging'); track.setPointerCapture(e.pointerId); };
    const pm=e=>{ if(!dragging) return; cur=startT+(e.clientX-startX); track.style.transform=`translateX(${cur}px)`; };
    const pu=e=>{ if(!dragging) return; dragging=false; track.classList.remove('dragging'); const d=e.clientX-startX; if(Math.abs(d)>60) go(idx+(d<0?1:-1)); else go(idx); };
    track.addEventListener('pointerdown',pd); track.addEventListener('pointermove',pm); track.addEventListener('pointerup',pu); track.addEventListener('pointercancel',pu);
    $$('a',track).forEach(a=>a.addEventListener('click',e=>{ if(Math.abs(cur-startT)>5) e.preventDefault(); }));
  });

  /* ---- hero video pause/play ---- */
  $$('.hero__pause').forEach(b=>{
    const v=$('video',b.parentElement); if(!v) return;
    const ic=(p)=>b.innerHTML=p?'<svg viewBox="0 0 14 14"><path d="M3 2.5v9l8-4.5z" fill="currentColor"/></svg>':'<svg viewBox="0 0 14 14"><rect x="3" y="2" width="2.6" height="10" rx="1" fill="currentColor"/><rect x="8.4" y="2" width="2.6" height="10" rx="1" fill="currentColor"/></svg>';
    ic(false);
    b.addEventListener('click',()=>{ if(v.paused){v.play();ic(false);} else {v.pause();ic(true);} });
    if(reduce){ v.pause(); ic(true); }
  });

  /* ---- forms (mockup: prevent navigation, show state) ---- */
  $$('form[data-mock]').forEach(f=>f.addEventListener('submit',e=>{ e.preventDefault(); const b=$('button[type=submit]',f); if(b){ const t=b.textContent; b.textContent='Thank you — we will be in touch'; b.disabled=true; setTimeout(()=>{b.textContent=t;b.disabled=false;},3500);} }));

  /* ---- hero rotating word ---- */
  $$('.rotator').forEach(r=>{
    const items=$$('span',r); if(items.length<2) return;
    let i=0; items[0].classList.add('is-in');
    if(reduce) return;
    setInterval(()=>{ const cur=items[i]; i=(i+1)%items.length; const nxt=items[i];
      cur.classList.remove('is-in'); cur.classList.add('is-out'); nxt.classList.remove('is-out'); nxt.classList.add('is-in');
      setTimeout(()=>cur.classList.remove('is-out'),600); },2400);
  });

  /* ---- scroll-scrub word darkening (grey → ink as the paragraph scrolls through) ---- */
  const scrubs=$$('.words.scrub');
  if(scrubs.length){
    const update=()=>{ const vh=innerHeight; scrubs.forEach(w=>{ const r=w.getBoundingClientRect(); const start=vh*0.9, end=vh*0.35; const p=Math.min(1,Math.max(0,(start-r.top)/(r.height+start-end))); const sp=$$('span',w); const n=Math.round(p*sp.length); sp.forEach((x,i)=>x.classList.toggle('on',i<n)); }); };
    let tick=false; addEventListener('scroll',()=>{ if(!tick){ tick=true; requestAnimationFrame(()=>{update();tick=false;}); } },{passive:true}); addEventListener('resize',update); update(); setTimeout(update,300);
  }

  /* ---- current year ---- */
  $$('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());
})();
