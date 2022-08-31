import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")   ### Configuration de taille affichage dans la page 

st.title('Data Vizualisation')

# définir NA values
na_values = [r'\N','NAN','Nan','""']
# predefinir la taille des graphiques
plt.rcParams["figure.figsize"] = (12,6)

#import du fichier ####changer l'url
df_main = pd.read_csv("https://raw.githubusercontent.com/SebastienTarres/Project/main/out.csv", header=0, sep=",", low_memory=False, na_values= na_values)

# rajouts de colonnes nécessaires pour les stats:
df_main['Année_de_sortie'] = pd.to_datetime(df_main['Année_de_sortie'], format='%Y')
df_main['Année'] = df_main['Année_de_sortie'].dt.year
df_main['Decade'] = df_main['Année_de_sortie'].apply(lambda x: (x.year//10)*10)
df_main['Note_moyenne_arrondie'] = df_main['Note_moyenne'].astype(int)

df_main['Liste_acteurs_et_actrices']=df_main['Liste_acteurs_et_actrices'].apply(lambda list1: str(list1).replace('[','').replace(']',''))
df_main[['Actor_1', 'Actor_2', 'Actor_3', 'Actor_4','Actor_5','Actor_6','Actor_7','Actor_8','Actor_9','Actor_10']] = df_main['Liste_acteurs_et_actrices'].str.split(',', expand=True)

st.write("Cette page présente une sélection de visualisation de données que nous avons réalisé au cours du projet.")

col1, col2 = st.columns(2)

with col1:
	##GRAPH 1: Top 10 directeur le plus productifs
	df_director = df_main['Directeur'].value_counts().to_frame()
	df_director.drop('Inconnu', axis=0, inplace=True)
	df_director = df_director.reset_index()
	df_director = df_director.rename(columns={'Directeur': 'nombre_de_films', 'index':'directeur'})
	df_director_head = df_director.head(10)

	st.header("Top 10 des directeurs les plus productifs")

	barplotDirector = sns.barplot(data=df_director_head, x='directeur', y='nombre_de_films', color='darkcyan')
	#plt.title('Top 10 des directeurs les plus productifs')
	plt.xlabel("Directeur")
	plt.ylabel("Nombre de films")
	plt.xticks(rotation=45)
	st.pyplot(barplotDirector.figure, clear_figure=True)

	st.write("text")


with col2:
	##GRAPH 2: repartitions films par genre
	columns_genres_list = ['Action',
	       'Aventure', 'Animation', 'Biographie', 'Comédie', 'Crime', 'Drame',
	       'Famille', 'Romance', 'Thriller', 'Guerre', 'Western', 'Histoire']
	len(columns_genres_list)

	columns_genreCount_list = []
	for i in columns_genres_list:
	    columns_genreCount_list.append(df_main[i].sum())
	df_genres_count = pd.DataFrame(columns_genreCount_list)
	df_genres_count['Genres'] = columns_genres_list
	df_genres_count.rename(columns = {0:'Nombre_de_films'},inplace=True)
	df_genres_count = df_genres_count.sort_values(by='Nombre_de_films', ascending=False)

	st.header("Nombre de films produits par genre")

	barplotFilmGenre = sns.barplot(data=df_genres_count, x='Genres', y='Nombre_de_films', color='darkcyan')
	plt.ylabel("Nombre de films")
	#plt.title('Nombre de films produits par genre')
	st.pyplot(barplotFilmGenre.figure, clear_figure=True)

	st.write("Les films comportent majoritairement des films de type Drame ou Comédie. Le choix des films proposés est le fruit de recherche sur la zone du Client fictif du département de la 'Creuse', qui se compose d'une population plutôt familiale. ")

# GRAPH 4:les top 10 de tous les films le plus vus et le mieux notés
st.header("Le top 10 des films les mieux notés")
st.write("Ce tableau nous présente les 10 films les mieux notés de notre base ainsi que le nombre de votes")
top_10_tot = df_main.sort_values(by=['Nombre_de_votes'], ascending=False)
top_note = top_10_tot.head(10)
top_note["Nombre de votes"] = top_note["Nombre_de_votes"].astype('Int64')
top_note["Note"] = top_note["Note_moyenne"].astype('float').round(1)
top = top_note[['Titre', 'Nombre de votes', 'Note']]
#st.dataframe(top)
# Styled
st.dataframe(top.style.format({'Note': '{:.1f}'}))

##GRAPH 3: Répartition par nombre de vote
# comptage de tous les films en fonction de la moyenne arrondie de votes (la repartition par genre reflète la tendance générale)
df_round_average = df_main["Note_moyenne_arrondie"].value_counts()
df_round_average = df_round_average.to_frame()
df_round_average.reset_index(inplace=True)
df_round_average.rename(columns={'index' : 'Moyenne', 'Note_moyenne_arrondie':'Nombre_de_votes'}, inplace=True)

st.header("Répartition par nombre de votes")

barplotVote = sns.barplot(data=df_round_average, x="Moyenne", y='Nombre_de_votes', color='darkcyan')
plt.ylabel('Nombre de films')
#plt.title('Répartition par nombre de votes')
st.pyplot(barplotVote.figure, clear_figure=True)

st.write("Une grosse partie des films sont au-dessus de la moyenne, la base de films sélectionnée est bien notée")


col1, col2 = st.columns(2)

with col1:
	# GRAPH 5: Evolution du nombre de films produits dans le temps'
	st.header("Nombre de films par année de sortie")
	fig=plt.figure(figsize=(10,5))
	ax1 = fig.add_subplot(111)
	#ax2 = ax1.twinx()
	sns.histplot(data=df_main, x='Année', stat="count", color='darkcyan', bins=35, ax=ax1)
	ax1.set_ylabel('Nombre de films')
	#plt.title('Evolution du nombre de films produits dans le temps')
	plt.xticks(rotation=60)
	st.pyplot(fig)

	st.write("text")

with col2:
	# GRAPH 6: évolution de la durée des films dans le temps
	st.header("Evolution de la durée des films")
	df = df_main
	plt.figure(figsize = (15,8))
	sns.lineplot(x = 'Année_de_sortie', y = 'Durée_en_minutes',data = df, color='darkcyan', ci=None, linewidth=3)
	plt.xlabel('Année')
	plt.ylabel('Durée')
	#plt.title('Durée des films')
	st.set_option('deprecation.showPyplotGlobalUse', False)
	st.pyplot()

	st.write("On constate que la durée des films c'est rallongé depuis les 1er sortie cinéma, la durée est passé de 80 min en moyenne à 120 min aujourd'hui !")

# GRAPH 7: Evolution du nombre de film par genre
# repartition des films par genre et par année
df_year_genre = df_main.groupby(by='Année').sum()
df_year_genre.drop(columns=['Nombre_acteurs_et_actrices','Durée_en_minutes','Note_moyenne','Nombre_de_votes'], inplace=True)

st.header("Evolution de la production de films des 3 genres les plus representés")
plt.figure(figsize = (15,8))
sns.lineplot(x = 'Année', y = 'Drame',data = df_year_genre, label = 'drame', linewidth=5)
sns.lineplot(x = 'Année', y = 'Comédie', data = df_year_genre,label = 'comédie', linewidth=5)
sns.lineplot(x = 'Année', y = 'Crime',data = df_year_genre, label = 'crime', linewidth=5)
plt.xlabel('Année')
plt.ylabel('Nombre de films')
plt.legend()
#plt.title('Evolution du nombre de film par genre')
st.pyplot()

st.write("On peut observer une nette augmentation de ces 3 genres, surtout ces dernières années.")


