# The script of the game goes in this file.
# Declare characters used by this game. The color argument colorizes the
# name of the character.

# The game starts here.

label start:
    define health = 4
    define hunger = 3
    define sword = 0
    define lantern = 0
    define lanternLit = 0
    define bread =  0
    define breadFind = 0
    define goblinExit = 1
    define goblinGuard = 1
    define rescueIncoming = 0
    define visibleTrap = 0

    transform topright: 
        xalign 1.0
        yalign 0.0
    transform topleft:
        xalign 0.0
        yalign 0.0
    transform midright:
        xalign 1.0
        yalign 0.5
    transform mid:
        xalign 0.5
        yalign 0.5
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.
    play sound "falling.mp3"
    queue sound "impact.mp3"
    pause 5.5
    play music "dungeon ambiance.mp3"

    # These display lines of dialogue.

    "{cps=0}You've fallen into a dungeon."

    "A corpse softened your fall. You silently thanks the dead adventurer."

    "You were seperated from your group and fell down. For now, the best course of action is to think."

    "It seems safe here. You could wait here... or have this your return spot."
    label hub:
        scene spawn
        if hunger <= 0 or health <= 0:
            jump PerishEnd
        
        if lantern == 1:
            if lanternLit == 1:
                show litlantern at topright
                hide lantern
            else: 
                show lantern at topright
                hide litlantern

        if sword == 1:
            show arming at midright

        if bread > 0:
            show moldybread at topleft
        
        if rescueIncoming == 4:
            play sound "pulley.mp3"
            "..."
            "There's an obnoxiously loud sound coming from the hole you came from."
            "Wait... that's a rope coming down! Your group finally came to your rescue!"
            "You COULD take the rope now... but you don't have to."
        
        if sword == 0:
            "On your left, you see light. To your right, darkness. Up ahead, a glint of something. Or, you could wait. What do you do now?"
        else: 
            "On your left, you see light. To your right, darkness. Up ahead, a few moving shadows. Or, you could wait. What do you do now?"

        menu: 
            "Go left":
                jump go_left

            "Go right":
                jump go_right

            "Go forward":
                jump go_forward

            "Wait":
                "You rest for a bit while waiting."
                "An unnatural hunger sets in..."
                "You feel.. hungrier."
                $ hunger = hunger - 1
                $ rescueIncoming = rescueIncoming + 1
                if health < 5:
                    "In exchange, it seems your recovery is boosted."
                    $ health = health + 1
                jump hub

            "Self Check":
                jump selfCheck

            "Eat the bread" if bread >= 1:
                "You hope it's still edible..."
                $ renpy.movie_cutscene("eating.webm")
                $ bread = bread - 1
                "Seems like it was."
                $ hunger = hunger + 2
                if hunger > 3:
                    $ hunger = 3
                jump hub

            "Light Lantern" if lantern == 1 and lanternLit == 0:
                call lanternLighting from _call_lanternLighting
                jump hub
        
            "Snuff out Lantern" if lantern == 1 and lanternLit == 1:
                $ lanternLit = 0
                "You snuff out your lantern's flame."
                jump hub

            "Climb the rope" if rescueIncoming >= 4:
                jump RescueEnd

    label go_left: 
        "You decide to go left."
        scene lantern on ground
        if lantern == 0:
            "There is a lantern on the ground underneath a torch. Whoever owned it probably doesn't need it anymore. Take it?"
            menu: 
                "Yes":
                    $ lantern = 1
                    "You take the unlit lantern with you."
                
                "No":
                    "You decide it's better not touching it. For now."
        else:
            "There is a torch here."

        if lantern == 1 and lanternLit == 0:
            "Light the lantern with the torch?"
            menu:
                "Yes":
                    call lanternLighting from _call_lanternLighting_1
            
                "No":
                    "You decide it's better not to light it right now."

        "You could go a little further. Should you?"
        menu:
            "Yes":
                if lanternLit == 1:
                    "You look for something useful, your lantern lighting the way..." 
                else:
                    "You explore further, hoping to find something useful..."
                jump encounter
            
            "No":
                "You decide it's better not to go too far right now. You head back."
                jump hub

    label go_forward:
        if sword == 0:
            "Trudging ahead, you become wary of what moves in the shadows. Is this really a good idea?"
            "... Anything could jump at you right about now."
            "And you wouldn't be able to do anything."
            "..."
            "You spot something shining in the corner of your eye."
            "You tiptoe to the place, the glimmer of metal guiding you."
            scene sword on ground
            "Your eyes did not decieve you."
            "In this cave of darkness, you found a glimmer of hope."
            "You found..."
            "A sword."
            show arming at mid
            "With this, you can at least defend yourself."
            "You holster it in your belt, steeling yourself for what else to come."
            hide arming
            $ sword = 1
            jump hub
        else:
            "There isn't anything else here. Furthermore, lurking here isn't a good idea."
            "They might get you."
            jump hub

    label lanternLighting:
        $ lanternLit = 1
        "You light the lantern. It's a bit easier to see now. But it's also easier to see you."
        return
    
    label encounter:
        $ exploration = renpy.random.randint(1, 10)
        if lanternLit == 1:
            $ exploration = exploration + 2
        
        if exploration >= 8:
            "You encounter a goblin!"
            if exploration == 10:
                "It becomes hostile! It attacks you!"
                if lanternLit == 1:
                    $ renpy.movie_cutscene("blocking hit.webm")
                    "Luckily, you were able to defend because you saw it wind up!"
                    $ health = health - 1
                else:
                    $ renpy.movie_cutscene("getting hit.webm")
                    $ health = health - 2
                "You fall back before it can do any more harm to you."
                jump hub
            else: 
                "It hasn't spotted you yet... What do you do?"
                menu:
                    "Fight it" if sword == 1:
                        $ renpy.movie_cutscene("trading hits.webm")
                        "You fight it off, but it wasn't pretty. You took some damage."
                        $ health = health - 2
                        show moldybread at mid
                        "Seems like it dropped some bread. You take it back with you."
                        hide moldybread
                        $ bread = bread + 1
                        jump hub
                    
                    "Ambush it" if sword == 1 and lanternLit == 0:
                        $ ambush = renpy.random.randint(1, 3)
                        if ambush < 3:
                            $ renpy.movie_cutscene("ambush.webm")
                            "You manage to kill it quickly."
                            show moldybread mid
                            "Seems like it dropped some bread. You take it back with you."
                            hide moldybread mid
                            $ bread = bread + 1
                            jump hub
                        else: 
                            $ renpy.movie_cutscene("trading hits.webm")
                            "You kill it before it severely damaged you. It still hit you, though."
                            $ health = health - 1
                            show moldybread at mid
                            "Seems like it dropped some bread. You take it back with you."
                            hide moldybread
                            $ bread = bread + 1
                            jump hub

                    "Back off":
                        $ retreat = renpy.random.randint(1, 10)
                        if lanternLit == 1:
                            $ retreat = retreat + 2
                            if sword == 1:
                                $ retreat = retreat + 1
    
                        if retreat < 7:
                            "You get away safely..."
                            jump hub

                        else: 
                            "It spots you and attacks!"
                            $ renpy.movie_cutscene("getting hit.webm")
                            $ health = health - 2
                            "You fall back before it can do any more harm to you."
                            jump hub
                    "Offer it Food" if bread >= 1:
                        "You attempt to give it some bread."
                        $ bread = bread - 1
                        $ negotiate = renpy.random.randint(1,2)
                        if negotiate == 1:
                            "It takes the bread and leaves you alone."
                            jump hub
                        else: 
                            "It knocks the bread out your hands and attacks!"
                            $ health = health - 2
                            "You run back to your safe place, injured."
                            jump hub


        elif exploration >= 3:
            if breadFind <=3:
                $ bread = bread + 1
                scene bread on ground
                "You find some bread on the ground."
                show moldybread at mid
                "... Is this safe to eat?"
                "You wonder about the safety of eating moldy bread. You then realize you don't have many options."
                hide moldybread
                $ breadFind = breadFind + 1
                jump hub
                
            else: 
                "You don't find anything. Maybe it's time to leave..."
                jump hub
        
        else: 
            "You don't find anything. You head back."
            jump hub
    
    label selfCheck:
        "You focus and observe your body. You feel..."
        if health == 5:
            "Absolutely fine. No injuries."
        elif health == 4:
            "Lightly wounded. It doesn't bother you much, but it still a pain."
        elif health == 3:
            "Injured. It's not wise to go exploring in this state, but it's not like you have much choice."
        elif health == 2:
            "Heavily injured. You're holding on, but barely. You won't let it end like this, after all."
        else:
            "Like you're at the brink of death. A fly could bite you and you would die."
            "Be VERY careful."
        if hunger == 3:
            "And also, there's a slight rumble in your tummy. It's always like that, but you feel like in here, it's different."  
        elif hunger == 2:
            "And also, hungry. If left unchecked, you're going to starve soon"   
        else: 
            "And also, you are starving. You need to eat something NOW."
        jump hub
    
    label PerishEnd:
        scene black
        "Hmm?"
        "."
        ".."
        "..."
        "... What happened?"
        scene perish
        "Why are you..."
        "Ahh..."
        "Sorry to say, you're dying."
        "Looks like your luck ran out."
        "Maybe, your body will save the next person who falls here."
        return
    
    label RescueEnd:
        play sound "rope.mp3"
        scene rescueending
        "You give the rope a tug, signalling to your team that you've grabbed the rope."
        "You hold on tight, making sure not to fall while they pull you up."
        play sound "pulley.mp3"
        "Slowly, you ascend back through the hole you fell through."
        "You can hear your team conversing now, just a little more and you'll see them again."
        "{cps=6}Finally, {w=0.6}you can smell the fresh{/cps}{nw}" 
        scene black
        play sound "impact.mp3"
        "{w=3.0}The rope snapped."
        "Not because you were heavy."
        "Not because it was weak."
        "But because there was something strong."
        "Stronger than an entire army."
        "And it was hungry."
        "And it saw you."
        return

    label go_right:
        scene unseen trap
        "It's dark around here. You could push on, but it would be better if you had a light source."
        if lanternLit == 1 and visibleTrap == 0:
            "Good thing you do."      
        elif visibleTrap == 1:
            "Good thing you already know where the trap is."
            scene lantern trap and goblin
        menu:
            "Push ahead":
                "You move toward the visible door."
                if visibleTrap == 1:
                    jump nearEscape
                "OUCH! You stepped on a trap."
                $ health = health - 2
                if health <= 0:
                    jump PerishEnd
                "But well, you're still standing. Too bad you don't know where the trap is."
                jump nearEscape

            "Throw lantern" if lanternLit == 1 and visibleTrap == 0:
                $ visibleTrap = 1
                "You throw the lantern in front of you, and it triggers a trap!"
                scene lantern trap and goblin
                "Good thing you didn't step in it."
                "The light also reveals a goblin, but he seems to be holding something else."
                jump go_right

            "Attack the Goblin" if visibleTrap == 1 and sword == 1 and goblinGuard == 1:
                "Goblin" "My, how uncivilized. It seems we will be unable to converse after all. I had high hopes in you."
                $ renpy.movie_cutscene("trading hits.webm")
                $ health = health - 3
                "The goblin was insanely strong. It was a bolaslinger, and you kept getting tripped up."
                "Eventually, you win through pure physical difference."
                $ goblinGuard = 0
                jump go_right

            "Talk to the Goblin" if visibleTrap == 1 and goblinGuard == 1:
                "Goblin" "Ah, finally. A civil one. It has been so long since I've interacted with one like you."
                "This goblin is suspicously well spoken."
                "Goblin" "I know I am suspicously well spoken, but this is simply how I was born."
                "Goblin" "Tell you what, if you offer me some food, I'll tell you something good."
                "Give the goblin food?"
                menu:
                    "Yeah, why not" if bread >= 1:
                        $ bread = bread - 1
                        "Goblin" "Don't trust everything in the dungeon. The light that shows you the way can very easily show others the way to you."
                    "No thanks":
                        "Goblin" "Well, alright."
                jump go_right

            "Back off":
                "You decide to go back to your safe place."
                jump hub
    label nearEscape:
        scene goblin next to escape
        if goblinExit == 1:  
            "A Goblin is visible on the other side of the room. It looks dangerous."
            if lanternLit == 1:
                "It spots you and attacks right away! It's strong!"
                $ renpy.movie_cutscene("getting hit.webm")
                $ health == health - 4
                if health <= 0:
                    jump PerishEnd
                if sword == 1:
                    "You fight with all your might, taking him down before you fall."
                    $ renpy.movie_cutscene("trading hits.webm")
                    "If it weren't for you being unscathed, you doubt you would have made it out alive."
                    $ goblinExit = goblinExit - 1 
                    jump nearEscape
                else:
                    "You run back to your safe place, at the brink of death."
                    jump hub
            else: 
                "It hasn't spotted you yet. What do you do?"
                menu:
                    "Fight it" if sword == 1:
                        "The goblin is stronger than all the goblins you've faced. Your only advantage is you caught it by surprise."
                        $ renpy.movie_cutscene("trading hits.webm")
                        $ health = health - 3
                        if health <= 0:
                            jump PerishEnd
                        $ goblinExit = goblinExit - 1
                        jump nearEscape

                    "Talk to it":
                        "It doesn't want to."
                        "It turns hostile and attacks you."
                        $ health = health - 4
                        if health <= 0:
                            jump PerishEnd
                        "You run back to your safe place before it kills you."
                        jump hub

                    "Back off":
                        "You fall back to the room you were just in."
                        jump go_right
                    
        elif lanternLit == 1:
            "Wait, this wasn't here before, was it?"
            scene escapeending
            "These are a set of stairs leading out! You hit the jackpot!"  
            "Well.. Assuming they don't collapse on you on your way out."
            "Climb the stairs?"
            menu: 
                "Yes":
                    "You climb the stairs."
                    "The creaking and dripping of the dungeon doesn't help your nerves."
                    "Your footsteps echo throughout the stairway. They seem to extend forever."
                    "And ever."
                    "And ever.."
                    "And ever..."
                    "But like all things, it comes to an end."
                    "And here, your adventure ends."
                    "As you emerge from the ground, your team rushes to you, asking if you're alright."
                    "The sight of sunlight almost blinds you."
                    "Ahh, it's good to be back."
                    return
                "No":
                    "You decide not to climb the stairs right now."
                    "You head back to the room you were in."
                    jump go_right
        else:
            "A dark room. A dead goblin. There isn't much else to see here."
            "You go back to the room you were just in."
            jump go_right



    # This ends the game.

    return
