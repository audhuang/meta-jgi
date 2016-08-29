#########################################################
### A) Installing and loading required packages
#########################################################

if (!require("gplots")) {
   install.packages("gplots", dependencies = TRUE)
   library(gplots)
   }
if (!require("RColorBrewer")) {
   install.packages("RColorBrewer", dependencies = TRUE)
   library(RColorBrewer)
   }

#########################################################
### B) Reading in data and transform it into matrix format
#########################################################

data <- read.csv("data", comment.char="#")
rnames <- data[,1]                            # assign labels in column 1 to "rnames"
mat_data <- data.matrix(data[,2:ncol(data)])  # transform column 2-5 into a matrix
rownames(mat_data) <- rnames                  # assign row names 

#########################################################
### C) Customizing and plotting the heat map
#########################################################

# creates a own color palette with costumized "color gradient" for the 10 different size bins.

#my_palette <- colorRampPalette(c("white", "yellow" ,"green","grey","black","purple","cyan","magenta","blue","brown","pink"))
my_palette <- colorRampPalette(c("grey","#FCB6D3","#ED9FB9","#DF889F","#D17185","#C35B6C","#B44452","#A62D38","#98161E","#8A0005","black"))#"#D21E45","#BD143E","#A81837","#931439","#7E1229","#690F22","#540C1B","#3F0914","#2A060D","black"))

####
# Set up the breaks
####
col_breaks = c(seq(0,0.1,by=0.01))

################################################
# Set up and initiate the saved image (resolution, proportions and size)
################################################

################################################
# creates a 5 x 10 inch image
################################################
png("hm.png",    # create PNG for the heat map        
  width = 5*500,        # 5 x 300 pixels
  height = 8*600,
  res = 600,            # 300 pixels per inch
  pointsize = 6)        # smaller font size


################################################
#set up the layout and sizes of the heatmap - components and their sizes)
################################################
#lmat = rbind(c(0,3),c(2,1),c(0,4))
#mylayout = rbind(c(0,3),c(2,1),c(0,4))
mylhei = c(0.7,8)
mylwid = c(1.5,4)
#mylmat = rbind(c(2,1),c(4,3))
#mymat   = rbind(1:2,3:4)

################################################
#determine distance: http://svitsrv25.epfl.ch/R-doc/library/amap/html/dist.html
################################################
dist.pear  <- function(x) as.dist(1-cor(t(x),method = "pearson"))
dist.ken   <- function(x) as.dist(1-cor(t(x),method = "kendall"))
dist.spear <- function(x) as.dist(1-cor(t(x),method = "spearman"))
#dist.spear <- function(x) as.dist(x,method = "spearman")

################################################
# Create the Heatmap!
################################################
heatmap.2(mat_data,
  #main = "Frequency of Nitroreductases in metagenomic surveys", # heat map title
  key=TRUE,
  key.xlab="No NTRs in survey",
  #symkey = (title = "No NTRs in survey"),
  density.info="none",                                          # turns off density plot inside color legend
  trace="none",                                                 # turns off trace lines inside the heat map
  margins =c(12,9),                                             # widens margins around plot
  col=my_palette,                                               # use on color palette defined earlier 
  dendrogram="both",                                            # dendrogram for both, can be "none"/"row"/"column"
  breaks=col_breaks,                                            # column breaks as defined - the bins
  #labRow=NA,				                        #disable row labels
  scale='none',                                                 #disable any scaling
  lhei=mylhei,
  lwid=mylwid,
  #mat=mymat,

  #distfun=dist.pear,
  #distfun=dist.ken,
  distfun=dist.spear,                                           #set up clustering method

  hclustfun = function(x) hclust(x,method = 'complete'),        #hierarchical clustering methods (http://www.inside-r.org/r-doc/stats/hclust) 

  #hclustfun = function(x) hclust(x,method = 'complete'),        #hierarchical clustering methods (http://www.inside-r.org/r-doc/stats/hclust) 
  	      		  		                        #NO: single,average,centroid  Maybe: ward.D, complete,mcquitty,median
  ###hclustfun = function(x) hclust(as.dist(1-cor(t(x), method="spearman")),method="complete"),
                                                                # side colors

RowSideColors = c(
  rep("blue",1),
  rep("blue",1), 
  rep('brown', 1),
  rep("brown",1)
#   rep("brown",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("cyan",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("blue",1),
#   rep("pink",1),
#   rep("cyan",1),
#   rep("pink",1),
#   rep("cyan",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("magenta",1),
#   rep("cyan",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("brown",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("pink",1),
#   rep("pink",1),
#   rep("blue",1),
#   rep("blue",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("magenta",1),
#   rep("pink",1),
#   rep("pink",1),
#   rep("pink",1),
#   rep("magenta",1),
#   rep("brown",1),
#   rep("cyan",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("cyan",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("magenta",1),
#   rep("pink",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("blue",1),
#   rep("cyan",1),
#   rep("cyan",1),
#   rep("blue",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("cyan",1),
#   rep("blue",1),
#   rep("brown",1),
#   rep("brown",1),
#   rep("magenta",1),
#   rep("blue",1),
#   rep("magenta",1)
),

  colsep=1:ncol(mat_data),#0:20,
  rowsep=1:nrow(mat_data),#0:236,
  sepcolor="white",
  sepwidth=c(0.001,0.001),


  Colv=TRUE)                                        # turn on column clustering (="NA" to disable)

#par(lend = 1)           # square line ends for the color legend
#legend("center",      # location of the legend on the heatmap
#    #inset=.5,
#    title = "survey origin",
#    legend = c("gut", "soil","freshwater","ocean","sludge","?","plant","reactor","sediment","waste_water"), # category labels
#    col = c("green", "brown", "cyan","blue","red","gray","yellow","pink","purple","magenta"),  # color key
#    lty= 1,             # line style
#    lwd = 10,            # line width
#    #horiz=TRUE,
#    #x.intersp=0.5,
#    #text.width=c(0,0,0,0,0,0)


dev.off()                                           # close the PNG device
