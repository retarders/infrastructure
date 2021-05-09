FROM java:8-jdk

ADD configs /server

WORKDIR /server 

# download paper
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/SportPaper.jar

# download plugins
RUN wget https://github.com/retarders/dalobby/releases/download/1.1/dalobby-da.jar -O plugins/DaLobby.jar
RUN wget /mnt/data/WorldEdit/worldedit-bukkit/build/libs/worldedit-bukkit-7.3.0-SNAPSHOT-dist.jar -O plugins/worldedit.jar

# copy configs
# ADD configs/server.properties /server/server.properties
# ADD configs/ops.json /server/ops.json
# ADD configs/sportpaper.ytml /server/sportpaper.yml

CMD ["java", "-jar", "./SportPaper.jar", "--online-mode", "false"]

EXPOSE 25565
