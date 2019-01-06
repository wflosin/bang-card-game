#   ______     ___     ___     __   __  _    _                                                              
#  │      \   │   │   │   \   │  │ /  \│ │  │ │ ®    
#  └.     │   └. .┘   └..\ \  └..┘│  _   │  │ │  
#   │  D  /    / \     ││ \ \  ││ │ / \  │  │ │  
#   │    │    / Δ \    ││  \ \ ││ │ │ .==┘. │ │  
#   │  D  \  / ___ \   ││   \ \││ │ \_│   │ '_'  
#  ┌'     │ ┌ '┐ ┌' ┐ ┌''┐   \  │ │      ┌' ┌-┐ 
#  │______/ │__│ │__│ │__│    \_│  \___^_│  │_│  
##########################################################################################################################################
# KNOWN BUGS
#------------# 
#   After using "Indians!", "Gatling" or "Saloon" the "Use card" Box doesn't dissapear
#   "General Store"
#   When you are the renegade, the g is cut off a bit from the bottom
#   "Panic!" and "Cat Balou", it swaps the cards around if you use one on a "Colt .45"
#   "Panic!" and "Cat Balou", don't work currently
#
##########################################################################################################################################
# CONTENT TO ADD
#----------------#
#   Shuffle the discard when there are no more cards in the deck
#   A clear way to see who took damage after "Gatling" or "Indians!"
#   Only highlight the boxes of players you are in range to shoot
# / A function to switch between "rect" structure and "box" structure (coordinates)
#   Title screen?
#   Duel, Dynamite, 
#   All the chracter abilities
#   AI so the other playes can take a turn
#   Winning or losing the game
#   Making the red box around your character (for cards you play on yourself) to fit exactly around your name
##########################################################################################################################################
# OPTIMIZATIONS AND LEGIBILITY
#------------------------------#
# / Turn game_char into a dictionary
#
##########################################################################################################################################
# / == complete
# - == in progress
#
#

#check if the modules are imported, and if they are not, import them
from sys import modules
if 'random' not in modules:
    import random
#if 'time' not in modules:
#    import time
if 'pygame' not in modules:
    import pygame
from operator import itemgetter
from collections import Counter
#sheriff, renegade, outlaw, outlaw, deputy, outlaw, deputy

def main():

    class cards_:
        def __init__(self):
            self.deck_info = {"Bang!":"The main method to reduce other players' life points. Consider:\na) what the distance to that player is; and\nb) if your weapon is capable of reaching that distance." ,
                        "Missed!":"Play a Missed! card to prevent losing a life when you are the victim of a kind of Bang! card.\nCan only be played on yourself.",
                        "Beer":"Regain a life point, but only up to your maximum life points.\nCan be played out of turn if you have received a hit that is lethal.\nCannot be used when there are only two players left.",
                        "Duel":"Playable to any player.  They may choose to discard a Bang! card.\nIf they do, you may play Bang! cards back and forth.\nThe player failing to play a Bang! card loses one life point.",
                        "Cat Balou":"Force any player to discard a card, regardless of the distance.",
                        "Panic!":"Draw one card from a player at a distance of 1.\nThis card is not affected by weapons, but only by cards such as Mustang and/or Scope.",
                        "Indians!":"Everyone except the player of the card has to discard a Bang! card, or lose a life.",
                        "Gatling":"Shoots a Bang! to all other players, regardless of distance.\nIt is not considered a Bang! card.\nYou can play any number of Gatling cards but only one Bang! card.",
                        "Saloon":"All players, you included regain one life point up to your maximum life points.",
                        "General Store":"Turn as many cards from the deck face up as the players still playing. Starting with you and proceeding clockwise, each player chooses one of those cards and puts it in his hands.",
                        "Stagecoach":"Draw two cards from the deck.",
                        "Wells Fargo":"Draw three cards from the deck.",
                        "Volcanic":"A gun that can hit targets at a distance of 1.\nAllows you to play any number of Bang! cards.",
                        "Schofield": "A gun that can hit targets at a distance of 2.",
                        "Remington":"A gun that can hit targets at a distance of 3.",
                        "Rev. Carabine":"A gun that can hit targets at a distance of 4.",
                        "Winchester":"A gun that can hit targets at a distance of 5.",
                        "Mustang":"Other players see you at a distance increased by one.",
                        "Jail":"Play on another player except the Sheriff.\nOn their next turn, they Draw! (after Dynamite if applicable)\nand if a Heart card is drawn, you escape from jail.\nDiscard the card and start your turn as normal.\nOtherwise, discard the card and miss your turn.",
                        "Barrel":"Allows you to Draw! when you are the target of a Bang!\nIf it is a Heart card, you are Missed! otherwise, nothing happens.",
                        "Scope":"You see all other players at a distance decreased by one.",
                        "Dynamite":"Play in front of you and wait until your next turn.\nDraw! and if you get between a 2 and 9 of Spades, the Dynamite explodes!\nLose three life points, and discard the card.\nOtherwise, pass the Dynamite to the player on your left (who will Draw! on their turn).",
                        "Colt .45":"A gun that can hit targets at a distance of 1."}

                # 1=A    11=J   12=Q   13=K
                # c=clubs   s=spades  d=diamonds  h=hearts
            self.deck = [#Brown cards
                    #25 "Bang!" cards
                    ('Bang!', 9, 'c'), ('Bang!', 8, 'c'), ('Bang!', 7, 'c'), ('Bang!', 6, 'c'), ('Bang!', 5, 'c'), ('Bang!', 4, 'c'),
                    ('Bang!', 3, 'c'), ('Bang!', 3, 'c'), ('Bang!', 2, 'c'), ('Bang!', 1, 's'), ('Bang!',13, 'h'), ('Bang!',12, 'h'),
                    # ('Bang!', 1, 'h'), ('Bang!', 1, 'h'), ('Bang!', 1, 'd'), ('Bang!', 2, 'd'), ('Bang!', 3, 'd'), ('Bang!', 4, 'd'),
                    # ('Bang!', 5, 'd'), ('Bang!', 6, 'd'), ('Bang!', 7, 'd'), ('Bang!', 8, 'd'), ('Bang!', 9, 'd'), ('Bang!',10, 'd'),
                    # ('Bang!',11, 'd'), ('Bang!',12, 'd'),
                    # #13 "Missed!" cards
                    # ('Missed!', 1, 'c'), ('Missed!',10, 'c'), ('Missed!',11, 'c'), ('Missed!',12, 'c'), ('Missed!',13, 'c'), ('Missed!', 2, 's'),
                    # ('Missed!', 3, 's'), ('Missed!', 4, 's'), ('Missed!', 5, 's'), ('Missed!', 6, 's'), ('Missed!', 7, 's'), ('Missed!', 8, 's'),
                    # #6 "Beer" cards
                    # ("Beer", 6, 'h'), ("Beer", 7, 'h'), ("Beer", 8, 'h'), ("Beer", 9, 'h'), ("Beer",10, 'h'), ("Beer",11, 'h'),
                    # #3 "Duel" cards
                    # ("Duel", 8, 'c'), ("Duel",11, 's'), ("Duel",12, 'd'),
                    #4 "Cat Balou" cards
                    ("Cat Balou", 9, 'd'), ("Cat Balou",10, 'd'), ("Cat Balou",11, 'd'), ("Cat Balou",13, 'h'),
                    #4 "Panic!" cards
                    ("Panic!", 1, 'h'), ("Panic!",11, 'h'), ("Panic!",12, 'h'), ("Panic!", 8, 'd'),
                    #2 "Indians!" cards
                    ("Indians!", 1, 'd'), ("Indians!", 13, 'd'),
                    #1 "Gatling" card
                    ("Gatling",10, 'h'),
                    #1 "Saloon" card
                    ("Saloon", 5, 'h'),

                    #2 "General Store" cards
                    ("General Store", 9, 'c'), ("General Store",12, 's'),
                    #2 "Stage Coach" cards
                    ("Stagecoach", 9, 's'), ("Stagecoach", 9, 's'),
                    #1 "Wells Fargo"
                    ("Wells Fargo", 3, 'h'),

                    #Blue cards
                    # #guns, 4th index is range
                    # ("Volcanic",10, 's', 1), ("Volcanic",10, 'c', 1),
                    # ("Schofield",11, 'c', 2), ("Schofield",12, 'c', 2), ("Schofield",13, 'c', 2),
                    # ("Remington",13, 'c', 3), ("Rev. Carabine", 1, 'c', 4), ("Winchester", 8, 's', 5),
                    # #2 "Mustang" cards
                    # ("Mustang", 8, 'h'), ("Mustang", 9, 'h'),
                    # #3 "Jail" cards
                    # ("Jail",10, 's'), ("Jail",11, 's'), ("Jail", 4, 'h'),
                    # #2 "Barrel" cards
                    # ("Barrel",12, 's'), ("Barrel",13, 's'),
                    # #1 "Scope" cards
                    # ("Scope", 1, 's'),
                    # #1 "Dynamite" card
                    # ("Dynamite", 2, 'h')
                    ]

            #jail is a blue card
            self.br_cards = ["Bang!", "Missed!", "Beer", "Duel", "Cat Balou", "Panic!", "Indians!", "Gatling", "Saloon", "General Store", "Stagecoach", "Wells Fargo", "Jail"]
            self.bl_cards = ["Volcanic", "Schofield", "Remington", "Rev. Carabine", "Winchester", "Mustang", "Barrel", "Scope", "Dynamite", "Colt .45"]
            self.guns = ['Volcanic', 'Schofield', 'Remington', 'Rev. Carabine', 'Winchester', 'Colt .45']
            self.card_value = {"Bang!":24, "Missed!":31, "Beer":89, "Duel":17, "Cat Balou":56, "Panic!":71, "Indians!":72, "Gatling":61,
                               "Saloon":8, "General Store":45, "Stagecoach":101, "Wells Fargo":101, "Jail":44,
                               "Volcanic":100, "Schofield":0, "Remington":0, "Rev. Carabine":0, "Winchester":0,
                               "Mustang":92, "Barrel":91, "Scope":38, "Dynamite":0}
            self.num_of_cards = 22

        def pre_card(self, card_num, target=None):
            #discard refresh
            pygame.draw.rect(screen, background, (651,351,98,148))
            pygame.draw.rect(screen, background, (750,350,40,150))
            #discards your card
            discard.append(in_hand[0][card_num])
            del in_hand[0][card_num]
            if target != None:
                cards_in_targets_hand = [*map(itemgetter(0), in_hand[target])]
                return cards_in_targets_hand

        def draw(self, number=False, suit=False):
            #draws a card and puts it into the discard, noting the suit and number
            card = deck[0]
            discard.append(deck[0])
            del deck[0]
            #discard refresh
            pygame.draw.rect(screen, background, (651,351,98,148))
            pygame.draw.rect(screen, background, (750,350,40,150))
            pygame.display.update(((651,351,98,148),(750,350,40,150)))
            if suit:
                return card[2]
            elif number and suit:
                return (card[1], card[2])

        #for dynamite and jail
        def given_card(self, target, card_num):
            blue_cards[target].append(in_hand[turn][card_num])
            del in_hand[turn][card_num]

        def hit(self, target, lives):
            lives[target] -= 1
            if game_char["iden"][target][1] == "El Gringo":
                temp = random.randrange(len(in_hand[turn]))
                in_hand[target].append(in_hand[turn][temp])
                del in_hand[turn][temp]
            elif game_char["iden"][target][1] == "Bart Cassidy":
                in_hand[target].append(deck[0])
                del deck[0]

        def gun_range(self, target, no_gun=False):
            global blue_cards
            #Using a System of equations to solve for the gun range of each player
            #reduced plnum
            p = plnum/2
            #a corresponds to "target", x corresponds to "turn"
            x = turn
            a = (-p) + target
            b = a + p
            c = a + 2*p
            
            if 0 <= x < a:
            	print("gun range opt 1")
            	distance = x - a + p
            elif 0 <= x < b:
            	print("gun range opt 2")
            	distance = (-x) + a + p
            elif b <= x < c:
            	distance = x - a - p
            	print("gun range opt 3")
            elif c <= x:
            	print("gun range opt 4")
            	distance = (-x) + 3*p + a 

            #The range of the gun "turn" is carrying
            if no_gun == True:
                gun_range == 1
            else:
                gun_range = blue_cards[turn][0][3]
            
            print("distance | gun range: ", distance, gun_range)
            #factors that affect the distance
            target_blue_cards = [*map(itemgetter(0), blue_cards[target])]
            turn_blue_cards = [*map(itemgetter(0), blue_cards[turn])]
            if "Scope" in turn_blue_cards:
                distance -= 1
            if "Mustang" in target_blue_cards:
                distance += 1
            if game_char["iden"][target][1] == "Paul Regret":
                distance += 1
            if game_char["iden"][turn][1] == "Rose Doolan":
                distance -= 1

            if gun_range >= distance:
                return True
            else:
                message("That player is out of range!")
                return False

        def bang(self, target, card_num, lives, card_played):
            #only if it was a "Bang!"card being played and not a gatling
            if card_played != "Gatling":
                #checks to see if the target is in range
                if self.gun_range(target) == False:
                    return 0
            #discards your Bang! card
            cards_in_targets_hand = self.pre_card(card_num, target)

            #if the target has a Missed! card
            if "Missed!" in cards_in_targets_hand:
                #If Slab is the one who shot you, you need 2 missed cards to counteract it
                if game_char["iden"][turn][1] == "Slab The Killer":
                    if [*map(itemgetter(0), in_hand[target])].count("Missed!") > 1:
                        for i in range(2):
                            index = cards_in_targets_hand.index("Missed!")
                            discard.append(in_hand[target][index])
                            del in_hand[target][index]
                #Otherwise, they discard a miss
                else:
                    index = cards_in_targets_hand.index("Missed!")
                    discard.append(in_hand[target][index])
                    del in_hand[target][index]

            #if the targest is a one life, they can use a beer instead of a missed as a missed
            elif lives[target] == 1:
                if "Beer" in cards_in_targets_hand:
                    index = cards_in_targets_hand.index("Beer")
                    discard.append(in_hand[target][index])
                    del in_hand[target][index]
                else:
                    return 1
            else:
                self.hit(target, lives)
                #player_spots(lives, blue_cards)
            #pygame.display.update()

        def duel(self, target, card_num, lives, click_spot):
            cards_in_targets_hand = self.pre_card(card_num, target)

            ### TO BE FILLED IN ###

        def catbalou_panic(self, card_played, card_num, ps_blue_cards, ps_blue_cards_width, player_box):
            global blue_cards
            #draws red boxes around all characters and items
            event_box = []
            for i in range(plnum):
                if i == 0:
                    continue
                for j in range(len(ps_blue_cards[i-1])):
                    #print("ps blue cards: ", ps_blue_cards)
                    #print(ps_blue_cards[i-1][j][0])
                    #print(ps_blue_cards[i-1][j][1])
                    #print(ps_blue_cards_width[i-1][j])
                    rect = (ps_blue_cards[i-1][j][0], ps_blue_cards[i-1][j][1], ps_blue_cards_width[i-1][j],28)
                    event_box.append(((ps_blue_cards[i-1][j][0],ps_blue_cards[i-1][j][1]),(ps_blue_cards[i-1][j][0]+ps_blue_cards_width[i-1][j],ps_blue_cards[i-1][j][1]+28)))
                    pygame.draw.rect(screen, (150,0,0), rect, 2)
            pygame.display.update()
            #print(ps_blue_cards, ps_blue_cards_width, i, j, sep=" <> ")
            #print("event_box: ",event_box)
            #print("player_box: ", player_box)
            #print("target_box: ", [((178,755),(1240,793))]+event_box+player_box)
            items = 0
            for i in range(len(ps_blue_cards)):
                items += len(ps_blue_cards[i])
            #print("items: ", items)

            #blue_cards = [[me],[("colt"),(),()],[("colt")],[("colt"),()]]
            #                       |>--your card box---<|  |>items<| |>players<|   
            target_box = events(0, [((178,755),(1240,793))]+event_box+player_box)
            #if you press "end turn"
            #print("taget box:", target_box)
            if type(target_box) == str:
                print("end turn")
                return 'a'
            # if you select another card
            elif target_box == 0:
                print("You selected another card, cat/panic")
                return 'b'
            #decreases target_box by one becuase we already know that the target_box != 0
            target_box -= 1
            #if you click in any of the blue card boxes
            if target_box < items:
                #Makes an unnested list of all the blue cards
                b_c_unnested = [blue_cards[i][j] for i in range(plnum) for j in range(len(blue_cards[i]))]
                #records how many blue cards each player has
                b_c_len = [len(blue_cards[i]) for i in range(plnum)]
                #[3,1,2,1]
                #target box = 0
                print("b_c_unnested: ", b_c_unnested)
                #(0,1,2)("3")(4,5)(6)
                target_item = target_box+len(blue_cards[0])
                if b_c_unnested[target_item][0] != "Colt .45":
                    #if a "Cat Balou" is played
                    if card_played == "Cat Balou":
                        if b_c_unnested[target_item][0] in [*map(itemgetter(0), blue_cards[target_box])]:
                            discard.append(b_c_unnested[target_item])
                            del b_c_unnested[target_item]
                            self.pre_card(card_num)
                    #if a "Panic!" is played
                    elif card_played == "Panic!":
                        #target needs to be in range (1 away)
                        if gun_range(target_box, True) == True:
                            in_hand[0].append(b_c_unnested[target_item])
                            del b_c_unnested[target_item]
                            self.pre_card(card_num)
                else:
                    message("You can't use your {} on their Colt .45!".format(card_played))

                #putting blue_cards back together. The commented loop is too bulky so I used the generator beneath it
                """
                blue_cards = [[] for i in range(plnum)]
                for i in range(plnum):
                    for j in range(b_c_len[i]):
                        blue_cards[i].append(b_c_unnested[0])
                """
                #[[(),(),()],[()],[(),()],[()]]
                blue_cards = [[b_c_unnested[i] for j in range(b_c_len[i])] for i in range(plnum)]

            #if you click on their name
            elif target_box >= items:
                #print("clicked on their name")
                target = target_box - items    + 1
                print("target", target)
                if len(in_hand[target]) != 0:
                    rand = random.randrange(len(in_hand[target]))
                    self.pre_card(card_num)
                    if card_played == "Cat Balou":
                        discard.append(in_hand[target][rand])
                    elif card_played == "Panic!":
                        in_hand[0].append(in_hand[target][rand])
                    del in_hand[target][rand]
                else:
                    message("{} has no cards left!".format(game_char["iden"][target][1]))

            ###AI for computer's turn###

            return 0

        def jail(self, card_num=None, target=None):
            global turn

            if game_char["role"][target] == "Sheriff":
                message("You can't put the Sheriff in Jail!")
                return 0
            elif "Jail" in [*map(itemgetter(0), blue_cards[target])]:
                message("%s is already in jail!"%game_char["iden"][target][1])
                return 0

            if target != None:
                self.given_card(target, card_num)

            #if it is your turn and you have a jail card equipped
            if "Jail" in [*map(itemgetter(0), blue_cards[turn])]:
                if self.draw(False, True) == "h":
                    turn += 1
                    message("%s missed their turn!"%game_char["iden"][turn][0])
                    return 1

        def beer(self, card_num, lives_box, lives):
            if lives[turn] != game_char["iden"][turn][0]:
                self.pre_card(card_num)
                lives[turn] += 1
                pygame.display.update(lives_box)
            else:
                message("You are at your max lives!")

        def stagecoach(self, card_num, cards_rect):
            self.pre_card(card_num)
            for i in range(2): self.give_card(turn)
            pygame.display.update(cards_rect)

        def fargo(self, card_num, cards_rect):
            self.pre_card(card_num)
            for i in range(3): self.give_card(turn)
            pygame.display.update(cards_rect)

        def indians_gatling(self, card_num, card_played, lives):
            self.pre_card(card_num)
            for target_ in range(plnum):
                if target_ == turn:
                    continue
                if game_char["iden"][target_][1] == "Calamity Janet":
                    num = char.calamityjanet(target_)
                    if num == 0:
                        return
                cards_in_targets_hand = [*map(itemgetter(0), in_hand[target_])]
                if card_played == 'Indians':
                    if "Bang!" in cards_in_targets_hand:
                        index = cards_in_targets_hand.index("Bang!")
                        discard.append(in_hand[target_][index])
                        del in_hand[target_][index]
                    else:
                        self.hit(target_, lives)
                #gatling
                else:
                    if "Missed!" in cards_in_targets_hand:
                        index = cards_in_targets_hand.index("Missed!")
                        discard.append(in_hand[target_][index])
                        del in_hand[target_][index]
                    else:
                        self.hit(target_, lives)

        def saloon(self, card_num, lives):
            self.pre_card(card_num)
            for target in range(plnum):
                if lives[target] != game_char["iden"][target][0]:
                    lives[target] += 1
            print(lives)

        def general_store(self, card_num, lives):
            #decrease the bias of volcanic, mustang, and barrel so that the AI can prioritize defense
            def vol_must_bar_bias(store_bias):
                if 'Volcanic' in store_bias[0]:
                    store_bias = store_bias('Volcanic', -14, store_bias)
                if 'Barrel' in store_bias[0]:
                    store_bias = store_bias('Barrel', -15, store_bias)
                if 'Mustang' in store_bias[0]:
                    store_bias = store_bias('Mustang', -16, store_bias)
                return store_bias
            #for the general store, to add and subtract bias to cards found in the store. take into account repeated cards
            def store_bias_f(self, name, number, store_bias):
                #store_bias = [[bang bang],[89 89]]
                for i in range(len(store_bias[0])):
                    if store_bias[0][i] == name:
                        store_bias[1][i] += number
                return store_bias

            self.pre_card(card_num)
            #makes a list of cards that are in the store
            store = [deck[i] for i in range(plnum)]
            store_const = store
            store_turn = turn
            del deck[:plnum]
            card_picked = [[] for i in range(plnum)]
            store_card_names = [*map(itemgetter(0), store)]
            #store_text = [gamefont.render("%s, "%store[i],0,(0,0,0)) for i in range(plnum)]
            store_text = gamefont.render("General Store: ", 0, (0,0,0))
            screen.blit(store_text, (17, 590))
            pygame.draw.rect(screen, background, (15,590,1200,30))

            #general store loop
            for index in range(plnum):
                #displays the general store cards
                store_width = store_text.get_width()
                click = [store_width+17]
                for i in range(plnum):
                    if i == plnum:
                        store_cards = gamefont.render(str(store[i]), 0, (0,0,0))
                    else:
                        store_cards = gamefont.render("%s, "%str(store[i]), 0, (0,0,0))
                    in_hand_width = 184 #from p1_cards_display
                    screen.blit( store_cards, (in_hand_width,760) )
                    in_hand_width += store_cards.get_width() #+12
                    click.append(store_width)

                #your turn to pick a card
                if store_turn == 0:
                    store_click_spots = click_spot(click)
                    card_num = events(0, store_click_spots)
                    print("General Store: var -> card_num: ", card_num)
                    in_hand[0].append(store[card_num])
                    del store[card_num]
                    card_picked[store_turn] = store[card_num][0]


                #AI computer's turn to pick a card
                else:
                    """ The AI algorithm
                    -takes the dictionary entries of the cards that are in "store"
                    -if statemets for Bang!, Missed!, beer, Saloon?, guns, blue cards they already have
                    -Takes the highest value and the AI picks that card
                    -display stuff
                    """
                    ##store_bias = [[bang bang],[89 89]]
                    #store = [(beer,,),(Bang!,,)]
                    store_bias_name = [store[i][0] for i in range(len(store))]
                    store_bias_n =  [self.card_value[store[i][0]] for i in range(len(store))]
                    store_bias = [store_bias_name, store_bias_n]

                    #the individual names of the card that they have in their hand
                    hand_card_names = [*map(itemgetter(0), in_hand[store_turn])]
                    #how many of each card do you have in your hand?
                    hand_n_cards = dict(Counter(hand_card_names))

                    blue_cards_names = [*map(itemgetter(0), blue_cards[store_turn])]

                    #if statements that change the bias for Bang!, Missed!, beer, Saloon?, guns, blue cards they already have
                    #Bang!
                    if 'Bang!' in store_card_names:
                        if hand_n_cards['Bang!'] == 0:
                            if 'Indians!'in store_const:
                                if lives[store_turn] > 3 and 'Beer' not in hand_card_names:
                                    store_bias[1][store_bias[0].index('Bang!')] += 33
                                elif lives[store_turn] == 1:
                                    if turn == store_turn or 'Indians!' in card_picked:
                                        store_bias[1][store_bias[0].index('Bang!')] += 64
                                        store_bias = vol_must_bar_bias(store_bias)

                    if 'Missed!' in store_card_names:
                        if hand_n_cards['Missed!'] == 0:
                            if lives[store_turn] > 3 and 'Beer' not in hand_card_names:
                                store_bias[1][store_bias[0].index('Missed!')] += 27
                            elif lives[store_turn] == 1:
                                store_bias[1][store_bias[0].index('Missed!')] += 57
                                store_bias = vol_must_bar_bias(store_bias)

                    if 'Beer' in store_card_names:
                        #if the AI is at max life or if AI has enough beers to get to max life -1
                        if (lives[store_turn] == game_char["iden"][store_turn][0]) or ((hand_n_cards['Beer'] + lives[store_turn] >= game_char["iden"][store_turn][0]-1) and game_char["iden"][store_turn][0] != 3):
                            store_bias = store_bias_f('Beer', -34, store_bias)
                        if lives[store_turn] == 1:
                            store_bias = vol_must_bar_bias(store_bias)
                            store_bias = store_bias_f('Stagecoach', -13, store_bias)

                    if 'Saloon' in store_card_names:
                        if store_turn == turn+1 and lives[store_turn] == 1:
                            store_bias[1][store_bias[0].index('Saloon')] += 81

                    if 'Scope' in store_card_names:
                        if blue_cards_names[0] == 'Volcanic': ###Include player bias###
                            #just below volcanic if bang/missed biases have been raised
                            store_bias[1][store_bias[0].index('Saloon')] += 49

                    for i in range(len(store_card_names)):
                        for j in range(len(blue_cards_names)):
                            if blue_cards_names[j] == store_card_names[i]:
                                store_bias[1][i] = 0
                    [store_bias[1][i]*0 for i in range(len(store_card_names)) for j in range(len(blue_cards_names)) if blue_cards_names[j] == store_card_names[i]]
                        ###considers the bias of the people after them, if they are friendly, let them take the copy of the blue card
                        ###otherwise, take the duplicate

                    #selects the highest bias card
                    store_n_max = store_bias[1].index(max(store_bias[1]))
                    ###display what card they took###
                    in_hand[store_turn].append(store[store_n_max])
                    del store[store_n_max]
                    del store_bias[store_n_max]
                    card_picked[store_turn] = store[card_num][0]
                    """
                    #inc bias if CPU has no bangs
                    for i in range(len(store)):
                        for j in range(len(in_hand[store_turn])):


                            if in_hand[store_turn][j][0] != "Bang!":
                                store_bias[store.index("Bang!")] += 3
                    """

                #end of the loop, change the turn to the next player
                if store_turn != plnum:
                    store_turn += 1
                else:
                    store_turn = 0



        def give_card(self, player_number):
            #print(in_hand, deck)
            #in_hand[player_number] += [deck[0]]
            (in_hand[player_number]).append(deck[0])
            del deck[0]

    class char:
        #[lives, description]
        identity = [[4, "Bart Cassidy", "Each time he is hit, he draws a card"],
                    [4, "Black Jack", "He shows the second card he draws. On Heart or Diamonds, he draws one more card"],
                    [4, "Calamity Janet", "She can use BANG! cards as Missed! cards and vice versa"],
                    [3, "El Gringo", "Each time he is hit by another player, he draws a card from the hand of that player"],
                    [4, "Jesse Jones", "He may draw his first card from the hand of a player"],
                    [4, "Jourdonnais", 'Whenever he is the target of a Bang!, he may "draw!": on a Heart, he is missed'],
                    [4, "Kit Carlson", "He looks at the top three cards of the deck and chooses the 2 to draw"],
                    [4, "Lucky Duke", 'Each time he "Draws!", he flips the top two cards and chooses one'],
                    [3, "Paul Regret", "All players see him at a distance increased by 1"],
                    [4, "Pedro Remirez", "He may draw his first card from the discard pile"],
                    [4, "Rose Doolan", "She sees all players at a distance decreased by 1"],
                    [4, "Sid Ketchum", "He may discard 2 cards to regain one life point"],
                    [4, "Slab The Killer", "Player needs 2 Missed! cards to cancel his Bang! card"],
                    [4, "Suzy Lafayette", "As soon as she has no cards in hand, she draws a card"],
                    [4, "Vulture Sam", "Whenever a player is eliminated from play, he takes in hand all the cards of that player"],
                    [4, "Willy The Kid", "He can play any number of Bang! cards"]]

        """
        identity = [char.BartCassidy, char.BlackJack, char.CalamityJanet, char.ElGringo,
                    char.JesseJones, char.Jourdonnais, char.KitCarlson, char.LuckyDuke,
                    char.PaulRegret, char.PedroRemirez, char.RoseDoolan, char.SidKetchum,
                    char.SlabTheKiller, char.SuzyLafayette, char.VultureSam, char.WillyTheKid]
        """

        def iden():
            iden = []
            for i in range(len(char.identity)):
                iden.append(char.identity[i][1])
            return iden

        def calamityjanet(target):
            if turn != 0:
                cards_in_targets_hand = [*map(itemgetter(0), in_hand[target])]
                a = "Missed!" in cards_in_targets_hand
                b = 'Bang!' in cards_in_targets_hand
                if a or b:
                    if a and b:
                        if random.randrange(2) == 0:
                            a = True
                            b = False
                        else:
                            b = True
                            a = False
                    if a:
                        index = cards_in_targets_hand.index("Missed!")
                    elif b:
                        index = cards_in_targets_hand.index("Bang!")
                    discard.append(in_hand[target][index])
                    del in_hand[target][index]
                else:
                    return 0
            #program what happens if something plays a card on you


    def help():
        help_text = gamefont.render("See console.",0,(50,0,0))
        screen.blit(help_text, (mid_width(help_text),50))
        pygame.display.update()
        print("\n|------------HELP MENU------------|")
        iden = char.iden()
        #characters
        while True:
            info = input("Type the name of the card or player you want information on (case sensitive).\nType 'Cards' or 'Characters' for a list of them\nDON'T CLICK ON THE GAME WINDOW\nOnly press [ENTER] to continue playing\n\n")
            if info in iden:
                char_info = iden.index(info)
                print(char.identity[char_info][2])
                print("")
            #cards
            elif info in (cards.bl_cards + cards.br_cards):
                print(cards.deck_info[info])
                print("")
            elif info == '':
                pygame.draw.rect(screen, background, (mid_width(help_text)-1,48,help_text.get_width()+2,help_text.get_height()+2))
                pygame.display.update()
                print("\nReturn to the game screen")
                return 1
            elif info == 'Cards':
                print(str(cards.bl_cards + cards.br_cards).replace("[","").replace("]","").replace("'","") + "\n")
            elif info == 'Characters':
                print(str(iden).replace("[","").replace("]","").replace("'","") + "\n")
            elif info == 'reset':
                return False
            else:
                print("Invalid input\n")

    def message(message):
        text = gamefont.render(message,0,(0,0,0))
        text_rect = (mid_width(text), 510, text.get_width(), text.get_height())
        screen.blit(text, (text_rect[0],510))
        pygame.display.update(text_rect)
        #clears the text
        events(1)
        pygame.draw.rect(screen, background, text_rect)
        pygame.display.update(text_rect)

    def preparation():
        global cards
        cards = cards_()
        #determining role cards
        global plnum
        plnum = None
        while plnum == None:
            plnum = 4
            #commented just for testing
            #plnum = int(input("how many people do you want to play against? 4-7 players: \n"))
            if plnum == 4:
                print("There is one sheriff, one renegade, and two outlaws")
                players = ["Sheriff", "Renegade", "Outlaw", "Outlaw"]
            elif plnum == 5:
                print("There is one sheriff, one renegade, two outlaws, and one deputy")
                players = ["Sheriff", "Renegade", "Outlaw", "Outlaw", "Deputy"]
            elif plnum == 6:
                print("There is one sheriff, one renegade, three outlaws, and one deputy")
                players = ["Sheriff", "Renegade", "Outlaw", "Outlaw", "Deputy", "Outlaw"]
            elif plnum == 7:
                print("There is one sheriff, one renegade, three outlaws, and two deputies")
                players = ["Sheriff", "Renegade", "Outlaw", "Outlaw", "Deputy", "Outlaw", "Deputy"]
            else:
                print("You can't play with that number of players")
                plnum = None
                #time.sleep(1)
        #time.sleep(1)

        #assigns a Role to the character
        role = list(range(plnum))
        for i in range(plnum):
            role[i] = players[(random.randrange(0,len(players)))]
            players.remove(role[i])

        #assigns each character an identity
        iden = list(range(plnum))
        for i in range(plnum):
            iden[i] = char.identity[(random.randrange(0,len(char.identity)))]
            char.identity.remove(iden[i])
            #iden[i] = iden[i][:2]
        #[BartCassidy, WillyTheKid, etc]

        global game_char
        game_char = {"role":role, "iden":iden}
        #[[Sheriff, outlaw, outlaw deputy], [[4, Rose],[4, Vulture],]]

        #print(game_char)
        #gives the sherrif a bonus life
        for i in range(plnum):
            if game_char["role"][i] == "Sheriff":
                game_char["iden"][i][0] += 1

        global deck
        deck = cards.deck
        random.shuffle(deck)
        #----
        global discard
        discard = []
        #giving out cards
        #lst = [['a','b','c'], [1,2,3], ['x','y','z']]
        """
        outputlist = []
        for values in game_char["iden"]:
            outputlist.append(values[0])
        """
        outputlist = [values[0] for values in game_char["iden"]]

        global your_turn

        p_lives_rect = (1152,704,50,60)

        global in_hand
        in_hand = [[] for i in range(plnum)]
        #print(outputlist)

        global gun_range
        gun_range = [()]

        for i in range(max(outputlist)):
            #eg/ i (from 0 to 5 cards)
            for j in range(plnum):
                #eg/ i (from 0 to 4 players)
                #print(i,j, game_char["iden"][j][0])
                # i % plnum
                if (i < game_char["iden"][j][0]):
                    #last time, eg/ i=4
                    cards.give_card(j)
        #print(in_hand)
        #in_hand = [[bang,missed],[general store, volcanic]]
        global blue_cards
        blue_cards = [[("Colt .45","","",1), ("Mustang","",""), ("Barrel","","")] for i in range(plnum)]

        """
        lives = ["" for i in range(plnum)]
        for i in range(plnum):
            lives[i] = game_char["iden"][i][0]
        """
        lives = [game_char["iden"][i][0] for i in range(plnum)]

        #screen initialization
        (width, height) = (1250,800)
        global screen
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bang!")
        global background
        background = (225, 210, 173)
        screen.fill(background)
        pygame.display.flip()

        pygame.font.init()
        global gamefont
        #height of text is 28
        gamefont = pygame.font.SysFont('bookantiqua', 22)
        #gamefont.set_bold(True)

        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        #temp text example
        """
        text = gamefont.render(str(in_hand), 0, (0,0,0))
        mid_width = width/2 - text.get_rect().width/2
        mid_height = height/2 - text.get_rect().height/2
        """

        """
        #texturing the surface
        for i in range(25000):
            #darkest
            #219, 201, 158
            #lightest
            #225, 210, 173
            point1 = (random.randrange(1250), random.randrange(800))
            point2 = (point1[0]*[-1,1][random.randrange(2)]+random.randrange(5), point1[1]*[-1,1][random.randrange(2)]+random.randrange(5))
            point3 =
            point4 =
            pygame.draw.aalines(screen, colour, 0, pointlist, 1)
        """
        pygame.draw.lines(screen, (156,115,70), True, [(0,0),(1250,0),(1250,800),(0,800)], 15)
        pygame.draw.line(screen, (156,115,70), (0,655), (1250,655), 12)
        pygame.draw.line(screen, (156,115,70), (170,655), (170,800), 12)
        #deck and discard
        pygame.draw.rect(screen, (156,115,70), (500,350,100,150), 0)
        pygame.draw.aalines(screen, (176,135,90), 0, ((498,352),(498,502),(598,502)), 1)
        pygame.draw.aalines(screen, (176,135,90), 0, ((496,354),(496,504),(596,504)), 1)
        pygame.draw.rect(screen, (0,0,0), (650,350,100,150), 1)

        screen.blit((gamefont.render("Character:           %s"%(game_char["iden"][0][1]),0,(0,0,0))), (17,670))
        screen.blit((gamefont.render("Ability:                %s"%(game_char["iden"][0][2]),0,(0,0,0))), (17,700))
        screen.blit((gamefont.render("Role:                    %s"%(game_char["role"][0]),0,(0,0,0))), (17,730))
        screen.blit((gamefont.render("Lives:",0,(0,0,0))), (1150,680))
        screen.blit((gamefont.render("Cards in hand:",0,(0,0,0))), (17,760))
        screen.blit((gamefont.render("Blue cards: %s"%(((str(list(map(itemgetter(0), blue_cards[0]))).replace("[","")).replace("]","")).replace("'"," ")), 0,(0,0,0))), (17,620))
        screen.blit((gamefont.render("Help",0,(0,0,0))), (1190,10))

        start_turn_text = (pygame.font.SysFont('bookantiqua', 90)).render("Your turn!", 0, (0,0,0))
        start_turn_x = mid_width(start_turn_text)
        start_turn_y = 510
        start_turn_rect = (start_turn_x, start_turn_y, start_turn_text.get_width(), start_turn_text.get_height())

        #[0]==Help
        global buttons
        buttons = [((1190,0),(1250,40)),((0,0),(105,40)),((),())]
        cards_rect = (178, 755, 1062, 38)
        blue_card_rect = (15,620,1220,30)
        shot_text = (gamefont.render('You have already played a "Bang!" card!', 0, (0,0,0)))
        itemed_text = (gamefont.render('You already have that item!', 0, (0,0,0)))
        use_card_text = gamefont.render('Use card', 0, (0,0,0))
        use_card_rect = (mid_width(use_card_text), 510, use_card_text.get_width(), use_card_text.get_height())
        use_card = {"text":use_card_text, "rect":use_card_rect}
        #print(use_card)

        return (lives, start_turn_text, start_turn_x, start_turn_y, start_turn_rect, cards_rect, blue_card_rect, shot_text, itemed_text, blue_cards, p_lives_rect, use_card)

    def death(lives, target):
        global plnum
        if game_char["role"][target] == 'Outlaw':
            death_text = 'An outlaw died!'
            #death_text_pos = (548, 522)
            #get 3 cards
            for i in range(3):
                cards.give_card(turn)
        elif game_char["role"][target] == 'Renegade':
            death_text = 'The renegade died!'
            #death_text_pos = (530.5, 522)
        elif game_char["role"][target] == 'Deputy':
            death_text = 'A deputy died!'
            #death_text_pos = (551.5, 522)
            #if the sheriff killed the deputy
            if game_char["role"][turn] == "Sheriff":
                for i in range(len(in_hand[turn])):
                    discard.append(in_hand[turn][i])
                    del in_hand[turn][i]
                for i in range(len(blue_cards[turn])):
                    if i == 0 and blue_cards[turn][0][0] == 'Colt .45':
                        continue
                    discard.append(blue_cards[turn][i])
                    del blue_cards[turn][i]
        message(death_text)
        """
        screen.blit(death_text, death_text_pos)
        pygame.display.update()
        events(1)
        pygame.draw.rect(screen, background, (death_text_pos[0], death_text_pos[1], death_text.get_width(), death_text.get_height()))
        """
        plnum -= 1
        vulture_playing = False
        #if vulture sam is playing
        for i in range(plnum):
            if game_char["iden"][i][1] == "Vulture Sam":
                vulture_playing = True
                for j in range(len(in_hand[target])):
                    in_hand[i].append(in_hand[target][j])
                for k in range(len(blue_cards[target])):
                    if k == 0 and blue_cards[target][0][0] == 'Colt .45':
                        continue
                    else:
                        in_hand[i].append(blue_cards[target][k])

        if vulture_playing == False:
            for i in range(len(in_hand[target])):
                discard.append(in_hand[target][i])
            for i in range(len(blue_cards[target])):
                if i == 0 and blue_cards[target][0][0] == 'Colt .45':
                    continue
                discard.append(blue_cards[target][i])
        del in_hand[target]
        del blue_cards[target]
        del game_char["role"][target]
        del game_char["iden"][target]
        del lives[target]

        #add victory conditions
        if "Sheriff" not in game_char["role"]:
            #outlaws in
            pass
        elif "Outlaw" not in game_char["role"] and "Renegade" not in game_char["role"]:
            #sheriff and deputy win
            pass
        elif plnum == 1 and "Renegade" in game_char["role"]:
            #renegade wins
            pass

    def mid_width(text, width=1250):
        mid_width = width/2 - text.get_rect().width/2
        return mid_width

    def mid_height(text, height=800):
        mid_height = height/2 - text.get_rect().height/2
        return mid_height

    def p1_cards_display(cards_rect):
        pygame.draw.rect(screen, background, cards_rect)
        in_hand_width = 184
        click = [184]
        for i in range(len(in_hand[0])):
            if i == len(in_hand[0])-1:
                cards_in_hand = gamefont.render(str(in_hand[0][i][0]), 0, (0,0,0))
            else:
                cards_in_hand = gamefont.render("%s, "%str(in_hand[0][i][0]), 0, (0,0,0))
            screen.blit( cards_in_hand, (in_hand_width,760) )
            in_hand_width += cards_in_hand.get_width() #+12
            click.append(in_hand_width)
            #print(click)

        return click

    def click_spot(click):
        click_spots = [() for i in range(len(in_hand[0]))]
        for i in range(len(in_hand[0])):
            if i == 0:
                click_spots[i] = ((178,755),(click[1],792))
            else:
                click_spots[i] = ((click[i],755),(click[i+1],792))
        return click_spots

    def player_spots(lives):
        #player_orientation is in box coordinates
        name_display = ["" for i in range(plnum)]

        for index in range(plnum):
            name_display[index] = gamefont.render(game_char["iden"][index][1], 0, (0,0,0))

        #2,3,4,5,6,7 player orientation
        #from 0 to 655
        try:
            player_orientation = [[(mid_width(name_display[1]), 125)],
                                  [(200,250), (1000,250)],
                                  [(200,400), (mid_width(name_display[2]), 150), (1000, 400)],
                                  [(200,425), (350,125), (850,125), (1000,425)],
                                  [(200,475), (250,250), (mid_width(name_display[3]),100), (950,250), (1000,475)],
                                  [(200,475), (225,250), (400,100), (800,100), (975,250), (1000,475)]]
        except IndexError:
            try:
                player_orientation = [[(mid_width(name_display[1]), 125)],
                                  [(200,250), (1000,250)],
                                  [(200,400), (mid_width(name_display[2]), 150), (1000, 400)],
                                  [(200,425), (350,125), (850,125), (1000,425)]]
            except IndexError:
                player_orientation = [[(mid_width(name_display[1]), 125)],
                                  [(200,250), (1000,250)]]

        name_text = ["" for i in range(plnum)]
        #Star on sheriff + display the names
        player_spots_blue_cards = [[] for i in range(plnum-1)]
        player_spots_blue_cards_width = [[] for i in range(plnum-1)]
        for i in range(plnum):
            if i == 0:
                continue
            else:
                name_text[i-1] = gamefont.render((str(lives[i]) + " " + game_char["iden"][i][1] + " " + str(len(in_hand[i]))),0,(0,0,0))
                pygame.draw.rect(screen, background, (player_orientation[plnum-2][i-1][0]-2, player_orientation[plnum-2][i-1][1]-30, name_text[i-1].get_width()+4, 28+72))
                if game_char["role"][i] == "Sheriff":
                    x = player_orientation[plnum-2][i-1][0] + (name_text[i-1].get_width())/2 -20
                    #x = player_orientation[plnum-2][i-1][0] + 55
                    y = player_orientation[plnum-2][i-1][1] + 50
                    pygame.draw.lines(screen, (166,124,0), True, [(0+x,0+y),(25+x,-72+y),(50+x,0+y),(-15.4+x,-47.6+y),(65.6+x,-47.6+y)], 3)
                screen.blit(name_text[i-1], player_orientation[plnum-2][i-1])

            #displays blue cards
            #blue_cards = [[("Colt .45", "a", "1")] for i in range(plnum)]
            #*#print("Player Spots: <> ", blue_cards[i], i)
            player_spots_blue_cards[i-1] = ["" for i in range(len(blue_cards[i]))]
            player_spots_blue_cards_width[i-1] = ["" for i in range(len(blue_cards[i]))]
            for j in range(len(blue_cards[i])):
                player_spots_blue_cards[i-1][j] = (player_orientation[plnum-2][i-1][0],player_orientation[plnum-2][i-1][1]+28*(j+1))
                #print(i,j,blue_cards)
                blue_card_text = (gamefont.render(blue_cards[i][j][0], 0, (0,0,0)))
                screen.blit(blue_card_text, player_spots_blue_cards[i-1][j])
                player_spots_blue_cards_width[i-1][j] = (blue_card_text.get_width())
                #print("player spots width %s"%(player_spots_blue_cards_width), "\n")
        #print(blue_cards)
        return (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width)

    def events(call, click_spots=None):
        global running
        while True:
            for event in pygame.event.get():
                #print(running)
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    #help button
                    if (buttons[0][0][0] <= mouse_pos[0] < buttons[0][1][0]) & (buttons[0][0][1] <= mouse_pos[1] < buttons[0][1][1]):
                        num = help()
                        if num == False:
                            running = False
                            break
                    if (buttons[1][0][0] <= mouse_pos[0] < buttons[1][1][0]) & (buttons[1][0][1] <= mouse_pos[1] < buttons[1][1][1]):
                        return 'End turn'
                    elif call == 0:
                        #checks if mouseUP is within a certain boundary
                        #[ ((#,#),(#,#)), ((#,#),(#,#)), ]
                        #mouse_pos = pygame.mouse.get_pos()
                        for i in range(len(click_spots)):
                            #x values & y values
                            if (click_spots[i][0][0] <= mouse_pos[0] < click_spots[i][1][0]) & (click_spots[i][0][1] <= mouse_pos[1] < click_spots[i][1][1]):
                                return i
                    elif call == 1:
                        return 1
                    print(mouse_pos)

    #USE ONLY ONE SET OF BOX COORDINATES, i.e. index the coordinates you want 
    #(this will make it so we know how many inputs into events there is)
    def rect2box(coords):
    	#Rectangluar coordinates
    	#     (left, top, width, height)
    	#     (left, top, right-left=width, bottom-top=height)
    	#Box coordinates
    	#     [ ((#,#),(#,#)), ((#,#),(#,#)), ]
    	#     [ ((left,top),(left+width=right, top+height=bottom)), ", "]
    	
    	#(inputted rect) to box
    	if len(coords) == 4:
    		return ((coords[0],coords[1]),(coords[0]+coords[2],coords[1]+coords[3]))
    	#(inputted box) to rect
    	else:
    		return (coords[0][0],coords[0][1],coords[1][0]-coords[0][0],coords[1][1]-coords[0][1]) 

    """
    def clear_red(screen):
        pygame.draw.rect(screen, background, (178, 755, 1060, 40))
        pygame.draw.rect(screen, background, (17, 610, 1220, 30))
    """

    def game():
        print("Bang!")
        #time.sleep(0.25)
        print("Loading: Game Preparation")
        #time.sleep(0.25)
        global blue_cards
        (lives, start_turn_text, start_turn_x, start_turn_y, start_turn_rect, cards_rect, blue_card_rect, shot_text, itemed_text, blue_cards, p_lives_rect, use_card) = preparation()
        (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)

        #pygame.draw.polygon(screen, (0,0,0), ((101,99), (101,199), (149,49)), 0)
        #pygame.draw.aalines(screen, (0,0,0), 1, ((100,100), (100,200), (150,50)), 1)
        #pygame.draw.arc(screen, (0,0,0), ((500,500),(750,750)), 1, 2, 3)
        #pygame.draw.lines(screen, (0,0,0), True, [player_orientation[5][0], player_orientation[5][1],player_orientation[5][2],player_orientation[5][3],player_orientation[5][4],player_orientation[5][5]], 3)
        #(100*a,100*a),(125*a,28*a),(150*a,100*a),(84.6*a,52.4*a),(165.6*a,52.4*a)
        #(50*a,50*a),(62.5*a,14*a),(75*a,50*a),(42.3*a,26.2*a),(82.8*a,26.2*a)
        #pygame.draw.rect(screen, (0,0,0), (178,755,120,37), 1)

        #game loop
        global running
        running = True
        while running:
            #(178,755,120,37)
            #pygame.draw.rect(screen, background, (650,350,140,150), 0)
            pygame.draw.rect(screen, (0,0,0), (650,350,100,150), 1)
            #displays your cards and returns the x values for the click bounds
            click =  p1_cards_display(cards_rect)
            #screen.blit((gamefont.render("Cards in hand:   %s"%(((str(list(map(itemgetter(0), in_hand[0]))).replace("[","")).replace("]","")).replace("'"," ")),0,(0,0,0))), (17,760))
            #screen.blit((gamefont.render("Blue cards:                    %s"%(blue_cards[0][0]), 0,(0,0,0))), (17,620))
            screen.blit((pygame.font.SysFont('bookantiqua', 50)).render(str(lives[0]), 0, (0,0,0)), (1165,705))
            pygame.display.update()

            #turns
            global turn
            #sheriff goes first
            #turn = (game_char["role"]).index("Sheriff")
            turn = 0
            #your turn
            if turn == 0:
                #displays "Your turn!" and dissapears when you click
                screen.blit(start_turn_text, (start_turn_x, start_turn_y))
                pygame.display.update(start_turn_rect)

                events(1)
                #screen.blit((pygame.font.SysFont('bookantiqua', 100)).render("Your turn!", 0, background), (start_turn_x, start_turn_y))
                pygame.draw.rect(screen, background, start_turn_rect)
                screen.blit((gamefont.render("End Turn",0,(0,0,0))), (12,10))

                #1. draw two cards
                cards.give_card(0)
                cards.give_card(0)

                bang_played = 0
                your_turn = True
                while your_turn == True:
                    num = None
                    #discard refresh
                    pygame.draw.rect(screen, background, (651,351,98,148))
                    pygame.draw.rect(screen, background, (751,350,20,150))
                    try:
                        screen.blit((gamefont.render(str(discard[-1][0]), 0, (0,0,0))), (652,390))
                    except IndexError:
                        pass
                    #gets rid of extra red lines around the player that might not have been erased (e.g. if you switch cards)
                    for i in range(plnum-1):
                        pygame.draw.rect(screen, background, (player_orientation[plnum-2][i][0], player_orientation[plnum-2][i][1], 200, 100))
                    click =  p1_cards_display(cards_rect)
                    (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)
                    pygame.display.update()
					
                    #2. play any number of cards
                    #provide a list of locations that you can click on, the run it through events()
                    click_spots = click_spot(click)
                    print("click spots: ", click_spots)
                    #[ ((#,#),(#,#)), ((#,#),(#,#)), ]
                    card_num = events(0, click_spots)
                    if type(card_num) == str:
                        break
                    #pygame.draw.rect(screen, background, cards_rect)
                    #draws red boxes around your cards
                    pygame.draw.lines(screen, (150,0,0), True, [(click[card_num]-5,755), (click[card_num]-5,790), (click[card_num+1]-2,790), (click[card_num+1]-2,755)], 2)
                    pygame.display.update()

                    card_played = in_hand[0][card_num][0]

                    #if a blue card is played
                    #["Volcanic", "Schofield", "Remington", "Rev. Carabine", "Winchester", "Mustang", "Barrel", "Scope", "Dynamite"]
                    if card_played in cards.bl_cards:
                        ### JAIL IS IN THE BR_CARDS SECTION ###
                        #draws lines around The blue card text box
                        pygame.draw.rect(screen, (150,0,0), (15,620,1219,29), 2)
                        pygame.display.update((cards_rect, blue_card_rect))
                        blue_box = events(0 , [((15,620),(1235,645))]+[rect2box(cards_rect)])
                        #if you press "end turn"
                        if type(blue_box) == str:
                            pygame.draw.rect(screen, background, cards_rect)
                            pygame.draw.rect(screen, background, (15,620,1219,29), 2)
                            break
                        #if you click on blue card text box
                        elif blue_box == 0:
                            #get rid of the red. The cards_rect
                            pygame.draw.rect(screen, background, blue_card_rect)
                            #if you already have that blue card
                            if card_played in list(map(itemgetter(0), blue_cards[0])):
                                #Adds text saying that you already have that card equiped
                                message('You already have that item!')
                                """screen.blit(itemed_text, (489.5, 522))
                                pygame.display.update((489.5,522,300,25))
                                if events(1) == 1:
                                    pygame.draw.rect(screen, background, (489.5,522,300,27))
                                    pygame.display.update((489.5,522,300,27))"""
                            #if you already have a gun equipped, discard the one you have equipped
                            elif (card_played in cards.guns):
                                if blue_cards[0][0][0] != "Colt .45":
                                    discard.append(blue_cards[0][0])
                                del blue_cards[0][0]
                                #print("this one!")
                                blue_cards[0].insert(0, in_hand[0][card_num])
                                del in_hand[0][card_num]
                            else:
                                blue_cards[0].append(in_hand[0][card_num])
                                del in_hand[0][card_num]
                            # in_hand[0] == [[(bang,,),(missed,,)],[(general store,,), (volcanic,,)]]
                            #if you dont select the box
                            click = p1_cards_display(cards_rect)
                            screen.blit((gamefont.render("Blue cards: %s"%(((str(list(map(itemgetter(0), blue_cards[0]))).replace("[","")).replace("]","")).replace("'"," ")), 0,(0,0,0))), (17,620))
                            pygame.display.update((cards_rect, blue_card_rect, (650,350,100,200)))
                        # if you select another card
                        elif 1 <= blue_box:
                            pygame.draw.rect(screen, background, blue_card_rect)
                            screen.blit((gamefont.render("Blue cards: %s"%(((str(list(map(itemgetter(0), blue_cards[0]))).replace("[","")).replace("]","")).replace("'"," ")), 0,(0,0,0))), (17,620))
                            card_num = blue_box - 1
                            continue
                        pygame.display.update()
                    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
                    #"""
                    #if a brown card is played
                    #["Bang!", "Missed!", "Beer", "Duel", "Cat Balou", "Panic!", "Indians!", "Gatling", "Saloon", "General Store", "Stagecoach", "Wells Fargo"]
                    elif card_played in cards.br_cards:
                        # If a card that targets someone is played
                        if card_played in ['Bang!', 'Duel', 'Cat Balou', 'Panic!', 'Jail']:
                            #draw red rectangles around each character
                            red_player_rect = ["" for i in range(plnum-1)]
                            red_player_box = [() for i in range(plnum-1)]
                            for i in range(plnum):
                                if i == 0:
                                    continue
                                #rect =(x,y,width,height)
                                red_player_rect[i-1] = (player_orientation[plnum-2][i-1][0]-2, player_orientation[plnum-2][i-1][1], name_text[i-1].get_width()+4, name_text[i-1].get_height())
                                pygame.draw.rect(screen, (150,0,0), red_player_rect[i-1], 2)
                                #gets the variable ready to be called into events() i.e. top right point and bottom right point
                                red_player_box[i-1] = rect2box(red_player_rect[i-1])
                            pygame.display.update(red_player_rect)



                            #if a cat balou is played, have all the character boxes and blue card boxes selected
                            if card_played == 'Cat Balou' or card_played == 'Panic!':
                                #print(player_spots_blue_cards, player_spots_blue_cards_width)
                                num = cards.catbalou_panic(card_played, card_num, player_spots_blue_cards, player_spots_blue_cards_width, red_player_box)
                                #print(num)
                                #gets rid of red lines
                                for i in range(plnum-1):
                                    #pygame.draw.rect(screen, background, red_player_rect[i], 2)                                                     EDIT: 27 -> 30
                                    pygame.draw.rect(screen, background, (player_orientation[plnum-2][i][0]-2, player_orientation[plnum-2][i][1]-22, 200, 50+30*len(blue_cards[i])))
                                pygame.draw.rect(screen, background, cards_rect, 2)
                                #print(blue_cards)
                                #(player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)
                                #If you click end turn
                                if num == 'a':
                                    break
                                #if you select another card or if everything went smoothly
                                elif num == 'b' or num == 0:
                                    print("AHHH")
                                    continue
                            
                            #[ ((#,#),(#,#)), ((#,#),(#,#)), ]
                            target = events(0, [rect2box(cards_rect)]+[red_player_box])
                            #if you press "end turn"
                            if type(target) == str:
                                print("end turn")
                                break
                            # if you select another card
                            elif target == 0:
                                print("You selected another card")
                                continue
                            #where Target WAS

                            #if you click in any of those boxes
                            elif target < plnum:
                                print("target")
                                #if a certain card is played
                                if (card_played == 'Bang!'):
                                    print(blue_cards, "Bang! call")
                                    #print("volcanic? ", in_hand[0][0][0],(in_hand[0][0][0] == 'Volcanic'))
                                    #print("Willy? ", game_char["iden"][0][1],(game_char["iden"][0][1] == 'Willy The Kid'))
                                    #print("Bang played? ", bang_played != 0)
                                    if (bang_played == 0 or ((game_char["iden"][0][1] == 'Willy The Kid') or (blue_cards[0][0][0] == 'Volcanic'))):
                                        print("bang was played")
                                        num = cards.bang(target, card_num, lives, card_played)
                                        #if death occurs
                                        if num == 1:
                                            death(lives, target)
                                            for i in range(plnum):
                                                pygame.draw.rect(screen, background, (player_orientation[plnum-1][i][0]-2, player_orientation[plnum-1][i][1]-22, 200, 50+27*len(blue_cards[target])))
                                            (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)
                                            print(plnum)
                                        #if the target is out of range
                                        elif num != 0:
                                            bang_played = 1

                                    elif (bang_played == 1):
                                        # and not ((game_char["iden"][0][1] == 'Willy The Kid') or (in_hand[0][0][0] == 'Volcanic')):
                                        #displays "You have already played a bang! card" and dissapears when you click
                                        message('You have already played a "Bang!" card!')
                                        """
                                        screen.blit(shot_text, (428.5, 522))
                                        pygame.display.update((428.5,522,410,25))
                                        if events(1) == 1:
                                            pygame.draw.rect(screen, background, (428.5,522,420,27))
                                            (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)
                                            pygame.display.update()"""
                                        continue
                                    else:
                                        continue

                                elif card_played == 'Duel':
                                    cards.duel(target, card_num, lives, click_spots)

                                elif card_played == 'Jail':
                                    num = cards.jail(card_num, target)
                                    if num == 0:
                                        continue
                                    elif num == 1:
                                        break

                            #gets rid of red lines
                            for i in range(plnum-1):
                                pygame.draw.rect(screen, background, red_player_rect[i], 2)
                            pygame.draw.rect(screen, background, cards_rect, 2)
                            (player_orientation, name_text, player_spots_blue_cards, player_spots_blue_cards_width) = player_spots(lives)
                            pygame.display.update()
                        #____________________________________________________________________________________________________________________________#
                        #cards used on yourself
                        elif card_played in ['Beer', 'Stagecoach', 'Wells Fargo']:
                            #draw red lines around your own name. the (184,672,150,25) is where your name is
                            pygame.draw.rect(screen, (150,0,0), (184,672,150,25), 2)
                            pygame.display.update((184,672,150,25))
                            your_name = events(0, [rect2box(cards_rect)]+[((184,672),(334,697))])
                            #if you click end turn
                            if  type(your_name) == str:
                                print("end turn")
                                break
                            #if you click on another card
                            elif your_name == 0:
                                print("You chose another card")
                                continue
                            #if you click on you own name
                            elif your_name == 1:
                                if card_played == 'Beer':
                                    cards.beer(card_num, p_lives_rect, lives)

                                elif card_played == 'Stagecoach':
                                    cards.stagecoach(card_num, cards_rect)

                                elif card_played == 'Wells Fargo':
                                    cards.fargo(card_num, cards_rect)
                            pygame.draw.rect(screen, background, (184,672,150,25), 2)
                            pygame.display.update((184,672,150,25))
                        #____________________________________________________________________________________________________________________________#
                        #untargeted cards
                        elif card_played in ['Indians!', 'Gatling', 'Saloon', 'General Store']:
                            #displays "use card" with a red box around it
                            screen.blit(use_card["text"], (use_card["rect"][0],use_card["rect"][1]))
                            pygame.draw.rect(screen, (150,0,0), use_card["rect"], 1)
                            pygame.display.update(use_card["rect"])

                            use_card_event = events(0, [rect2box(cards_rect)]+[rect2box(use_card["rect"])])
                            #if you click end turn
                            if  type(use_card_event) == str:
                                print("end turn")
                                break
                            #if you click on another card
                            elif use_card_event == 0:
                                print("You chose another card")
                                continue
                            elif use_card_event == 1:
                                if card_played in ['Indians!', 'Gatling']:
                                    cards.indians_gatling(card_num, card_played, lives)
                                elif card_played == 'Saloon':
                                    cards.saloon(card_num, lives)
                                    print(lives)
                                elif card_played == 'General Store':
                                    cards.general_store(card_num, lives)
	                        #clears "use card" text and red box
                            pygame.draw.rect(screen, background, use_card["rect"])
                            pygame.display.update(use_card["rect"])
                    #if events(0, [(),()]) == 0:
                    #"""

                    pygame.display.update()



            pygame.display.update()
        return 0






    if game() == 0:
        global blue_cards, turn, plnum, game_char, disacrd, your_turn, in_hand, screen, background, game_font, buttons, running
        blue_cards=turn=plnum=game_char=disacrd=your_turn=in_hand=gun_range=screen=background=game_font=buttons = None
        running = True

        game()

if __name__ == "__main__":
    main()

