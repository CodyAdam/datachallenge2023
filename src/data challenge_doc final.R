#base de données
{
library (httr)  
library(stargazer)
library(corrplot)
library(sampling)
library(readr)
library(data.table)
library(insee)
library(dplyr)
library(rio)
library(openxlsx)
library(data.table)
  library(readxl)
}
#

#import des données
tra <- read_xlsx("trajets.xlsx")
colnames(tra) <- cbind("nom_commune", "destination", "durée")
tra <- tra[tra$durée != 0,] #ville A vers ville A

url <- "https://raw.githubusercontent.com/rennesdatascience/datachallenge2023/main/data/sujet-1/communes_bre.csv"
response <- GET(url)
com <- fread(url)
com <- cbind(com$`Geo Point`,com$`Code Officiel Commune`,com$`Nom Officiel Commune Majuscule`)
com <- data.frame(com)
colnames(com) <- cbind("geopoint", "insee_commune","nom_commune")

int <- read_xlsx("interventions.xlsx")
colnames(int) <- cbind("insee_commune", "activ_client", "activ_reseau")


pop_Bzh <- read_delim("~/Desktop/Master ief /M2/Data challenge/pop Bzh.csv", 
                      delim = ";", escape_double = FALSE, col_names = FALSE, 
                      trim_ws = TRUE)

pop_Bzh <- pop_Bzh[-1:-3,]
n <- pop_Bzh[1,]
pop_Bzh <- pop_Bzh[-1,]
colnames(pop_Bzh) <- n
#pondérer les valeurs qualitatives de nos activités

int$activ_client[int$activ_client=="Très Bas"] <- 1
int$activ_client[int$activ_client=="Bas"] <- 1.1
int$activ_client[int$activ_client=="Moyen"] <- 1.2
int$activ_client[int$activ_client=="Haut"] <- 1.3
int$activ_client[int$activ_client=="Très Haut"] <- 1.4

int$activ_reseau[int$activ_reseau=="Très Bas"] <- 1 
int$activ_reseau[int$activ_reseau=="Bas"] <- 1.1
int$activ_reseau[int$activ_reseau=="Moyen"] <- 1.2
int$activ_reseau[int$activ_reseau=="Haut"] <- 1.3
int$activ_reseau[int$activ_reseau=="Très Haut"] <- 1.4

int$activ_client <- as.numeric(int$activ_client)
int$activ_reseau <- as.numeric(int$activ_reseau)
# crér un fichier satisfaction clients selon là où ils agissent
#créer un fichier satisfaction employés selon le site sur lequels ils sont implantés
set.seed(123)

# client
sat_clt <- data.frame(x = sample(1:5, 1207, replace = TRUE))
nbe_clt <- data.frame(x = sample(0:10, 1207, replace = TRUE))
sat_tot <- (sat_clt*nbe_clt)
sat_ville <- rep(com$nom_commune,length.out =  1207)

df_clt <- cbind(sat_ville, sat_clt, nbe_clt, sat_tot); colnames(df_clt) <- cbind("ville", "sat_clt","nbe_clt", "sat_tot")
df_clt <- df_clt[df_clt$nbe_clt != 0,]
#write.xlsx(df_clt, "df_clt.xlsx")

# employé - 50 sites
sat_emp <- data.frame(x = sample(1:5, 50, replace = TRUE))
nbe_emp <- data.frame(x = sample(5:25, 50, replace = TRUE))
sat_tot <- (sat_emp*nbe_emp)
sat_ville <- rep(com$nom_commune, length.out =  50)

df_emp <- cbind(sat_ville, sat_emp, nbe_emp, sat_tot); colnames(df_emp) <- cbind("ville", "sat_emp","nbe_emp", "sat_tot")
#write.xlsx(df_emp, "df_emp.xlsx")


#       corrélation entre l'activité et la population


pop <- data.frame(as.numeric(pop_Bzh$`Population municipale (historique depuis 1876) 2019`))
cor(int$activ_client,pop)
#                                             0.1208799
cor(int$activ_reseau,pop)
#                                             0.1410923
###       POUR LES VILLES DE MOINS DE 300000
# pour l'activité client
population <- data.frame(pop[pop < 30000,])
#Code qui efface les ville de moins de 30000 hab
activ_client <- int$activ_client[-247]
activ_client <- activ_client[-364]
activ_client <- activ_client[-556]
activ_client <- activ_client[-842]
activ_client <- activ_client[-888]
activ_client <- activ_client[-1067]
activ_client <- activ_client[-1197]
activ_client <- data.frame(activ_client)

cor(activ_client,population)
#   act_cli           0.235363
#pour le résaeu
activ_reseau <- int$activ_reseau[-247]
activ_reseau <- activ_reseau[-364]
activ_reseau <- activ_reseau[-556]
activ_reseau <- activ_reseau[-842]
activ_reseau <- activ_reseau[-888]
activ_reseau <- activ_reseau[-1067]
activ_reseau <- activ_reseau[-1197]
activ_reseau <- data.frame(activ_reseau)

cor(activ_reseau,population)
#   act_res          0.2134983

# POur les villes de moind de 2000 hab
population2 <-data.frame(int$insee_commune,pop_Bzh$Code,pop_Bzh$`Population municipale (historique depuis 1876) 2019`,int$activ_client,int$activ_reseau)
population2$pop_Bzh <- as.numeric(pop_Bzh$`Population municipale (historique depuis 1876) 2019`)
population2 <- population2[,-1:-3]

population2 <- data.frame(population2[population2$pop_Bzh < 2000,])



cor(population2$int.activ_client,population2$pop_Bzh)
#                                                       0.2695472
plot(population2$pop_Bzh,population2$int.activ_client,  pch = 19, col = "lightblue") +
  abline(lm(population2$pop_Bzh~population2$int.activ_client), col = "red", lwd = 3)
cor.test(population2$pop_Bzh,population2$int.activ_client) #0,270

cor(population2$int.activ_reseau,population2$pop_Bzh)
#                                                       0.2242377
plot(population2$pop_Bzh,population2$int.activ_reseau,  pch = 19, col = "lightblue") +
  abline(lm(population2$pop_Bzh~population2$int.activ_reseau), col = "red", lwd = 3)
cor.test(population2$pop_Bzh,population2$int.activ_reseau) #0,224

