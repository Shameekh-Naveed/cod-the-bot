from operator import imod


def RPS(user1,user2="comp"):
    from random import randint


    emojis={
        "stable":":right_fist:      :left_fist:",
        "rock":":fist:",
        "paper":":hand_splayed:",
        "scissor":":v:"
    }
    
    choices = ["Rock","Scissors","Paper"]
    
    def user_choice(user):
        if user=="rock":
            user=0
        elif user1=="scissor":
            user=1
        elif user=="paper":
            user=2 
        return user 
    
    
    user1_choice = user_choice(user1)

    if user2=="comp":
        user2_choice = randint(0,2)

    user2 = choices[user2_choice]
    
    

    def field(user1_choice,user2_choice):
        field = emojis["stable"]
        if user1_choice == 0 and user2_choice == 0:
            field = emojis["rock"]+"      "+emojis["rock"]
        elif user1_choice == 0 and user2_choice == 1:
            field = emojis["rock"]+"      "+emojis["scissor"]
        elif user1_choice == 0 and user2_choice == 2:
            field = emojis["rock"]+"      "+emojis["paper"]
        elif user1_choice == 1 and user2_choice == 0:
            field = emojis["scissor"]+"      "+emojis["rock"]
        elif user1_choice == 1 and user2_choice == 1:
            field = emojis["scissor"]+"      "+emojis["scissor"]
        elif user1_choice == 1 and user2_choice == 2:
            field = emojis["scissor"]+"      "+emojis["paper"]
        elif user1_choice == 2 and user2_choice == 0:
            field = emojis["paper"]+"      "+emojis["rock"]
        elif user1_choice == 2 and user2_choice == 1:
            field = emojis["paper"]+"      "+emojis["scissor"]
        elif user1_choice == 2 and user2_choice == 2:
            field = emojis["paper"]+"      "+emojis["paper"]
        return field
        
    def game_stat(user1_choice,user2_choice):
        stat={
            "message":"Yay! You win",
            "description":"You're really good at it",
            "color":0x00ff00,
        }
        if user1_choice == user2_choice:
            stat={
            "message":"Huh! We had a draw",
            "description":"Good game",
            "color":0x808080,
        }
        elif user1_choice-1==user2_choice or (user1_choice-1==-1 and user1_choice+1!=user2_choice):
            stat={
            "message":"You lose.",
            "description":"Better luck next time",
            "color":0xff0000,
        }
        return stat



    return user2,field(user1_choice,user2_choice),game_stat(user1_choice,user2_choice)

