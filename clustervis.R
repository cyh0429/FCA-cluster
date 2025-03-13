library(Mfuzz)
library(data.table)
library(readxl)
library(ggplot2)
library(RColorBrewer)
library(ggsci)
library(openxlsx)
library(ClusterGVis)
library(Biobase)
library(BiocGenerics)
library(data.table)
library(PerformanceAnalytics)
library(corrplot)
library(openxlsx)
library(data.table)
library(ggplot2)
library(ggpubr)
library(Cairo)

data<-read.table(file='path/study data.csv',header=TRUE,row.names= 1,sep=',')
head(data,3)
data<-data[,c(5:10)]
set.seed(123456)
getClusters(exp = data)
# using mfuzz for clustering
cm <- clusterData(exp = data,
                  cluster.method = "mfuzz",
                  cluster.num = 4)
str(cm)
visCluster(object = cm, 
           plot.type = "line",
           ms.col = c("green","orange","blue"),
           add.mline = T)+
  theme(axis.title = element_text(
    family = 'Times New Roman',
    face='bold', 
    size=15, 
    lineheight = 1),
    axis.text.x = element_text(
      family = 'Times New Roman',
      face="bold", 
      color="black",
      size=12,
      angle = 0),
    axis.text.y = element_text(
      family = 'Times New Roman',
      face="bold", 
      color="black",
      size=12
    ))+
  theme(axis.ticks.length = unit(-0.15,'cm'))
dir.create(path="mfu")
cc<- cm$wide.res
write.csv(cc,paste0("mfu","/mfuzz",".csv"))
library(grid)
visCluster(object = cm,
           plot.type = "both",
           column_names_rot = 0,
           add.box = T,
           add.line = T,
           line.side = "left",
           show_row_dend = F,
           boxcol = ggsci::pal_npg()(8) )            
#kmeans
ck <- clusterData(exp = data,
                  cluster.method = "kmeans",
                  cluster.num = 4)
str(cm)
visCluster(object = ck, 
           plot.type = "line",
           ms.col = c("blue","yellow","red"),
           add.mline = T)+
  theme(axis.title = element_text(
    family = 'Times New Roman',
    face='bold', 
    size=15, 
    lineheight = 1),
    axis.text.x = element_text(
      family = 'Times New Roman',
      face="bold", 
      color="black",
      size=12,
      angle = 0),
    axis.text.y = element_text(
      family = 'Times New Roman',
      face="bold", 
      color="black",
      size=12
    ))+
  theme(axis.ticks.length = unit(-0.15,'cm'))
dev.off()
