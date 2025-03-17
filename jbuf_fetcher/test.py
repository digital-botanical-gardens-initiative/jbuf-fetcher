# projet 1
# celsius = float(input("Combien de dégré °C fait-il ? "))
# fahrenheit = celsius*9/5+32
# print( celsius, "degrés Celsius équivalent à" , fahrenheit, "degrés Fahrenheit")

# projet 2

# note_au_bac = float(input("Quelle est votre note au bac ? "))

# if note_au_bac >= 18:
# print("Félicitations du jury")
# elif 16 <= note_au_bac < 18:
# print("Très bien")
# elif 14 <= note_au_bac < 16:
# print("Bien")
# elif 12 <= note_au_bac < 14:
# print("Assez bien")
# else:
# print("Pas de mention")


# projet 3

"""nb_vie = 7

mot_secret = "tortue"
mot_public = "_" * len(mot_secret)

while nb_vie > 0 and mot_secret != mot_public: #Tant que le nombre de vie est plus grand que 0 et que le mots secret est différent du mot publique
    lettre = input("Ecrivez une lettre : ")

    if lettre in mot_secret:
        for i in range(len(mot_secret)): # i = position dans le mot, dans la taille du mot secret
            if mot_secret[i] == lettre:
                mot_public = mot_public[:i] + lettre + mot_public[i + 1:]
    else:
        nb_vie -= 1

    if mot_public == mot_secret:
        print("Bravo ! Le mot est" , mot_secret )
    elif nb_vie == 0:
        print("Vous avez perdu")
    else:
        print("Vous avez " , nb_vie , "vie(s) restante(s)")
        print( "Le mot est : ", mot_public)"""

# nb_vies = 7

# mot_cache = "leopard"
# mot_public = "_"* len(mot_cache)

# while nb_vies > 0 and mot_cache != mot_public:
# lettre = input("Ecrivez une lettre ")

# if lettre in mot_cache:
# for i in range(len(mot_cache)):
# if mot_cache[i] == lettre:
# mot_public = mot_public[:i] + lettre + mot_public[i+ 1:]
# else:
# nb_vies -=1

# if mot_cache == mot_public:
# print("Bravo vous avez gagner")
# print("Le mot mystère est" , mot_cache)
# elif nb_vies == 0:
# print("Dommage, vous avez perdu")
# else:
# print("Il vous reste" , nb_vies)
# print("Le mot est : " , mot_public)

# fonction

# def ma_fonction(ma_variable=5):
# print("ma variable est" , ma_variable)

# ma_fonction(42)
# ma_fonction()

# def ma_fonction_2(*args):
# print("ma variable 2 est" , args)

# ma_fonction_2(2 , 3 , 4 , 6 , 1 ,)

# def ma_fonction_argument_nomme(**kwargs):
# print("mes arguments sont" , *kwargs )

# ma_fonction_argument_nomme(quatre=4, trois=3, deux=2, un=1)

# def somme(a, b):
# return a + b
# s = somme(4,5)

# print(s)

# def simple_range(n):
# l = []
# i = 0

# while i<n:
# l.append(i)
# i +=1

# return l

# print(simple_range(5))

# nombres = (1, 2, 3, 4, 5)

# print(nombres.index(3))
# print(nombres.count(3))

"""
class Pizza:
    def __init__(self, base, prix, diametre, style, ingredients):
        self.base = base
        self.prix = prix
        self.diametre = diametre
        self. style = style
        self.ingredients = ingredients

    def ajouter_ingredients(self, nouvel_ingredient):
        if nouvel_ingredient == "ananas":
            raise TypeError("Les ananas ne vont pas sur les pizzas")
        self.ingredients.append(nouvel_ingredient)
        self.prix = self.prix + 1

    def servir(self, table):
        print("j'amène la pizza à la table" , table)

    def livraison(self, adresse):
        print("Je livre la pizza à l'adresse", adresse)

base = input("Quelle base voulez-vous ? (tomate/blanche)")
taille = input ("Quelle taille voulez-vous ? (moyenne/grande)")
style = input("Quel style voulez-vous = (classique, calzone, stromboli)")
ingredients = input("Quels ingrédients voulez-vous ?")

diametre = 30
if taille == "grande":
    diametre = 34

ingredients = ingredients.split(", ")

prix = 5 + len(ingredients)

pizza = Pizza(
base=base,
diametre=diametre,
style=style,
ingredients=ingredients,
prix=prix,
)

print(pizza.ingredients, pizza.prix)
pizza.ajouter_ingredients("olives")
print(pizza.ingredients, pizza.prix)
pizza.livraison("9 rue du bois")
pizza.servir(13)
ananas = input("Voulez-vous ajouter des ananas ? (oui,non) ")

if ananas == "oui":
    pizza.ajouter_ingredients ("ananas") """

# exercice 1 Ecrivez un script qui détermine si une chaîne contient ou non le caractère "e"

# chaine = str("abcdefgh")

# if "e" in chaine:
# print("la lettre e est dans la chaîne")
# else:
# print("la lettre e n'est pas dans la chaîne")

# coding: utf-8
"""
from tkinter import Button, Label, Tk, Checkbutton, StringVar, Radiobutton

fenetre = Tk()

label = Label(fenetre, text="Hello World")
label.pack()

#label
label = Label(fenetre, text="Voilà une fenêtre", bg="white")
label.pack()

label = Label(fenetre, text="Voilà une autre fenêtre en rouge", bg="red")
label.pack()

# checkbutton
bouton = Checkbutton(fenetre, text="J'aime les chats")
bouton.pack()



# label
label = Label(fenetre, text="Est-ce que j'aime vraiment les chats", bg="white")
label.pack()

# radiobutton
value = StringVar()
bouton1 = Radiobutton(fenetre, text="Oui", variable=value, value=1)
bouton2 = Radiobutton(fenetre, text="Non", variable=value, value=2)
bouton3 = Radiobutton(fenetre, text="Peu être", variable=value, value=3)
bouton1.pack()
bouton2.pack()
bouton3.pack()

# bouton de sortie
bouton = Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()

fenetre.mainloop() """

# chaine="abcdefghijklmnopqrstuvwxyz" * 10

# i=1
# while i <= len(chaine):
# print(chaine[:i])
# chaine=chaine[i:]
# i+=1


# chaine = "Bonjour je suis Héloïse"

# i=1

# while i<= len(chaine):
# print(chaine[:i])
# i+=1

# def cesar(msg" , clef=0)
# alphabet = "abcdefghijklmnopqrstuvwxyz"
# chiffre = ""

# for l in msg.lower():
# pos = alphabet.find(l)

# if pos != -1:
# chiffre+=alphabet[(pos+clef) % len(alphabet)]
# else:
# chiffre+=1
# return chiffre
