FROM codechimpio/vips-alpine:latest
LABEL authors="Tahsin Kurc, Erich Bremer"

RUN 	apk update && \
		apk upgrade && \
		apk add bash && \
		apk add openjdk8-jre && \
        apk update && apk add ca-certificates && update-ca-certificates && apk add openssl && \
		apk add --no-cache python3-dev libstdc++ && \
    	apk add --no-cache g++ && \
    	ln -s /usr/include/locale.h /usr/include/xlocale.h && \
		apk add python3 && \
		pip3 install numpy && \
		pip3 install pandas
RUN		wget --no-check-certificate https://downloads.openmicroscopy.org/bio-formats/6.2.0/artifacts/bftools.zip && \
		cd /usr/bin && unzip /bftools.zip && \
		mv bftools/* . && rmdir bftools && \
		rm -f /bftools.zip && cd /root	

WORKDIR /root

COPY . /root/.
RUN  chmod 0755 /root/run_convert*.sh 

ENV  PROCAWKDIR=/root
ENV  JVM_ARGS="-Xms2048m -Xmx2048m"
ENV PATH=.:$PATH

CMD 	["run_convert.sh"]
