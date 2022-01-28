import random
def directly_draw():
    pool_count = 0
    card_pool = []
    value = 1
    card_pool = [0 for i in range(43)]
    #init card pool
    for i in range(3):
        card_pool.append(1)
        card_pool.append(2)
        card_pool.append(3)
        card_pool.append(4)
        card_pool.append(6)
        card_pool.append(7)
        card_pool.append(8)
        card_pool.append(9)
    card_pool.append(1)
    card_pool.append(4)
    card_pool.append(6)
    card_pool.append(9)
    card_pool.append(10)

    random.shuffle(card_pool)
    method1_count = 0
    method1_key = 0
    #method1:directly draw

    while(1):
        draw = card_pool[0]
        #print("draw =",draw)
        method1_count += 1
        if(draw == 1 or draw == 4 or draw == 6 or draw ==9):
            break
        elif(draw == 2 or draw == 3 or draw == 7 or draw == 8 or draw == 10):
            #2.5 pairs
            if(method1_key == 0):
                method1_key = draw
                card_pool.pop(0)
            #judge if bingo
            else:
                #finish 2.5 pairs for bingo
                if((draw == method1_key or draw == 10) and method1_key != 10):
                    break
                #finish 4-holes for bingo
                elif(method1_key == 10 and (draw == 2 or draw ==3 or draw == 7 or draw
                    == 8)):
                    break
                else:
                    card_pool.pop(0)
        else:
            card_pool.pop(0)
    #print("method1 count =",method1_count)
    return method1_count

def pon_then_draw():
    pool_count = 0
    card_pool = []
    value = 1
    #init card pool
    card_pool = [0 for i in range(42)]
    for i in range(3):
        card_pool.append(1)
        card_pool.append(2)
        card_pool.append(3)
        card_pool.append(4)
        card_pool.append(6)
        card_pool.append(7)
        card_pool.append(8)
        card_pool.append(9)
    card_pool.append(1)
    card_pool.append(4)
    card_pool.append(6)
    card_pool.append(9)
    random.shuffle(card_pool)
    method2_count = 0
    #method2:pon then draw
    while(1):
        draw = card_pool[0]
        #print("draw =",draw)
        method2_count += 1
        if(draw == 1 or draw == 2 or draw == 3 or draw == 4 or draw == 6 or draw
                == 7 or draw ==8 or draw == 9):
            break
        else:
            card_pool.pop(0)
    return method2_count+1

method1_sum_draw = 0
method2_sum_draw = 0

test_time = 100000
for i in range(test_time):
    method1_sum_draw += directly_draw()
    method2_sum_draw += pon_then_draw()

print("test times: ",test_time)
print("method1 average draw:",method1_sum_draw/test_time)
print("method2 average draw:",method2_sum_draw/test_time)
