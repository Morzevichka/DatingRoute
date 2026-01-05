FROM maven:3.9.11-amazoncorretto-21 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN rm -rf /root/.m2 && mvn clean package -Pprod -DskipTests -X

FROM amazoncorretto:21-alpine AS corretto-jdk
RUN apk add --no-cache binutils
RUN $JAVA_HOME/bin/jlink \
	--verbose \
	--add-modules ALL-MODULE-PATH \
	--strip-debug \
	--no-man-pages \
	--no-header-files \
	--compress=2 \
	--output /customjre

FROM alpine:3.23
ENV JAVA_HOME=/jre
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY --from=corretto-jdk /customjre $JAVA_HOME

ARG APPLICATION_USER=appuser
RUN adduser --no-create-home -u 1000 -D $APPLICATION_USER
RUN mkdir /app

COPY --from=builder /app/target/*.jar /app/app.jar

RUN chown -R $APPLICATION_USER /app \
	&& chmod 755 -R /app

WORKDIR /app

USER 1000

EXPOSE 8081

ENTRYPOINT ["/jre/bin/java", "-jar", "app.jar"]
