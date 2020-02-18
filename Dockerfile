FROM codechimpio/vips-alpine:latest
MAINTAINER Tahsin Kurc

RUN 	apk update && \
	apk upgrade && \
	apk add --update openssl && \
	apk add --update bash && \
	apk add --update openjdk7-jre && \
	wget --no-check-certificate http://downloads.openmicroscopy.org/bio-formats/5.9.0/artifacts/bftools.zip && \
	cd /usr/bin && unzip /bftools.zip && \
	mv bftools/* . && rmdir bftools && \
	rm -f /bftools.zip && cd /root	

ENV 	VIPS_TMPDIR /tmp
ENV 	PROCAWKDIR /root

COPY 	run_convert*.sh /usr/bin/
COPY 	process.awk $PROCAWKDIR/
RUN  	chmod 0755 /usr/bin/run_convert*.sh

RUN 	export JVM_ARGS="-Xms2048m -Xmx2048m"

CMD 	["/bin/bash"]
