library(readxl)
library(xlsx)

df<-read_excel(path = paste('D:\\Computer Science\\Projects\\',
                            'Evalueserve 2019\\Machine Learning\\',
                            'k-means clustering.xlsx', sep = ''))

#checking missing values
View(as.data.frame(sapply(df, function(x)sum(is.na(x)))))

#mean imputation
m<-mean(df$`Fees (in Lakh)`,na.rm = T)
i<-which(is.na(df$`Fees (in Lakh)`))
df$`Fees (in Lakh)`[i]<-m

#model imputation

library(magrittr)
library(dplyr)


df %>%
  group_by(`Duration(in Months)`) %>%
  summarise(count=n())


i<-which.max(table(df$`Duration(in Months)`))[[1]]
d<-as.data.frame(table(df$`Duration(in Months)`))
x<-d$Var1[i]

df$`Duration(in Months)`[which(is.na(df$`Duration(in Months)`))] <- x

#since 24 has got the highest occurence, we will
#impute with 24.

str(df)

df2<-df

df2$IELTS_Score[is.na(df2$IELTS_Score)]<-0

str(df)
df$`Duration(in Months)`<-as.factor(df$`Duration(in Months)`)


df2$Master<-as.factor(df2$Master)
df2$Bachelor<-as.factor(df2$Bachelor)
df2$`Diploma/Certification`<-as.factor(df2$`Diploma/Certification`)
df2$Doctorate<-as.factor(df2$Doctorate)
df2$Science<-as.factor(df2$Science)
df2$Arts<-as.factor(df2$Arts)
df2$Commerce<-as.factor(df2$Commerce)
df2$`Engineering Degree`<-as.factor(df2$`Engineering Degree`)
df2$`Medical Degree`<-as.factor(df2$`Medical Degree`)
df2$MBA<-as.factor(df2$MBA)
df2$IELTS_flag<-as.factor(df2$IELTS_flag)
df2$TOEFL_flag<-as.factor(df2$TOEFL_flag)
df2$GMAT_flag<-as.factor(df2$GMAT_flag)
df2$GRE_flag<-as.factor(df2$GRE_flag)
df2$IELTS_Score <- as.factor(df2$IELTS_Score)
df2$TOEFL_Score <- as.factor(df2$TOEFL_Score)
df2$GMAT_Score <- as.factor(df2$GMAT_Score)
df2$GRE_Score <- as.factor(df2$GRE_Score)
str(df2)

#converting variables into logical form

df2$Master<-ifelse(df2$Master == "Yes",1,0)
df2$Bachelor<-ifelse(df2$Bachelor == "Yes",1,0)
df2$`Diploma/Certification`<-ifelse(df2$`Diploma/Certification` == "Yes",1,0)
df2$Doctorate<-ifelse(df2$Doctorate == "Yes",1,0)

df2$Science<-ifelse(df2$Science == "Yes",1,0)
df2$Arts<-ifelse(df2$Arts == "Yes",1,0)
df2$Commerce<-ifelse(df2$Commerce == "Yes",1,0)
df2$`Engineering Degree`<-ifelse(df2$`Engineering Degree` == "Yes",1,0)
df2$`Medical Degree`<-ifelse(df2$`Medical Degree` == "Yes",1,0)
df2$MBA<-ifelse(df2$MBA == "Yes",1,0)
df2$IELTS_flag<-ifelse(df2$IELTS_flag == "Yes",1,0)
df2$TOEFL_flag<-ifelse(df2$TOEFL_flag == "Yes",1,0)
df2$GMAT_flag<-ifelse(df2$GMAT_flag == "Yes",1,0)
df2$GRE_flag<-ifelse(df2$GRE_flag== "Yes",1,0)
#changing factors into numeric

df2$`Duration(in Months)`<-as.numeric(df2$`Duration(in Months)`)
df2$IELTS_Score<-as.numeric(df2$IELTS_Score)
df2$TOEFL_Score<-as.numeric(df2$TOEFL_Score)
df2$GMAT_Score<-as.numeric(df2$GMAT_Score)
df2$GRE_Score<-as.numeric(df2$GRE_Score)
str(df2)
#dummy encoding 
#model.matrix()

df3<-df2

kmeans(x=df3,centers = 3,nstart =50)

# We need to put these variables into numeric form by dummy encoding:
df3$University_Name<-NULL
df3$Course_name<-NULL



#Clustering
km.out<-kmeans(x=df3,centers=3,nstart = 50)

km.out$cluster

df4$Cluster<-km.out$cluster
df$Cluster<-km.out$cluster

write.csv(x = df,row.names = F,file = "C:\\Users\\tilak\\Desktop\\regex\\clustering\\output_main3.csv")


#clustering2
# Total within sum of squares
wss<-0

for(i in 1:11){
  
  km.out<-kmeans(x=df3,centers=i,nstart = 10)
  wss[i - 1]<-km.out$tot.withinss
  
}
str(df2)
write.csv(x = df,row.names = V,file = "C:\\Users\\tilak\\Desktop\\regex\\clustering\\output_main2.csv")
write.xlsx2(x = df3, row.names = F, 
file = paste('D:\\Computer Science\\Projects\\Evalueserve 2019\\', 
             'Machine Learning\\k-means clustering output.xlsx', sep = ''))
plot(1:10,wss)

str(wss)
#
#dummy encoding
#clustersplot
#fee normalization




