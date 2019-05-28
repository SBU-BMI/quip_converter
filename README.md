# quip_converter
Convert vendor format to tiled, multires tiff format

building:
	git clone https://github.com/SBU-BMI/quip_converter.git
	docker build -t quip_converter quip_converter

Sample usage:
	docker run -v /home/myhomedir:/tmp vips:latest run_convert_wsi.sh /tmp/001738-000050_01_01_20180710.vsi /tmp/big.tif /tmp/multi.tif
