FROM sonatype/nexus3:3.59.0

ENV NEXUS_KEYSTORE /nexus-keystore
ENV KEYSTOREPASSWORD=changeit
ENV KEYMANAGERPASSWORD=changeit
ENV TRUSTSTOREPASSWORD=changeit

USER root
RUN mkdir -p ${NEXUS_KEYSTORE} && chown nexus:nexus ${NEXUS_KEYSTORE}


RUN keytool -genkeypair \
        -keystore ${NEXUS_KEYSTORE}/keystore.jks \
        -storepass changeit \
        -keypass changeit \
        -alias jetty -keyalg RSA -keysize 2048 -validity 5000  \
        -dname "CN=*.local, OU=Nexus, O=NamLH, L=Unspecified, ST=Unspecified, C=VN" \
        -ext "SAN=DNS:nexus.local" -ext "BC=ca:true"

RUN sed 's|\(<Set name="KeyStorePath">\).*$|\1<Env name="NEXUS_KEYSTORE"/>/keystore.jks</Set>|' \
        -i /opt/sonatype/nexus/etc/jetty/jetty-https.xml \
     && sed 's|\(<Set name="KeyStorePassword">\).*$|\1<Env name="KEYSTOREPASSWORD"/></Set>|' \
        -i /opt/sonatype/nexus/etc/jetty/jetty-https.xml \
     && sed 's|\(<Set name="KeyManagerPassword">\).*$|\1<Env name="KEYMANAGERPASSWORD"/></Set>|' \
        -i /opt/sonatype/nexus/etc/jetty/jetty-https.xml \
     && sed 's|\(<Set name="TrustStorePath">\).*$|\1<Env name="NEXUS_KEYSTORE"/>/keystore.jks</Set>|' \
        -i /opt/sonatype/nexus/etc/jetty/jetty-https.xml \
     && sed 's|\(<Set name="TrustStorePassword">\).*$|\1<Env name="TRUSTSTOREPASSWORD"/></Set>|' \
        -i /opt/sonatype/nexus/etc/jetty/jetty-https.xml

EXPOSE 8443
USER nexus