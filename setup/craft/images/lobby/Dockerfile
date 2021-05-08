FROM java:8-jdk
WORKDIR /server 

# download paper
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/SportPaper.jar

# download plugins
RUN mkdir plugins
RUN wget https://github.com/retarders/dalobby/releases/download/1.1/dalobby-da.jar -O plugins/DaLobby.jar

CMD ["java", "-jar", "./SportPaper.jar", "--online-mode", "false", "--pvp", "false", "--allow-nether", "false", "--difficulty", "0"]

EXPOSE 25565
