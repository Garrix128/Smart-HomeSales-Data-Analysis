# SpringBoot后端Dockerfile
FROM openjdk:8-jre-alpine

WORKDIR /app

COPY target/Smart_Home_Analysis-1.0-SNAPSHOT.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]



