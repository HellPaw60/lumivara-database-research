er(e.tier))||1)),r=Math.max(0,Math.floor(Number(e.refine))||0);return Math.ceil(Rs[n-1]*(100+r*Cs)*t/(100*EA))}function Hs(A){const e=(A.gear??[]).filter(t=>ye(A,t)>0);return{items:e,cost:e.reduce((t,n)=>t+Os(A,n),0)}}const Ns=A=>A.area===RA.area&&Math.hyp

uipment:.0125,card:.001,bossCard:.01,relicBox:.01,refineStone:.01,extraStat:.25,aspdAccessory:.3},Ra=70,Cc=A=>A>=Ra?ie.refineStone:0,Ce={startLevel:20,perLevel:.0025,max:.3},Ca=A=>Math.max(0,Math.min(Ce.max,(A-Ce.startLevel)*Ce.perLevel)),Ic=(A,e)=>1-Ca(A)*(1-M

||c,w4=new Set(["casting","skill","hit","potion","refine","use","emote"]);function C4(h,c,S,T){return h==="all"||!w4.has(c.type)||!c.player||c.player===S||c.victim===S?!0:T(c.player)}function M4(){if(document.getElementById("player-display"))return;const h

