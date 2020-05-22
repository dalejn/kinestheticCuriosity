path = "data/subjectLevel/"
outpath = "/data/kFolds/"
file.names <- dir(path, pattern=".csv")
for (file in file.names){
  data = read.csv(paste(path,file,sep=""), header=TRUE)
  
  k1 = data.frame()
  k2 = data.frame()
  k3 = data.frame()
  
  for (day in unique(data$Day)[c(TRUE,FALSE,FALSE)]){
    slice <-data[which(data$Day==day),]
    k1 <- rbind(k1, slice)
  }
  
  for (day in unique(data$Day)[c(FALSE,TRUE,FALSE)]){
    slice <-data[which(data$Day==day),]
    k2 <- rbind(k2, slice)
  }
  
  for (day in unique(data$Day)[c(FALSE,FALSE,TRUE)]){
    slice <-data[which(data$Day==day),]
    k3 <- rbind(k3, slice)
  }
    
  fold1_Train <- rbind(k2,k3)
  fold1_Test <- k1

  fold2_Train <- rbind(k1,k3)
  fold2_Test <- k2
  
  fold3_Train <- rbind(k1,k2)
  fold3_Test <- k3

  subjectName <- substr(file,1,nchar(file)-4)
  
  x <- fold1_Train$Node
  levels(x) <- 1:length(levels(x))
  fold1_Train$Node <- as.numeric(x)
  
  x <- fold1_Test$Node
  levels(x) <- 1:length(levels(x))
  fold1_Test$Node <- as.numeric(x)
  
  x <- fold2_Train$Node
  levels(x) <- 1:length(levels(x))
  fold2_Train$Node <- as.numeric(x)
  
  x <- fold2_Test$Node
  levels(x) <- 1:length(levels(x))
  fold2_Test$Node <- as.numeric(x)
  
  x <- fold3_Train$Node
  levels(x) <- 1:length(levels(x))
  fold3_Train$Node <- as.numeric(x)
  
  x <- fold3_Test$Node
  levels(x) <- 1:length(levels(x))
  fold3_Test$Node <- as.numeric(x)
  
  write.table(fold1_Train[2], paste(outpath,subjectName,"_fold1_Train.txt", sep=""), row.names=FALSE, col.names=FALSE)
  write.table(fold1_Test[2], paste(outpath,subjectName,"_fold1_Test.txt",sep=""), row.names=FALSE,col.names=FALSE)
  
  write.table(fold2_Train[2], paste(outpath,subjectName,"_fold2_Train.txt", sep=""), row.names=FALSE,col.names=FALSE)
  write.table(fold2_Test[2], paste(outpath,subjectName,"_fold2_Test.txt",sep=""), row.names=FALSE,col.names=FALSE)
  
  write.table(fold3_Train[2], paste(outpath,subjectName,"_fold3_Train.txt", sep=""), row.names=FALSE,col.names=FALSE)
  write.table(fold3_Test[2], paste(outpath,subjectName,"_fold3_Test.txt",sep=""), row.names=FALSE, col.names=FALSE)
}