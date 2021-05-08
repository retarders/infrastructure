FROM java:8-jdk
WORKDIR /server 

# download paper
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/SportPaper.jar

# download plugins
RUN mkdir plugins
RUN wget https://github.com/PGMDev/PGM/releases/download/v0.11/PGM.jar -O plugins/pgm.jar

CMD ["java", "-jar", "./SportPaper.jar", "--online-mode", "false"]

EXPOSE 25565
