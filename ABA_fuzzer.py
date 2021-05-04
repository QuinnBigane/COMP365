import os  
import subprocess
import time

#os.system('echo \"LIN admin\nqbig2222\nqbig2222\nCHP qbig2222\nbigane12\nbigane12\nEXT\"| python3 ABA.py >> test.txt')

random_inputs = ["和製漢語", 
  "部落格", 
  "사회과학원 어학연구소", 
  "찦차를 타고 온 펲시맨과 쑛다리 똠방각하", 
  "社會科學院語學研究所", 
  "울란바토르", 
  "𠜎𠜱𠝹𠱓𠱸𠲖𠳏", 
  "表ポあA鷗ŒéＢ逍Üßªąñ丂㐀𠀀", 
  "Ⱥ", 
  "Ⱦ", 
  "ヽ༼ຈل͜ຈ༽ﾉ ヽ༼ຈل͜ຈ༽ﾉ", 
  "(｡◕ ∀ ◕｡)", 
  "\`ｨ(´∀\`∩", 
  "__ﾛ(,_,*)", 
  "・(￣∀￣)・:*:", 
  "ﾟ･✿ヾ╲(｡◕‿◕｡)╱✿･ﾟ", 
  ",。・:*:・゜’( ☻ ω ☻ )。・:*:・゜’", 
  "(╯°□°）╯︵ ┻━┻)", 
  "┬─┬ノ( º _ ºノ)", 
  "😍", 
  "👩🏽", 
  "👾 🙇 💁 🙅 🙆 🙋 🙎 🙍", 
  "🐵 🙈 🙉 🙊", 
  "❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙", 
  "✋🏿 💪🏿 👐🏿 🙌🏿 👏🏿 🙏🏿", 
  "🚾 🆒 🆓 🆕 🆖 🆗 🆙 🏧", 
  "0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟", 
  "🇺🇸🇷🇺🇸 🇦🇫🇦🇲🇸", 
  "🇺🇸🇷🇺🇸🇦🇫🇦🇲", 
  "🇺🇸🇷🇺🇸🇦", 
  "１２３", 
  "١٢٣", 
  "ثم نفس سقطت وبالتحديد،, جزيرتي باستخدام أن دنو. إذ هنا؟ الستار وتنصيب كان. أهّل ايطاليا، بريطانيا-فرنسا قد أخذ. سليمان، إتفاقية بين ما, يذكر الحدود أي بعد, معاملة بولندا، الإطلاق عل إيو.", 
  "בְּרֵאשִׁית, בָּרָא אֱלֹהִים, אֵת הַשָּׁמַיִם, וְאֵת הָאָרֶץ", 
  "הָיְתָהtestالصفحات التّحول", 
  "﷽", 
  "ﷺ", 
  "مُنَاقَشَةُ سُبُلِ اِسْتِخْدَامِ اللُّغَةِ فِي النُّظُمِ الْقَائِمَةِ وَفِيم يَخُصَّ التَّطْبِيقَاتُ الْحاسُوبِيَّةُ، ", 
  "‪‪test‪", 
  "⁦test⁧", 
  "Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳ ̞̥̱̳̭r̛̗̘e͙p͠r̼̞̻̭̗e̺̠̣͟s̘͇̳͍̝͉e͉̥̯̞̲͚̬͜ǹ̬͎͎̟̖͇̤t͍̬̤͓̼̭͘ͅi̪̱n͠g̴͉ ͏͉ͅc̬̟h͡a̫̻̯͘o̫̟̖͍̙̝͉s̗̦̲.̨̹͈̣", 
  "̡͓̞ͅI̗̘̦͝n͇͇͙v̮̫ok̲̫̙͈i̖͙̭̹̠̞n̡̻̮̣̺g̲͈͙̭͙̬͎ ̰t͔̦h̞̲e̢̤ ͍̬̲͖f̴̘͕̣è͖ẹ̥̩l͖͔͚i͓͚̦͠n͖͍̗͓̳̮g͍ ̨o͚̪͡f̘̣̬ ̖̘͖̟͙̮c҉͔̫͖͓͇͖ͅh̵̤̣͚͔á̗̼͕ͅo̼̣̥s̱͈̺̖̦̻͢.̛̖̞̠̫̰", 
  "̗̺͖̹̯͓Ṯ̤͍̥͇͈h̲́e͏͓̼̗̙̼̣͔ ͇̜̱̠͓͍ͅN͕͠e̗̱z̘̝̜̺͙p̤̺̹͍̯͚e̠̻̠͜r̨̤͍̺̖͔̖̖d̠̟̭̬̝͟i̦͖̩͓͔̤a̠̗̬͉̙n͚͜ ̻̞̰͚ͅh̵͉i̳̞v̢͇ḙ͎͟-҉̭̩̼͔m̤̭̫i͕͇̝̦n̗͙ḍ̟ ̯̲͕͞ǫ̟̯̰̲͙̻̝f ̪̰̰̗̖̭̘͘c̦͍̲̞͍̩̙ḥ͚a̮͎̟̙͜ơ̩̹͎s̤.̝̝ ҉Z̡̖̜͖̰̣͉̜a͖̰͙̬͡l̲̫̳͍̩g̡̟̼̱͚̞̬ͅo̗͜.̟", 
  "̦H̬̤̗̤͝e͜ ̜̥̝̻͍̟́w̕h̖̯͓o̝͙̖͎̱̮ ҉̺̙̞̟͈W̷̼̭a̺̪͍į͈͕̭͙̯̜t̶̼̮s̘͙͖̕ ̠̫̠B̻͍͙͉̳ͅe̵h̵̬͇̫͙i̹͓̳̳̮͎̫̕n͟d̴̪̜̖ ̰͉̩͇͙̲͞ͅT͖̼͓̪͢h͏͓̮̻e̬̝̟ͅ ̤̹̝W͙̞̝͔͇͝ͅa͏͓͔̹̼̣l̴͔̰̤̟͔ḽ̫.͕", 
  "Z̮̞̠͙͔ͅḀ̗̞͈̻̗Ḷ͙͎̯̹̞͓G̻O̭̗̮", 
  "˙ɐnbᴉlɐ ɐuƃɐɯ ǝɹolop ʇǝ ǝɹoqɐl ʇn ʇunpᴉpᴉɔuᴉ ɹodɯǝʇ poɯsnᴉǝ op pǝs 'ʇᴉlǝ ƃuᴉɔsᴉdᴉpɐ ɹnʇǝʇɔǝsuoɔ 'ʇǝɯɐ ʇᴉs ɹolop ɯnsdᴉ ɯǝɹo˥", 
  "00˙Ɩ$-"]

user_commands = ["GER",
    "ADR",
    "EDR",
    "DER",
    "IMD"]

admin_commands = ["DAL",
    "ADU",
    "LSU",
    "DEU"]


#initialize output file
output_file = open("output_file.txt", "w")


"""Fuzz testing of Inital module"""
print("Fuzzing initial module.")

#
#test typing in random inputs with no login session
#
os.system(">test0_actual.txt")
#loop through all random inputs
for random_input in random_inputs:
    os.system('echo "'+random_input+'\nEXT"| python3 ABA.py >> test0_actual.txt')
infile = open("test0_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Unrecognized command\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 0 resulted in a score of:" + str(score) + "\n")
#
#test typing in a real admin command with random input after it
#
os.system(">test1_actual.txt")
#loop through all admin inputs
for admin_command in admin_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "'+admin_command+" "+random_input+'\nEXT"| python3 ABA.py >> test1_actual.txt')
infile = open("test1_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > No active login session\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 1 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real user command with random input after it
#
os.system(">test2_actual.txt")
#loop through all user inputs
for user_command in user_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "'+user_command+" "+random_input+'\nEXT"| python3 ABA.py >> test2_actual.txt')
infile = open("test2_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > No active login session\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 2 resulted in a score of:" + str(score) + "\n")



"""Fuzz testing of admin module"""
print("Fuzzing admin module.")

#first login init
os.system(">test_actual.txt")
os.system('echo "LIN admin\nqbig2222\nqbig2222\nEXT" | python3 ABA.py >> test_actual.txt')
#
# test typing in random inputs with admin login
#
os.system(">test3_actual.txt")
#loop through all random inputs
for random_input in random_inputs:
    os.system('echo "LIN admin\nqbig2222\n'+random_input+'\nEXT"| python3 ABA.py >> test3_actual.txt')
infile = open("test3_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > Unrecognized command\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 3 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real admin command with random input after it
#
os.system(">test4_actual.txt")
#loop through all admin inputs
for admin_command in admin_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        if admin_command == "LSU":
            pass
        else:
            os.system('echo "LIN admin\nqbig2222\n'+admin_command+" "+random_input+'\nEXT"| python3 ABA.py >> test4_actual.txt')
infile = open("test4_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass    
    elif line == "ABA > Invalid userID\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 4 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real user command with random input after it
#
os.system(">test5_actual.txt")
for user_command in user_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN admin\nqbig2222\n'+user_command+" "+random_input+'\nEXT"| python3 ABA.py >> test5_actual.txt')
infile = open("test5_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass    
    elif line == "ABA > Admin not authorized\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 5 resulted in a score of:" + str(score) + "\n")






"""Fuzzing user Module"""
print("Fuzzing user module.")

#first login init
os.system('echo "LIN admin\nqbig2222\nqbig2222\nADU A\nLOU\nLIN A\nqbig2222\nqbig2222\nEXT" | python3 ABA.py >> test_actual.txt')

#
# test typing in random inputs with no login session
#
os.system(">test6_actual.txt")
#loop through all random inputs
for random_input in random_inputs:
    os.system('echo "LIN A\nqbig2222\n'+random_input+'\nEXT"| python3 ABA.py >> test6_actual.txt')
infile = open("test6_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > Unrecognized command\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 6 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real admin command with random input after it
#
os.system(">test7_actual.txt")
#loop through all admin inputs
for admin_command in admin_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN A\nqbig2222\n'+admin_command+" "+random_input+'\nEXT"| python3 ABA.py >> test7_actual.txt')
infile = open("test7_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass    
    elif line == "ABA > Admin not active\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 7 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real user command with random input after it
#
os.system(">test8_actual.txt")
#loop through all user inputs
for user_command in user_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN A\nqbig2222\n'+user_command+" "+random_input+'\nEXT"| python3 ABA.py >> test8_actual.txt')
infile = open("test8_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass    
    elif line == "ABA > Invalid recordID\n":
        pass
    elif line == "ABA > Can’t open Input_file\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 8 resulted in a score of:" + str(score) + "\n")









"""Fuzzing admin module after user logged in"""

print("Fuzzing admin module after user logged in.")
#
# test typing in random inputs with no login session
#
os.system(">test9_actual.txt")
#loop through all random inputs
for random_input in random_inputs:
    os.system('echo "LIN A\nqbig2222\nLOU\nLIN admin\nqbig2222\n'+random_input+'\nEXT"| python3 ABA.py >> test9_actual.txt')
infile = open("test9_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Unrecognized command\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 9 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real admin command with random input after it
#
os.system(">test10_actual.txt")
#loop through all admin inputs
for admin_command in admin_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        if admin_command == "LSU":
            pass
        else:
            os.system('echo "LIN A\nqbig2222\nLOU\nLIN admin\nqbig2222\n'+admin_command+" "+random_input+'\nEXT"| python3 ABA.py >> test10_actual.txt')
infile = open("test10_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Invalid userID\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 10 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real user command with random input after it
#
os.system(">test11_actual.txt")
#loop through all user inputs
for user_command in user_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN A\nqbig2222\nLOU\nLIN admin\nqbig2222\n'+user_command+" "+random_input+'\nEXT"| python3 ABA.py >> test11_actual.txt')
infile = open("test11_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Admin not authorized\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 11 resulted in a score of:" + str(score) + "\n")





"""Fuzzing user module after admin logged in"""
print("Fuzzing user module after admin logged in.")
#
# test typing in random inputs with no login session
#
os.system(">test12_actual.txt")
#loop through all random inputs
for random_input in random_inputs:
    os.system('echo "LIN admin\nqbig2222\nLOU\nLIN A\nqbig2222\n'+random_input+'\nEXT"| python3 ABA.py >> test12_actual.txt')
infile = open("test12_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Unrecognized command\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 12 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real admin command with random input after it
#
os.system(">test13_actual.txt")
#loop through all admin inputs
for admin_command in admin_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN admin\nqbig2222\nLOU\nLIN A\nqbig2222\n'+admin_command+" "+random_input+'\nEXT"| python3 ABA.py >> test13_actual.txt')
infile = open("test13_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
#check all lines of output file, decrement score if not matching
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Admin not active\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 13 resulted in a score of:" + str(score) + "\n")
#
# test typing in a real user command with random input after it
#
os.system(">test14_actual.txt")
#loop through all user inputs
for user_command in user_commands:
    #loop through all random inputs
    for random_input in random_inputs:
        os.system('echo "LIN admin\nqbig2222\nLOU\nLIN A\nqbig2222\n'+user_command+" "+random_input+'\nEXT"| python3 ABA.py >> test14_actual.txt')
infile = open("test14_actual.txt", "r")
lines = infile.readlines()
#add to score for first and last input
score = 2
for line in lines:
    if line == "ABA > Address Book Application, version 1.0. Type “HLP” for a list of commands\n":
        pass
    elif line == "ABA > Enter your password: OK\n":
        pass
    elif line == "ABA > OK\n":
        pass    
    elif line == "ABA > Invalid recordID\n":
        pass
    elif line == "ABA > Can’t open Input_file\n":
        pass
    else:
        score -= 1
infile.close()
output_file.write("test 14 resulted in a score of:" + str(score) + "\n")

output_file.close()
os.remove("test_actual.txt")
os.remove("test0_actual.txt")
os.remove("test1_actual.txt")
os.remove("test2_actual.txt")
os.remove("test3_actual.txt")
os.remove("test4_actual.txt")
os.remove("test5_actual.txt")
os.remove("test6_actual.txt")
os.remove("test7_actual.txt")
os.remove("test8_actual.txt")
os.remove("test9_actual.txt")
os.remove("test10_actual.txt")
os.remove("test11_actual.txt")
os.remove("test12_actual.txt")
os.remove("test13_actual.txt")
os.remove("test14_actual.txt")
