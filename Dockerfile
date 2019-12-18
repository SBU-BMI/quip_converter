FROM codechimpio/vips-alpine:latest
LABEL authors="Erich Bremer, Tahsin Kurc"
RUN 	apk update && \
	apk upgrade && \
	apk add bash && \
	apk add openjdk8-jre && \
        apk update && apk add ca-certificates && update-ca-certificates && apk add openssl
RUN	wget --no-check-certificate https://downloads.openmicroscopy.org/bio-formats/6.3.1/artifacts/bftools.zip && \
	cd /usr/bin && unzip /bftools.zip && \
	mv bftools/* . && rmdir bftools && \
	rm -f /bftools.zip && cd /root	
ENV 	PROCAWKDIR /root
COPY 	run_convert*.sh /usr/bin/
COPY 	process.awk $PROCAWKDIR/
RUN  	chmod 0755 /usr/bin/run_convert*.sh
RUN 	export JVM_ARGS="-Xms2048m -Xmx2048m"
CMD 	["/bin/bash"]
