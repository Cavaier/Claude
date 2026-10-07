
(function(){
  var $=function(id){return document.getElementById(id)};
  var user=null,db=null,room=null,myId=null;
  var ready=false,roster=[],peers=[],claudeDoc=null,acts=[],names={},lastAt=null,myDoing=null;
  var KIND={working:'Working on',waiting:'Waiting for Claude',note:'Note',claude:'Claude',start:'Claude started',done:'Claude saved'};
  function ago(t){if(!t)return'';var s=Math.max(0,(Date.now()-t)/1000);if(s<60)return'just now';if(s<3600)return Math.round(s/60)+' min ago';if(s<86400)return Math.round(s/3600)+' h ago';return Math.round(s/86400)+' d ago'}
  function hm(t){var d=new Date(t);return d.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
  function nm(id){return (id&&names[id]&&names[id].name)||'Someone'}
  async function resolve(ids){
    if(!user)return;ids=ids.filter(function(i){return i&&!names[i]});if(!ids.length)return;
    try{var p=await user.profiles(ids);for(var k in p)names[k]=p[k]}catch(e){}
  }
  function where(){
    var best='top';document.querySelectorAll('.entry').forEach(function(e){if(e.getBoundingClientRect().top<160)best=e.id});return best;
  }
  function whereLabel(w){return w&&/^e\d\d$/.test(w)?'on '+w.slice(1):'overview'}

  function renderWho(){
    var box=$('lvWho');box.textContent='';
    var people={},order=[];
    function get(id){if(!people[id]){people[id]={id:id,online:false,me:id===myId};order.push(id)}return people[id]}
    roster.forEach(function(r){if(r.id)get(r.id).seen=r.lastSeen});
    var agents=[];
    peers.forEach(function(p){
      if(p.kind==='agent'){agents.push(p);return}
      var x=get(p.by||p.peer);x.online=true;if(p.isMe)x.me=true;
      if(!x.pr||p.isMe)x.pr=p.presence||{};
    });
    if(myId)get(myId).me=true;
    if(room&&myId)get(myId).online=true;
    order.sort(function(a,b){var A=people[a],B=people[b];return (B.me-A.me)||(B.online-A.online)||((B.seen||0)-(A.seen||0))});
    var others=order.filter(function(id){return !people[id].me&&people[id].online}).length;
    $('lvDot').className='dot'+(others?' on':'');
    $('lvDot').title=others?'Someone else is on the page now':'Nobody else is on the page now';
    if(!order.length&&!agents.length){box.appendChild(el('span',null,ready?(room?'Just you':'Live presence unavailable in this view'):'Connecting…'));return}
    order.forEach(function(id){
      var x=people[id],pr=x.pr||{};
      var c=el('span','chip'+(x.online?'':' off'));
      c.appendChild(el('span','pd'+(x.online?' on':'')));
      var label=nm(id)+(x.me?' (you)':'');
      c.appendChild(el('span',null,label));
      var at;
      if(x.online){at=whereLabel(typeof pr.at==='string'?pr.at:'');if(typeof pr.doing==='string'&&pr.doing)at+=' · '+pr.doing}
      else at=x.seen?'offline · seen '+ago(x.seen):'offline';
      c.appendChild(el('span','at',at));
      c.title=label+' — '+(x.online?'online, ':'')+at;
      box.appendChild(c);
    });
    agents.forEach(function(){var c=el('span','chip');c.appendChild(el('span','pd on'));c.appendChild(el('span',null,'Claude'));box.appendChild(c)});
  }
  function renderClaude(){
    var b=$('lvClaude');b.textContent='';
    var d=claudeDoc;
    var dot=el('span','dot');b.appendChild(dot);
    if(!db){b.appendChild(el('span',null,''));b.style.display='none';return}
    b.style.display='';
    if(!d){b.appendChild(el('span',null,'Claude: idle'));return}
    var stale=d.at&&(Date.now()-d.at>45*60000);
    if(d.state==='working'&&!stale){dot.className='dot work';b.appendChild(el('span',null,'Claude working: '+(d.task||'a change')+' · '+ago(d.at)))}
    else{b.appendChild(el('span',null,'Claude idle'+(d.task?' · last: '+d.task:'')+(d.at?' · '+ago(d.at):'')))}
    b.title=b.textContent;
  }
  function renderLog(){
    var ol=$('lvLog');ol.textContent='';
    if(!db){var li=el('li');li.appendChild(el('time'));li.appendChild(el('span','hint','The activity log is unavailable in this view.'));ol.appendChild(li);return}
    if(!acts.length){var l2=el('li');l2.appendChild(el('time'));l2.appendChild(el('span','hint','No activity yet.'));ol.appendChild(l2);return}
    acts.forEach(function(a){
      var li=el('li');var t=el('time',null,typeof a.at==='number'?hm(a.at):'');if(typeof a.at==='number')t.title=new Date(a.at).toLocaleString();li.appendChild(t);
      var s=el('span');
      var who=a.actor==='claude'?(typeof a.label==='string'&&a.label?a.label:'Claude'):nm(a.by);
      s.appendChild(el('span','k',KIND[a.kind]||'Note'));
      s.appendChild(el('b',null,who));
      s.appendChild(document.createTextNode(' — '+(typeof a.text==='string'?a.text:'')));
      li.appendChild(s);ol.appendChild(li);
    });
  }
  function renderAll(){renderWho();renderClaude();renderLog()}

  $('lvBtn').addEventListener('click',function(){var p=$('lvPanel');p.hidden=!p.hidden;this.setAttribute('aria-expanded',String(!p.hidden))});
  $('lvForm').addEventListener('submit',async function(ev){
    ev.preventDefault();var kind=$('lvKind').value,text=$('lvText').value.trim();if(!text)return;
    if(room&&kind!=='note'){myDoing=(kind==='waiting'?'waiting for Claude: ':'')+text.slice(0,80);try{await room.presence({doing:myDoing})}catch(e){}renderWho()}
    if(db){try{await db.collection('activity').add({at:Date.now(),by:myId,kind:kind,text:text})}catch(e){alert('Could not post: you may only have view access to this page.');return}}
    $('lvText').value='';
  });
  $('lvClear').addEventListener('click',async function(){myDoing=null;if(room){try{await room.presence({doing:null})}catch(e){}}renderWho()});

  var tick=null;
  function track(){
    if(tick)return;tick=setTimeout(function(){tick=null;var w=where();if(w!==lastAt&&room){lastAt=w;room.presence({at:w}).catch(function(){})}},400);
  }

  renderAll();
  (async function(){
    var c=window.claude;if(!c||!c.use){ready=true;renderAll();return}
    var r=await Promise.all([c.use('user'),c.use('db'),c.use('room')]);
    user=r[0];db=r[1];room=r[2];
    if(user){try{myId=await user.id()}catch(e){}}
    if(room){
      room.onPeers(async function(ch){peers=ch.peers.slice();await resolve(peers.map(function(p){return p.by}));renderWho()},function(){room=null;renderWho()});
      lastAt=where();room.presence({at:lastAt}).catch(function(){});
      window.addEventListener('scroll',track,{passive:true});
    }
    if(db){
      if(myId){
        var seenRef=db.doc('people/'+myId);
        seenRef.set({lastSeen:Date.now()}).catch(function(){});
        window.addEventListener('pagehide',function(){seenRef.set({lastSeen:Date.now()}).catch(function(){})});
      }
      db.collection('people').limit(50).onSnapshot(async function(s){
        roster=s.docs.map(function(d){var v=d.data()||{};return {id:d.id,lastSeen:typeof v.lastSeen==='number'?v.lastSeen:0}});
        await resolve(roster.map(function(r){return r.id}));renderWho();
      },function(){});
      db.doc('live/claude').onSnapshot(function(s){claudeDoc=s.exists?s.data():null;renderClaude()},function(){});
      db.collection('activity').orderBy('at','desc').limit(40).onSnapshot(async function(s){
        acts=s.docs.map(function(d){return d.data()||{}});
        await resolve(acts.map(function(a){return a.by}));renderLog();
      },function(){});
    }
    ready=true;renderAll();
    setInterval(function(){renderClaude();renderWho()},30000);
  })();
})();
