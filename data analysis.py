#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#nous allaons nous baser sur les données mensuelles de vente de societé de smartphones et gadgets:

# question
#1 quel est le mois durant lequel nous avons réaliser le plus de chiffres d'affaires
#2 dans quel ville nous avons enregistré un maximum de commandes?
#3 en quelle moment doit on faire une campagne publicitaire pour avoir plus de ventes?
#4 quel produit se vend le plus? et pourquoi?
#5 quel est les combinaisons de produit qui se vendent le plus?


# In[40]:


#1 découverte des données

# imporer les packages 
import os
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


# In[41]:


# collecter les noms des fichiers (datasets)
files=[file for file in os.listdir(r'C:\Users\E682\Desktop\Projects\python\projet en data analysis_comment analyser les ventes de votre entreprise\Sales_Data')]
for file in files:
    print(file)


# In[42]:


path = r'C:\Users\E682\Desktop\Projects\python\projet en data analysis_comment analyser les ventes de votre entreprise\Sales_Data'

# creer une base de données vide
all_data=pd.DataFrame()

for file in files:
    current_data=pd.read_csv(path+'/'+file)
    all_data=pd.concat([all_data,current_data])
print(all_data)


# In[43]:


#exple afficher mois de janvier
donnee_janvier=pd.read_csv(path+'/Sales_January_2019.csv')
donnee_janvier.shape


# In[44]:


#mettre les donné dans un seul fichier
all_data.to_csv(path+'/all_data.csv', index=False)


# In[45]:


#explorer la base de donneé : les types
all_data.dtypes


# In[46]:


all_data.head()


# In[47]:


#les valeur manquantes
all_data.isnull().sum()


# In[48]:


# supprimer les valeur manquantes
all_data=all_data.dropna(how='all')
all_data.shape


# In[49]:


#2 quel est le mois durant lequel nous avons réaliser 

def month(x):
    return x.split('/')[0]
#month('12/30/19 00:01') pr teser notre code


# In[50]:


#appliquer la fonction sur notre colonne order en ajoutant la colonne Monthl
all_data['Month']=all_data['Order Date'].apply(month)
all_data


# In[51]:


#afficher les valeur unique de colonne Month
all_data['Month'].unique()


# In[52]:


all_data=all_data[all_data['Month']!='Order Date']
all_data['Month'].unique()


# In[53]:


all_data.dtypes


# In[54]:


#changer le type
all_data["Month"]=all_data['Month'].astype(int)
all_data.dtypes


# In[55]:


all_data['Price Each']=all_data['Price Each'].astype(float)
all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data.dtypes


# In[56]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data


# In[30]:


all_data.groupby('Month')['Sales'].sum()


# In[57]:


#visualisation des donn
months=range(1,13)
plt.bar(months,all_data.groupby('Month')['Sales'].sum())
plt.xticks(months)
plt.ylabel('Sales in USD')
plt.xlabel('Month number')
plt.show()


# In[58]:


#3 dans quel ville nous avons enregistré un maximum de commandes?

all_data


# In[59]:


#recuperation du 2em element etant separerpr des virgules
'136 Church St, New York City, NY 10001'.split(',')[1]


# In[60]:


# fonction pour recupere le 2eme elemet separer par chacun par des virgulez
def city(x):
  return x.split(',')[1]


# In[62]:


#appliquer la fonction de recuperation de la ville et l'ajouter a un new colonne
all_data['city']=all_data['Purchase Address'].apply(city)
all_data


# In[63]:


#grouper par ville et les compter 
all_data.groupby('city')['city'].count()


# In[64]:


#explemoi pour prendre uniquement les noms
all_data.groupby('city')['city'].count().index


# In[66]:


#explemoi pour prendre uniquement les valeurs
all_data.groupby('city')['city'].count().values


# In[68]:


plt.bar(all_data.groupby('city')['city'].count().index,all_data.groupby('city')['city'].count().values)
plt.xticks(rotation='vertical')
plt.ylabel('Received orders')
plt.xlabel('City name')
plt.show()


# In[71]:


#4 en quelle moment doit on faire une campagne publicitaire pour avoir plus de ventes?

   #new colonne et transformar la colonne order d en donnée temporelle puis extrait l'heure
all_data['Hour']=pd.to_datetime(all_data['Order Date']).dt.hour


# In[80]:


all_data


# In[73]:


keys=[]
hours=[]
for key,hour in all_data.groupby('Hour'):
    keys.append(key)
    hours.append(len(hour))
hours


# In[75]:


#moimeme
all_data.groupby('Hour')['Hour'].count()


# In[77]:


plt.grid
plt.plot(keys,hours)
plt.xlabel('heure de la journée')
plt.ylabel('nombre de commande')


# In[ ]:


# reponse4: entre 10h et 19h


# In[78]:


#5 quel produit se vend le plus? et pourquoi

  #explemoi grouper le produit en fonction de la quantité
all_data.groupby('Product')['Quantity Ordered'].sum()


# In[79]:


#visualiser le groupement des produit en fonction des quantité
all_data.groupby('Product')['Quantity Ordered'].sum().plot(kind='bar')


# In[81]:


# pourquoi le produit se vend le plus

  #grouper le produit en fonction de la moyenne du prix 
all_data.groupby('Product')['Price Each'].mean()


# In[82]:


#creation des variable pour visualisation des produit les plus vendu et la moyenne des prix en bleu
products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
prices=all_data.groupby('Product')['Price Each'].mean()


# In[83]:


#visualisation des produit les plus vendu et la moyenne des prix en bleu
plt.figure(figsize=(40,24))
fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity,color='g')
ax2.plot(products,prices,'b-')
ax1.set_xticklabels(products,rotation='vertical',size=8)


# In[ ]:


# reponse5: les produit les plus moins chere(prix moyenne en bleu) sont celle qui se vend le plus(quantité de product vendu vert)
# AAA Batteries (4-pack) se vend plus et son prix est 2.99


# In[86]:


#6 quelles sont les combinaisons de produit qui se vendent le plus?
 
    #colonne order id=client et ne pas spprimer les elements dupliquer 
df=all_data[all_data['Order ID'].duplicated(keep=False)] 


# In[87]:


#groupement du client en fonction des produit et transformer les produit pour les grouper et join pour ajouter les produit les de la meme commande separer par des virgules
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))


# In[88]:


df


# In[89]:


#afficher tout les produit grouper
df["Grouped"]


# In[90]:


#suppriper les ORder ID(client) dupliquer
df2=df.drop_duplicates(subset=['Order ID'])
df2


# In[91]:


#explemoi les combinaison qui sont tres acheter
df2['Grouped'].value_counts()


# In[92]:


#explemoi les 5 premeire combinaison les plus acheter
df2['Grouped'].value_counts()[0:5]


# In[93]:


#visualiser sous forme d'un diagramme sectoriel les 5 premiere combinaison le plus acheter
df2['Grouped'].value_counts()[0:5].plot.pie()


# In[ ]:


#reponse6: visualiser sous forme d'un diagramme sectoriel les 5 premiere combinaison le plus acheter
#on peut le preparer sous forme de rapport et le presenter a notre client donc les diagrammes avec des commentaire

