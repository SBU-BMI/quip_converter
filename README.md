# quip_converter
Convert vendor format to tiled, multires tiff format

building:

	git clone https://github.com/SBU-BMI/quip_converter.git

	docker build -t quip_converter quip_converter

Sample usage:

A whole folder.  In this example, /home/me/images contains a folder called svsfiles.

	docker run -v /home/me/images:/tmp quip_converter run_convert.sh /tmp/svsfiles svs

A single file

	docker run -v /home/me:/tmp quip_converter run_convert_wsi.sh /tmp/001738-000050_01_01_20180710.vsi /tmp/big.tif /tmp/multi.tif
