#!/usr/bin/python
import time
import numpy as np
import random
import os
from copy import deepcopy

CARD_KIND_NUM = 4
CARD_NUM = 4
WORD_NUM = 7
NUMBER_NUM = 9
WORD_INDEX = 0
KIND_OFFSET = 6
MAX_HAND = 17

mj_dict = {0:'E',1:'S',2:'W',3:'N',4:'M',5:'F',6:'B',7:'w',8:'b',9:'s'}


EMPTY_2D_HAND = [[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]


def get_eyes_list(hand):
    eyes_list = []
    for kind in range(CARD_KIND_NUM):
        for card_index in range(len(hand[kind])):
            card_num = hand[kind][card_index]
            if (kind == 0):
                if(card_num == 2):
                    eyes_list.append([kind, card_index])
            else:
                if(card_num >= 2):
                    eyes_list.append([kind, card_index])
    return eyes_list

def bingo_check(hand):
    eyes_list = get_eyes_list(hand)
    if (len(eyes_list) == 0):
        return -1
    else:
        for valid_eyes in range(len(eyes_list)):
            cp_hand = deepcopy(hand)
            eyes_kind = eyes_list[valid_eyes][0]
            eyes_index = eyes_list[valid_eyes][1]
            cp_hand[eyes_kind][eyes_index] -= 2
            fail_flag = 0
            for kind in range(CARD_KIND_NUM):
                if(fail_flag == 1):
                    break
                for card_index in range(len(cp_hand[kind])):
                    card_num = cp_hand[kind][card_index]
                    if (kind == WORD_INDEX):
                        if (card_num == 1 or card_num == 2 or card_num == 4):
                            return -1
                        elif (card_num == 3):
                            cp_hand[kind][card_index] -= 3
                    else:
                        if (card_num == 4 and card_index <= 6):
                            cp_hand[kind][card_index] -= 4
                            cp_hand[kind][card_index + 1] -= 1
                            cp_hand[kind][card_index + 2] -= 1
                        elif (card_num == 3):
                            cp_hand[kind][card_index] -= 3
                        elif (card_num > 0 and card_index <= 6):
                            cp_hand[kind][card_index] -= card_num
                            cp_hand[kind][card_index + 1] -= card_num
                            cp_hand[kind][card_index + 2] -= card_num
                        elif (card_num < 0):
                            fail_flag = 1
                            break
            if (np.any(cp_hand[1:]) == 0):
                return 0
    return -1

def list_bingo_card(hand):
    cp_hand = deepcopy(hand)
    bingo_list = []
    for kind in range(CARD_KIND_NUM):
        if (kind == WORD_INDEX):
            for card_index in range(WORD_NUM):
                cp_hand[kind][card_index] += 1
                if (bingo_check(cp_hand) == 0):
                    bingo_list.append([kind, card_index])
                cp_hand[kind][card_index] -= 1
        else:
            for card_index in range(NUMBER_NUM):
                cp_hand[kind][card_index] += 1
                if(bingo_check(cp_hand)==0):
                    bingo_list.append([kind, card_index])
                cp_hand[kind][card_index] -= 1
    return bingo_list

def get_view_hand(hand):
    cp_hand = deepcopy(hand)
    view_hand = [[] for kind in range(CARD_KIND_NUM)]
    for kind in range(len(cp_hand)):
        for card_index in range(len(cp_hand[kind])):
            card_num = cp_hand[kind][card_index]
            if (kind == 0 and card_num > 0):
                for card in range(card_num):
                    card_name = mj_dict[card_index]
                    view_hand[kind].append(card_name)
            elif (kind > 0 and card_num > 0):
                for card in range(card_num):
                    card_name = str(card_index + 1) + mj_dict[kind + KIND_OFFSET]
                    view_hand[kind].append(card_name)
    return view_hand

def create_shuffled_pool():
    card_pool = []
    for kind in range(CARD_KIND_NUM):
        if (kind == 0):
            for card_index in range(WORD_NUM):
                for card_num in range(CARD_NUM):
                    card_pool.append(mj_dict[card_index])
        else:
            for card_index in range(NUMBER_NUM):
                for card_num in range(CARD_NUM):
                    card_name = str(card_index + 1) + mj_dict[kind + KIND_OFFSET]
                    card_pool.append(card_name)
    random.shuffle(card_pool)
    return card_pool

def draw(pool):
    card_val = pool[0]
    pool.pop(0)
    return card_val

def init_hand(pool):
    hand = pool[0:16]
    del pool[0:16]
    return hand

def hand_dimension_1to2(view_hand):
    hand = deepcopy(EMPTY_2D_HAND)
    val_list = list(mj_dict.values())
    for card in view_hand:
        if (len(card) == 1):
            position = val_list.index(card)
            hand[0][position] += 1
        else:
            card_index = int(card[0]) - 1
            position = val_list.index(card[1]) - 6
            hand[position][card_index] += 1
    return hand

def start_game():
    while True:
        print("Shuffles the cards...")
        card_pool = create_shuffled_pool()
        raw_hand = init_hand(card_pool)
        drawn_card = draw(card_pool)
        draw_count = 1
        cal_hand = hand_dimension_1to2(raw_hand)
        view_hand = get_view_hand(cal_hand)
        print("Your hand:",view_hand)
        print("You have drawn:",drawn_card)
        raw_hand.append(drawn_card)
        cal_hand = hand_dimension_1to2(raw_hand)
        while (bingo_check(cal_hand) != 0):
            while True:
                    print("Which card to play?")
                    card_to_play = input()
                    if (card_to_play in raw_hand):
                        raw_hand.remove(card_to_play)
                        break
                    else:
                        print("You don't have this card")
            drawn_card = draw(card_pool)
            draw_count += 1
            cal_hand = hand_dimension_1to2(raw_hand)
            view_hand = get_view_hand(cal_hand)
            print("Your hand:", view_hand)
            print("You have drawn:", drawn_card)
            raw_hand.append(drawn_card)
            cal_hand = hand_dimension_1to2(raw_hand)
        print("Bingooo! with:", drawn_card)
        print("You have drawn",draw_count,"cards to win")
        print("Play again? Y/N")
        confirm = input()
        while(confirm != 'Y' and confirm != 'N'):
                print("Invalid input")
                confirm = input()
        if (confirm == 'N'):
                exit()
        elif (confirm =='Y'):
                continue

if __name__ == '__main__':
    start_game()













