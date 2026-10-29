import win32api, os, time, msvcrt, subprocess
from background import opnum

def append_answer(prob_list, num:int):
    return f'{prob_list[num]} ({num+1})'

def sort_dict(dictionary: dict, keyOrValue):
    sortedDict = {}
    if keyOrValue == 'key':
        loc = 0
    elif keyOrValue == 'value':
        loc = 1
    sortedTuple =  sorted(dictionary.items(), key = lambda i:str(i[loc]))
    for i in sortedTuple:
        sortedDict[i[0]] = i[1]
    return sortedDict

def sort_multiple_answer(multiple_answer_list):
    temp_dict = {}
    temp_list = []
    for i in multiple_answer_list[1:]:#because of the True at the start of any list
        temp_dict[i] = int(i[3]) #because this is the number
    return_dict = sort_dict(temp_dict, 'value')
    for i in return_dict:
        temp_list.append(i)
    return temp_list

def show_multiple_answer(multiple_answer_list):
    return_str = ''
    for i in multiple_answer_list:
        return_str += i
        if i == multiple_answer_list[len(multiple_answer_list)-1]:
            pass
        else:
            return_str += ', '
    return return_str

def change_start_point():
    #flush all the shit
    while msvcrt.kbhit():
        msvcrt.getwch()

    while True:
        print('何問目から始めますか')
        question = input('>> ')
        if opnum.is_int(question) == True:
            return int(question)
        print('\033[31m入力が間違っています\033[37m')

class log:
    def __init__(self):
        self.prob_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self.answer_list = []
        self.multiple_answer = []
        self.removed_answer = None
        self.start_point = 1
        self.questionaire_start = None
        self.temp_subtract_questionaire_num = 0
        self.past_subtract_questionaire_num = 0
        self.multiple_questionaire_start = []
        self.multiple_questionaire_end = []

    def show_screen(self):
        subprocess.run("cls", shell=True)
        #print(f'{self.answer_list=}')
        #print(f'{self.removed_answer=}')
        #print(f'{self.multiple_answer=}')
        #print(f'{self.questionaire_start=}')
        #print(f'{self.multiple_questionaire_start=}')
        #print(f'{self.multiple_questionaire_end=}')
        #print(f'{self.temp_subtract_questionaire_num=}')
        #print(f'{self.past_subtract_questionaire_num=}')

        highlight_answer = []

        if self.removed_answer == None:
            pass
        elif type(self.removed_answer) != list:
            highlight_answer.append(self.removed_answer)
        else:
            [self.multiple_answer.append(i) for i in self.removed_answer]

        if len(self.multiple_answer) != 0:
            [highlight_answer.append(i) for i in self.multiple_answer]

        print(f'{(len(self.answer_list) + self.start_point) - self.temp_subtract_questionaire_num - self.past_subtract_questionaire_num}', end='')
        
        if self.questionaire_start != None:
            print(f'-{self.temp_subtract_questionaire_num + 1}', end='')
        print('問目：', end='')
        if  len(self.multiple_answer) != 0:
            print(f'\033[36m連続回答\033[37m')
        else:
            print('')
        for ilen, i in enumerate(self.prob_list):
            if len(highlight_answer) == 0:
                pass
            elif f'{i} ({ilen+1})' in highlight_answer:
                print('\033[32m', end='')
            print(f'{i}: ({ilen+1})', '\033[37m')


    def main(self):
        chang = True
        base_key = 0x60
        while True:
            settings = win32api.GetKeyState(0x10) #shift
            if settings < 0:
                self.start_point = change_start_point()
                chang = True

            continuous = win32api.GetKeyState(0x6B) #テンキー+

            if continuous >= 0:
                pass
            elif len(self.multiple_answer) == 0:
                self.multiple_answer.append('True')
                chang = True
            elif len(self.multiple_answer) == 1: #Trueしか入ってない
                self.multiple_answer = []
                chang = True
            else:
                self.answer_list.append(self.multiple_answer)
                chang = True

            if continuous >= 0:
                pass
            elif len(self.multiple_answer) <= 1: #if there is content in the multiple answer
                pass
            elif self.questionaire_start == None:
                self.multiple_answer = [] #i put this shit here because if i don't put it here, and i delete everything in multiple answer while in the continuing questionaire, it would not know to subtract one from the visual questionaire number cause of elif len(self.multiple_answer) <= 1: this part it would just assume that there is nothing in the multiple questioaire therefore is not answered and would not work as planned
            elif len(self.answer_list) == self.questionaire_start:
                self.multiple_answer = []
            else:
                self.multiple_answer = []
                self.temp_subtract_questionaire_num += 1



            continue_questionaire = win32api.GetKeyState(0x6D) #テンキー-
            if continue_questionaire >= 0:
                pass
            elif self.questionaire_start == None:
                self.questionaire_start = len(self.answer_list)
                chang = True
            elif len(self.answer_list) == self.questionaire_start:
                subtract_questionaire_num = 0
                self.questionaire_start = None
                chang = True
            else:
                self.multiple_questionaire_start.append(self.questionaire_start)
                self.multiple_questionaire_end.append(len(self.answer_list)-1)
                self.questionaire_start = None
                self.past_subtract_questionaire_num += self.temp_subtract_questionaire_num -1 #-1 because i want this to go to the next question
                self.temp_subtract_questionaire_num = 0
                chang = True

            for key_code, alphabet in enumerate(self.prob_list):
                is_pressed = win32api.GetKeyState(base_key + (key_code+1))
                if is_pressed >= 0:
                    pass
                elif len(self.multiple_answer) == 0:
                    self.answer_list.append(append_answer(self.prob_list, key_code))
                    chang = True
                elif not f'{alphabet} ({key_code+1})' in self.multiple_answer:
                    self.multiple_answer.append(append_answer(self.prob_list, key_code))
                    chang = True

                if is_pressed >= 0:
                    pass
                elif self.questionaire_start == None:
                    pass
                elif len(self.answer_list) == self.questionaire_start:
                    pass
                elif len(self.multiple_answer) != 0:
                    pass
                else:
                     self.temp_subtract_questionaire_num += 1

            
            end_study = win32api.GetKeyState(0x6E) #テンキー .
            if end_study < 0:
                self.end()
                self.end_screen()
            
            go_back = win32api.GetKeyState(0x08)
            reset_questionaire_len = False
            if not go_back < 0:
                pass
            elif self.questionaire_start == None:
                pass
            elif len(self.multiple_answer) != 0: #if there is multiple answer, i dont need to subtract anything its still the same answer
                pass
            elif self.temp_subtract_questionaire_num > 0: #if there is something i subtracted in this questionaire, we would delete it
                self.temp_subtract_questionaire_num -= 1
            elif self.temp_subtract_questionaire_num == 0: #if there is nothing in here just subtract everything
                self.questionaire_start = None
                reset_questionaire_len = True

            if not go_back < 0:
                pass
            elif len(self.answer_list)-1 in self.multiple_questionaire_end:
                expired_index = self.multiple_questionaire_end.index(len(self.answer_list)-1)
                self.temp_subtract_questionaire_num = self.multiple_questionaire_end[expired_index] - self.multiple_questionaire_start[expired_index]
                self.past_subtract_questionaire_num -= self.temp_subtract_questionaire_num
                self.questionaire_start = self.multiple_questionaire_start[expired_index]
                self.multiple_questionaire_start.pop(expired_index)
                self.multiple_questionaire_end.pop(expired_index)

            if not go_back < 0:
                pass
            elif reset_questionaire_len == True:
                reset_questionaire_len = False #this is so that when 3-1 is the number, it would go back to 3 and not 2
                chang = True
            elif len(self.multiple_answer) != 0: #[0]はTrueだからね
                self.multiple_answer.pop(len(self.multiple_answer)-1)
                chang = True
            elif len(self.answer_list) != 0:
                self.removed_answer = self.answer_list[len(self.answer_list)-1]
                self.answer_list.pop(len(self.answer_list)-1)
                chang = True


            if chang == True:
                self.show_screen()
                self.removed_answer = None
                chang = False
                time.sleep(0.2)

    def end(self):
        remove_num = 1
        self.temp_questionaire_start = self.multiple_questionaire_start.copy()
        self.temp_questionaire_end = self.multiple_questionaire_end.copy()

        if len(self.multiple_answer) <= 1:
            pass
        elif self.questionaire_start != None:
            self.temp_subtract_questionaire_num += 1 #bc im going t add something to the answer_list (as seen below) 
            

        if len(self.multiple_answer) > 1: #so that multiple answer is not just [True]
            self.answer_list.append(self.multiple_answer)
            self.multiple_answer = []
            remove_num = 0
        elif len(self.multiple_answer) == 1:
            self.multiple_answer = ['True']
        else:
            self.multiple_answer = []


        if self.questionaire_start == None:
            pass
        elif len(self.answer_list) != self.questionaire_start:
            self.temp_questionaire_start.append(self.questionaire_start)
            self.temp_questionaire_end.append(len(self.answer_list)-1)

    def end_screen(self):
        temp_result_questionaire_subtract = 0
        past_result_questionaire_subtract = 0

        subprocess.run("cls", shell=True)
        #print(self.multiple_questionaire_start)
        print('結果発表：')
        same_questionaire_bool = False
        for ilen, i in enumerate(self.answer_list):
            print(f'{ilen+self.start_point-temp_result_questionaire_subtract-past_result_questionaire_subtract}', end='')
            if ilen in self.temp_questionaire_start:
                same_questionaire_bool = True

            if same_questionaire_bool == True:
                temp_result_questionaire_subtract += 1
                print(f'-{temp_result_questionaire_subtract}', end='')

            if ilen in self.temp_questionaire_end:
                past_result_questionaire_subtract += temp_result_questionaire_subtract -1 #to start new one, subtract one
                temp_result_questionaire_subtract = 0
                same_questionaire_bool = False
            print('問目: ', end='')
            
            if type(i) != list:
                print(i)
            else:
                answer = sort_multiple_answer(i)
                print(show_multiple_answer(answer))

        time.sleep(0.2)
        while True:
            start_study = win32api.GetKeyState(0x6E) #テンキー .
            if start_study < 0:
                self.show_screen()
                time.sleep(0.2)
                break
        self.main()


log_test = log()
log_test.main()