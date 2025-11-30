USE GAME_DATABASE;

insert into Player Values ("Stiffler","agustin51@gmail,com","2025-10-14"),
(2,"Carlinho","agustin23@gmail,com","2025-12-01");

insert into Character_1 Values (1,1,"Loki",1,34),
(2,2,"Thor",3,3);

insert into Mission (1,"La fabrica de chocolate","Mision de prueba", 1),
(2,"Rescate en la torre","Mision de rescate", 2);

insert into CharacterMission Values (1,1,1),
(2,1,2);

insert into Item Values (1,"Hacha de batalla",1,3),
(2,"Escudo",2,1);
