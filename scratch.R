options(scipen=999)

stars = read.csv("hygdata_v3.csv", na.strings=c("","NA"))
visible = stars[which(stars$mag < 6.34),]

write.csv(visible[,c("id","dist","x","y","z","ra","dec","mag","ci","con","lum","proper")],file="stars_trim.csv",col.names=FALSE,row.names=FALSE)

sum(is.na(visible$proper))