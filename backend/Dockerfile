FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

RUN mkdir -p /app/data

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
