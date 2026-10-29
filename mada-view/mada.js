(function(){
const D=window.MADA, U=D.units, ar=n=>n.toLocaleString('ar-EG');
const money=n=>Math.round(n).toLocaleString('en-US')+' جنيه';
const sel=document.getElementById('cUnit');let down=10,years=8;
function pick(box,attr,set){box.addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;box.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c===b));set(+b.dataset[attr]);calc();});}
pick(document.getElementById('cDown'),'down',v=>down=v);pick(document.getElementById('cYears'),'years',v=>years=v);
let last=null;
function calc(){const u=U.find(x=>x.id===sel.value);const dp=u.price*down/100,rest=u.price-dp,m=rest/(years*12);
document.getElementById('oPrice').textContent=money(u.price);document.getElementById('oDown').textContent=money(dp)+' ('+ar(down)+'٪)';
document.getElementById('oMonth').textContent=money(m);document.getElementById('oQuarter').textContent=money(m*3);
last={unit:u.ar,price:u.price,down,years,monthly:Math.round(m)};
const f=document.getElementById('lead');if(f)f.unit.value=u.ar;}
sel.addEventListener('change',calc);calc();
document.querySelectorAll('.u-calc').forEach(b=>b.addEventListener('click',()=>{sel.value=b.dataset.id;calc();document.getElementById('calc').scrollIntoView({behavior:'smooth'});}));
const f=document.getElementById('lead'),err=document.getElementById('lErr');
f.addEventListener('submit',e=>{e.preventDefault();const n=f.name.value.trim(),p=f.phone.value.replace(/\D/g,'');
if(n.length<2||!/^01[0125]\d{8}$/.test(p)){err.hidden=false;err.textContent='من فضلك اكتب اسمك ورقم موبايل مصري صحيح (١١ رقمًا يبدأ بـ 01).';return;}
err.hidden=true;
const lead={source:'mada-view-landing',project:D.project.id,name:n,phone:p,unit:f.unit.value,budget:f.budget.value,time:f.time.value,calc:last,ts:new Date().toISOString()};
// Phase 2: POST lead to the n8n webhook that creates the record in Dar Brokers' CRM.
if(window.MADA_HOOK){fetch(window.MADA_HOOK,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(lead)}).catch(()=>{});}
const msg='طلب تجريبي — مدى ڤيو (مشروع مفاهيمي)\nالاسم: '+n+'\nالموبايل: '+p+'\nالوحدة: '+lead.unit+'\nالميزانية: '+lead.budget+'\nأنسب وقت: '+lead.time+(last?'\nالحاسبة: مقدم '+last.down+'٪ على '+last.years+' سنوات — قسط شهري '+last.monthly.toLocaleString('en-US')+' جنيه':'');
window.open('https://wa.me/'+window.MADA_WA+'?text='+encodeURIComponent(msg),'_blank','noopener');});
})();