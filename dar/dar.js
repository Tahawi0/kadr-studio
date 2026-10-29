(function(){
const D=window.DAR;
const TYPE={apartment:'شقة',duplex:'دوبلكس',townhouse:'تاون هاوس',twin:'توين هاوس',villa:'فيلا'};
const fmt=n=>(n/1e6).toLocaleString('ar-EG',{maximumFractionDigits:1})+' مليون جنيه';
const ar=n=>n.toLocaleString('ar-EG');
let units=[];
function fromMada(m){const p=m.project;return m.units.map(u=>({id:'mada-'+u.id,type:u.type,ar:u.ar,area_name:p.name+' — بين التجمع والعاصمة',beds:u.beds,baths:null,area:u.area,land:u.land,price:u.price,
 status:'تسليم '+ar(p.delivery),pay:'مقدم من '+ar(Math.min(...p.down_options))+'٪ وتقسيط حتى '+ar(Math.max(...p.years_options))+' سنوات',img:u.img,source:'developer',dev:p.developer}));}
function load(m){units=fromMada(m).concat(D.resale);
 const areas=[...new Set(units.map(u=>u.area_name))];const sa=document.getElementById('fArea');areas.forEach(a=>{const o=document.createElement('option');o.value=a;o.textContent=a;sa.appendChild(o);});render();}
// Live link: read Mada's units from the shared data file; fall back to the copy baked in at build time.
fetch('../data/mada-units.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject()).then(load).catch(()=>load(D.mada));
const $=id=>document.getElementById(id);let src='';
function filtered(){const a=$('fArea').value,t=$('fType').value,mx=+$('fMax').value||Infinity,b=+$('fBeds').value||0;
 let r=units.filter(u=>(!a||u.area_name===a)&&(!t||u.type===t)&&u.price<=mx&&u.beds>=b&&(!src||u.source===src));
 const s=$('fSort').value;r.sort((x,y)=>s==='price-desc'?y.price-x.price:s==='area-desc'?y.area-x.area:x.price-y.price);return r;}
function render(){const r=filtered();$('cnt').textContent=ar(r.length);$('empty').hidden=!!r.length;
 $('grid').innerHTML=r.map(u=>`<button class="card" type="button" data-id="${u.id}"><div class="ph"><img src="../assets/img/${u.img}-s.webp" alt="${u.ar}" loading="lazy"><span class="badge${u.source==='developer'?' dev':''}">${u.source==='developer'?'من المطوّر':'ريسيل'}</span></div>
 <div class="c-body"><p class="c-loc">${u.area_name}</p><h3>${u.ar}</h3><div class="c-spec"><span>${ar(u.area)} م²</span><span>${ar(u.beds)} غرف</span><span>${u.status}</span></div>
 <p class="c-price">${fmt(u.price)}</p><p class="c-pay">${u.pay}</p></div></button>`).join('');}
['fArea','fType','fMax','fBeds','fSort'].forEach(i=>$(i).addEventListener('change',render));
$('fSrc').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;src=b.dataset.v;$('fSrc').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));render();});
$('featShow').addEventListener('click',()=>{const b=$('fSrc').querySelector('[data-v="developer"]');b.click();});
let cur=null,lastFocus=null;
function open(u){cur=u;lastFocus=document.activeElement;$('mImg').src='../assets/img/'+u.img+'.webp';$('mImg').alt=u.ar;$('mTag').textContent=(u.source==='developer'?'من المطوّر · '+u.dev:'ريسيل · '+u.area_name);
 $('mTitle').textContent=u.ar;$('mPrice').textContent=fmt(u.price);
 const rows=[['المساحة',ar(u.area)+' م²'],u.land?['الأرض',ar(u.land)+' م²']:null,['الغرف',ar(u.beds)],u.baths?['الحمامات',ar(u.baths)]:null,['الحالة',u.status],['طريقة الدفع',u.pay]].filter(Boolean);
 $('mSpec').innerHTML=rows.map(([a,b])=>`<li><span>${a}</span><b>${b}</b></li>`).join('');$('modal').hidden=false;document.body.style.overflow='hidden';$('mClose').focus();}
function close(){$('modal').hidden=true;document.body.style.overflow='';$('lErr').hidden=true;if(lastFocus)lastFocus.focus();}
$('grid').addEventListener('click',e=>{const c=e.target.closest('.card');if(c)open(units.find(u=>u.id===c.dataset.id));});
$('mClose').addEventListener('click',close);$('modal').addEventListener('click',e=>{if(e.target.id==='modal')close();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('modal').hidden)close();});
$('lead').addEventListener('submit',e=>{e.preventDefault();const f=e.target,n=f.name.value.trim(),p=f.phone.value.replace(/\D/g,'');
 if(n.length<2||!/^01[0125]\d{8}$/.test(p)){$('lErr').hidden=false;$('lErr').textContent='اكتب اسمك ورقم موبايل مصري صحيح (١١ رقم يبدأ بـ 01).';return;}
 $('lErr').hidden=true;
 if(f.website.value)return;const lead={source:'dar-brokers-site',website:f.website.value,unit_id:cur.id,unit:cur.ar,price:cur.price,name:n,phone:p,time:f.time.value,ts:new Date().toISOString()};
 if(window.DAR_HOOK){fetch(window.DAR_HOOK,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(lead)}).catch(()=>{});}
 const msg='طلب تجريبي — دار بروكرز (مشروع مفاهيمي)\nالوحدة: '+cur.ar+' — '+cur.area_name+'\nالسعر: '+(cur.price/1e6)+' مليون جنيه\nالاسم: '+n+'\nالموبايل: '+p+'\nالتواصل: '+lead.time;
 window.open('https://wa.me/'+D.wa+'?text='+encodeURIComponent(msg),'_blank','noopener');});
})();