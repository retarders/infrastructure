FROM java:8-jdk
WORKDIR /server 

# download travertine
# not sure if this is the correct version to use in our case
RUN wget https://papermc.io/api/v2/projects/travertine/versions/1.16/builds/183/downloads/travertine-1.16-183.jar

# download plugins
RUN mkdir plugins
RUN wget https://github.com/retarders/damessage/releases/download/1.0/damessage-1.0-SNAPSHOT.jar -O plugins/damessage.jar

CMD ["java", "-jar", "./travertine-1.16-183.jar.jar"]
