1/player.json"):h.load.spritesheet(A,Yw(A),{frameWidth:96,frameHeight:96}));if(w){h.load.atlas("npc-blacksmith","/npc/blacksmith-v1/npc.png","/npc/blacksmith-v1/npc.json"),h.load.atlas("npc-merchant","/npc/merchant-v2/player.png","/npc/merchant-v2/player.json"),h.load.atlas("npc-broker","/npc/merchant-v1/npc.png","/npc/merchant-v1/npc.json"),h.load.atlas("banker","/jobs/banker-v2/player.png","/jobs/banker-v

6/player","player-thief":"/jobs/thief-v6/player","player-acolyte":"/jobs/acolyte-v2/player","player-merchant":"/jobs/merchant-v1/player","player-mamushi":"/jobs/mamushi-v2/player","player-kensei":"/jobs/kensei-v1/player","player-nekobaku":"/jobs/nekobaku-v1/player"},FA=h=>h&&Qv["player-"+h]?"player-"+h:"player";function Z2(h,c){const S=Qv[c];S&&h.atlas(c,S+".png",S+".json")}function DA(h,c){return c==="pl

tlas("npc-merchant","/npc/merchant-v2/player.png","/npc/merchant-v2/player.json"),h.load.atlas("npc-broker","/npc/merchant-v1/npc.png","/npc/merchant-v1/npc.json"),h.load.atlas("banker","/jobs/banker-v2/player.png","/jobs/banker-v2/player.json"),h.load.atlas("stat-master","/jobs/stat-master-v1/player.png","/jobs/stat-master-v1/player.json"),h.load.atlas("fusion-master","/npc/fusion-master-v1/player.png"

n"),h.load.atlas("banker","/jobs/banker-v2/player.png","/jobs/banker-v2/player.json"),h.load.atlas("stat-master","/jobs/stat-master-v1/player.png","/jobs/stat-master-v1/player.json"),h.load.atlas("fusion-master","/npc/fusion-master-v1/player.png","/npc/fusion-master-v1/player.json");for(const A of["hammer","anvil","success","broken"])h.load.image("forge-"+A,"/effects/forge-"+A+"-v1.png")}h.load.image("ember-

s("stat-master","/jobs/stat-master-v1/player.png","/jobs/stat-master-v1/player.json"),h.load.atlas("fusion-master","/npc/fusion-master-v1/player.png","/npc/fusion-master-v1/player.json");for(const A of["hammer","anvil","success","broken"])h.load.image("forge-"+A,"/effects/forge-"+A+"-v1.png")}h.load.image("ember-bolt","/effects/ember-bolt-v1.png"),h.load.image("flame-burst","/effects/flame-burst-v2.png"),h.loa

n"),h.load.atlas("npc-broker","/npc/merchant-v1/npc.png","/npc/merchant-v1/npc.json"),h.load.atlas("banker","/jobs/banker-v2/player.png","/jobs/banker-v2/player.json"),h.load.atlas("stat-master","/jobs/stat-master-v1/player.png","/jobs/stat-master-v1/player.json"),h.load.atlas("fusion-master","/npc/fusion-master-v1/player.png","/npc/fusion-master-v1/player.json");for(const A of["hammer","anvil","success

,"matk",14221296),buff:"remedy"},mammonite:{...f("merchant","Gold Strike",1,2,3500,72,"enemy"),cooldownFromAspd:!0},cartstrike:f("merchant","Cart Strike",3,3.5,3e3,100,"area","damage","atk",16755810),hammerfall:f("merchant","Quake Hammer",5,4,4500,150,"area"

