FROM	ubuntu:18.04
LABEL	authors="Tahsin Kurc"

RUN		apt-get update && \
		apt-get -y install libvips libvips-dev libvips-tools openslide-tools
RUN     apt-get -y install openjdk-11-jre wget python3 python3-pip && \
		pip3 install numpy pandas 

WORKDIR /root

RUN		apt-get -y install zip bc && \
		wget --no-check-certificate https://downloads.openmicroscopy.org/bio-formats/6.2.0/artifacts/bftools.zip && \
	 	cd /usr/bin && unzip /root/bftools.zip && \
	 	rm -f /root/bftools.zip 	

COPY 	. /root/.
RUN  	chmod 0755 /root/run_convert*.sh 

ENV  	PROCAWKDIR=/root
ENV  	JVM_ARGS="-Xms2048m -Xmx2048m"
ENV 	PATH=.:/usr/bin/bftools:$PATH

CMD 	["run_convert.sh"]
