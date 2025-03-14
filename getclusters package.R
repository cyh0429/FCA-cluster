getClusters <- function(obj = NULL,...){
  # check datatype
  cls <- class(obj)
  
  if(cls == "cell_data_set"){
    extra_params <- list(cds_obj = obj,assays = "counts",...)
    exp <- do.call(pre_pseudotime_matrix,extra_params)
  }else if(cls %in% c("matrix","data.frame")){
    exp <- obj
  }
  
  factoextra::fviz_nbclust(exp, stats::kmeans, method = "wss") +
    ggplot2::labs(subtitle = "Elbow method")
}