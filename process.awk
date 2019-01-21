BEGIN {maxx=0; maxa=0; mpp_x=0.0; mpp_y=0.0; id=0;}
{
   val["PhysicalSizeX"] = 0.25
   val["PhysicalSizeY"] = 0.25
   for (i=2;i<=NF;i++) {
       split($i,a,"=");
       split(a[2],b,"\"");
       if (a[1]=="SizeX") val[a[1]] = b[2];
       if (a[1]=="SizeY") val[a[1]] = b[2];
       if (a[1]=="PhysicalSizeX") val[a[1]] = b[2];
       if (a[1]=="PhysicalSizeY") val[a[1]] = b[2];
       if (a[1]=="ID") val[a[1]] = b[2];
   }
   if (maxa<(val["SizeX"]*val["SizeY"])) { 
      maxa=(val["SizeX"]*val["SizeY"]); 
      mpp_x=val["PhysicalSizeX"];
      mpp_y=val["PhysicalSizeY"];
      split(val["ID"],c,":");
      id=c[2]
   }
}
END { print id","mpp_x","mpp_y; }
		
