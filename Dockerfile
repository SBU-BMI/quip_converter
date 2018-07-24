FROM codechimpio/vips-alpine:latest
MAINTAINER Tahsin Kurc

RUN 	apk update && \
	apk upgrade && \
	apk add bash && \
	apk add openjdk7-jre && \
	wget http://downloads.openmicroscopy.org/bio-formats/5.9.0/artifacts/bftools.zip && \
	cd /usr/bin && unzip /bftools.zip && \
	mv bftools/* . && rmdir bftools && \
	rm -f /bftools.zip && cd /root	

ENV 	VIPS_TMPDIR /tmp
ENV 	PROCAWKDIR /root

COPY 	run_convert*.sh /usr/bin/
COPY 	process.awk $PROCAWKDIR/
RUN  	chmod 0755 /usr/bin/run_convert*.sh

CMD 	["/bin/bash"]
