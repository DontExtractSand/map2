import streamlit as st
import pandas as pd
import urllib.parse

# Display title and description of the app
st.title("Pour ne pas bâillonner l'ensemble des organisations environnementales financées par des dons...")
st.write("""
Cette application vous aide à trouver les coordonnées complètes de votre député puis vous permet de l'appeler à prendre position contre les amendements bâillon qui pourraient revenir dans le projet de loi de finance 2025. En effet, les amendements en lien ci-dessous ont pour l'instant été refusés mais pourraient revenir en séance pleinière.
Si vous avez besoin d'aide pour trouver votre circonscription, vous pouvez utiliser cette carte :
""")
st.page_link("https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE", label="https://www2.assemblee-nationale.fr/recherche-localisee/carte/FRANCE")
st.page_link("https://www.assemblee-nationale.fr/dyn/17/amendements/0324A/CION_FIN/CF685", label="Amendement CF685")
st.page_link("https://www.assemblee-nationale.fr/dyn/17/amendements/0324A/CION_FIN/CF686", label="Amendement CF686")
st.page_link("https://www.assemblee-nationale.fr/dyn/17/amendements/0324A/CION_FIN/CF477", label="Amendement CF477")

# Function to load the CSV file from GitHub
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/DontExtractSand/map/refs/heads/main/deputes-active.csv"
    data = pd.read_csv(url)
    return data

# Load the data from the GitHub repository
df = load_data()

if df is not None:
    # Extract and sort unique values for departementCode and circo
    departement_codes = sorted(df['departementCode'].unique())  # Sort numerically or alphabetically
    circo_values = sorted(df['circo'].unique())  # Sort numerically or alphabetically

    # Dropdowns for user input
    departement = st.selectbox("Choisissez votre département", departement_codes)
    circonscription = st.selectbox("Choisissez votre circonscription", circo_values)

    # Button to submit the selection
    if st.button("Soumettre"):
        # Find the matching row
        matching_row = df[(df['departementCode'] == departement) & (df['circo'] == circonscription)]

        # Display results
        if not matching_row.empty:
            st.write("Voici les coordonnées du député correspondant (**vérifiez son groupe politique et la pertinence de l'interpeler avant envoi**) :")
            st.write(matching_row)

            # Extract the Twitter handle from the matching row
            twitter_handle = matching_row['twitter'].values[0]
            facebook_handle = matching_row['facebook'].values[0]
            email_address = matching_row['mail'].values[0]
            first_name = matching_row['prenom'].values[0]
            last_name = matching_row['nom'].values[0]
            civ = matching_row['civ'].values[0]
            permanence = matching_row['permanence'].values[0]
            groupe = matching_row['groupe'].values[0]

            ### Twitter Message ###
            st.header("**Solution 1 : interpeler votre député sur X/Twitter** avec le message suivant :")
            if pd.notna(twitter_handle) and twitter_handle != '':
                # Build the tweet message
                tweet_message = f"{twitter_handle} Message à écrire... Positionnez-vous contre ces amendements bâillon."

                # URL encode the tweet message to handle special characters
                encoded_tweet_message = urllib.parse.quote(tweet_message)

                # Generate the Twitter URL
                twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet_message}"

                # Display the link to tweet
                st.write(f"Votre tweet : {tweet_message}")
                st.markdown(f"[Cliquer ici pour twitter ce message]({twitter_url})")
            else:
                st.write("Ce député n'a pas de compte Twitter connu dans notre base.")
            
            ### Facebook Message ###
            st.header("**Solution 2 : interpeler votre député sur Facebook** avec le message suivant :")
            if pd.notna(facebook_handle) and facebook_handle != '':
                # Build the Facebook message
                facebook_message = f"""
                Message à écrire... Positionnez-vous contre ces amendements bâillon.
                """

                # URL encode the tweet message to handle special characters
                encoded_facebook_message = urllib.parse.quote(facebook_message)

                # Generate the Facebook share URL
                facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=https://yourwebsite.com&quote={encoded_facebook_message}"

                # Display the link to post on Facebook
                st.write(f"Votre message Facebook : {facebook_message}")
                st.markdown(f"[Cliquer ici pour poster sur Facebook]({facebook_url})")
            else:
                st.write("Ce député n'a pas de compte Facebook connu dans notre base.")

            ### Email Message ###
            st.header("**Solution 3 : écrivez par email à votre député** avec le message suivant :")
            if pd.notna(email_address) and email_address != '':
                # Build the email subject and body
                email_subject = "Titre à écrire... Positionnez-vous contre ces amendements bâillon"
                email_body = f"""
                {civ} {first_name} {last_name}, Message à écrire... Positionnez-vous contre ces amendements bâillon.
                """

                # URL encode the subject and body for the mailto link
                encoded_subject = urllib.parse.quote(email_subject)
                encoded_body = urllib.parse.quote(email_body)

                # Create mailto link
                mailto_link = f"mailto:{email_address}?subject={encoded_subject}&body={encoded_body}"

                # Display the link to send an email
                st.write(f"L'adresse : {email_address}")
                st.write(f"Le sujet du message : {email_subject}")
                st.write(f"Votre email : {email_body}")
                st.markdown(f"[Cliquez ici pour envoyer un email]({mailto_link})")
            else:
                st.write("Ce député n'a pas d'adresse email connue dans notre base.")

            # Postcard text
            if permanence != '' and pd.notna(permanence) :
                address=permanence
            else:
                address="Assemblée nationale - 126 Rue de l'Université, 75355 Paris 07 SP"
            postcard_text = f"""
            {civ} {first_name} {last_name}, Message à écrire... Positionnez-vous contre ces amendements bâillon.
            """

            # Display the postcard preview
            st.header("**Solution 4 : envoyez une lettre à votre député** avec le message suivant :")
            st.write(f"{postcard_text}")

            # Display recipient and address
            st.write(f"**Destinataire** à préciser : {first_name} {last_name}")
            st.write(f"**Addresse** (à défaut de permance connue, l'adresse de l'assemblée est utilisée) : {address}")
        
        else:
            st.write("Nous n'avons pas trouvé de député correspondant.")
else:
    st.write("Erreur : la donnée source n'est pas disponible.")

# Pied de page
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
        Cette application utilise les données de l'opendata de l'assemblée nationale (<a href="https://data.assemblee-nationale.fr/">https://data.assemblee-nationale.fr/</a>) complétées par celles de Vox Public (<a href="https://www.voxpublic.org">https://www.voxpublic.org</a>).<br>
        Si des données sont erronées ou manquantes, n'hésitez pas à nous en faire part sur <a href="mailto:adresse@preciser.org">adresse@preciser.org</a>.<br>
        L'envoi des messages reste de la responsabilité des utilisateurs.trices. Il est donc utile d'adapter, valider les messages au regard du propos souhaité, de chaque contexte personnel et des députés destinataires.
    </div>
    """,
    unsafe_allow_html=True
)
