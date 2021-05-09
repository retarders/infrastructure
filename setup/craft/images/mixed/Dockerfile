FROM java:8-jdk

ADD configs /server
WORKDIR /server 

# download paper
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/SportPaper.jar

# download plugins
RUN mkdir plugins
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/PGM.jar -O plugins/pgm.jar
RUN wget https://maven.enginehub.org/repo/com/sk89q/worldedit/worldedit-bukkit/7.3.0-SNAPSHOT/worldedit-bukkit-7.3.0-20210429.114142-33.jar -O plugins/WorldEdit.jar

# copy configs
# RUN mkdir /server/plugins/PGM
# ADD configs/PGM/config.yml /server/plugins/PGM/config.yml
# ADD configs/PGM/map-pools.yml /server/plugins/PGM/map-pools.yml
# 
# ADD configs/ops.json /server/ops.json
# ADD configs/sportpaper.yml /server/sportpaper.yml

CMD ["java", "-jar", "./SportPaper.jar", "--online-mode", "false"]

EXPOSE 25565
