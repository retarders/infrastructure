FROM java:8-jdk
WORKDIR /server 

# download paper
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/SportPaper.jar

# download plugins
RUN mkdir plugins
RUN wget https://github.com/retarders/dalobby/releases/download/1.1/dalobby-da.jar -O plugins/DaLobby.jar

# copy configs
ADD server.properties /server/server.properties

ADD configs/ops.json /server/ops.json
ADD configs/sportpaper.ytml /server/sportpaper.yml

CMD ["java", "-jar", "./SportPaper.jar", "--online-mode", "false"]

EXPOSE 25565
