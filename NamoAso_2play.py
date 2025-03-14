print('名もなきあの遊び 2人プレイ')

import random
import threading
import time

def input_with_timeout(prompt, timeout):
    user_input = [None]                                    #入力を保持するリスト
    stop_event = threading.Event()                         #イベントフラグ

    def get_input():                                       #ユーザー入力を処理するスレッド関数
        user_input[0] = input(prompt)
        stop_event.set()                                   #入力が完了したらイベントをセットしてカウントダウンを停止させる

    def countdown(timeout):                                #カウントダウンを処理するスレッド関数
        for t in range(timeout,0,-1):
            if stop_event.is_set():                        #入力が完了したらカウントダウンを終了する
                break
            print(f'残り時間: {str(t).zfill(2)}', end='\r')
            time.sleep(1)
        if not stop_event.is_set():                        #タイムアップした場合
            print('タイムアップ！あなたの負けです')

    input_thread=threading.Thread(target=get_input)        #スレッドの設定
    countdown_thread=threading.Thread(target=countdown, args=(timeout,))

    input_thread.start()                                   #スレッドをスタート
    countdown_thread.start()

    input_thread.join(timeout)                             #指定された秒数だけスレッドの終了を待つ

    if input_thread.is_alive():                            #タイムアウトした場合
        print('タイムアップ！あなたの負けです')
        stop_event.set()                                   #イベントをセットしてカウントダウンを停止
        input_thread.join()                                #スレッドが終了するまで待つ
        return None
    else:
        return user_input[0]

o=random.randint(1,3)                                    #スタートの指の本数を選ぶ
p=random.randint(1,3)
q=random.randint(1,3)
r=random.randint(1,3) 

if o==3 and q==2:
    o=random.randint(1,2)
if o==2 and q==3:
    q=random.randint(1,2)
if o==3 and r==2:
    o=random.randint(1,2)
if o==2 and r==3:
    r=random.randint(1,2)
if p==3 and q==2:
    p=random.randint(1,2)
if p==2 and q==3:
    q=random.randint(1,2)
if p==3 and r==2:
    p=random.randint(1,2)
if p==2 and r==3:
    r=random.randint(1,2)

hand_1 = {'a':1,'b':o,'c':p}                               #手の定義
hand_2 = {'A':1,'B':q,'C':r}

        
print(f'現在のPlayer1の手は{hand_1}')
print(f'現在のPlayer2の手は{hand_2}')

Y = 'A'                                                    #エラーの対処

n = random.randint(0,1)                                    #先攻・後攻をランダムに決める
if n == 0:
    print('Player1が先攻です')
    while hand_1 != {} and hand_2 != {}:
        print('Player1のターン')
        
        x = input_with_timeout('Player1の手を選んでください(a,b,c)',15)
        if x:
            pass
        else:
            print('制限時間を過ぎたので入力は無効です')
            break
        y = input_with_timeout('Player2のどの手に足すか選んでください(A,B,C)',7)
        if y:
            pass
        else:
            print('制限時間を過ぎたので入力は無効です')
            break
        
        while True:                                         #指の本数を足す&文字列のエラー対処
            try:
                hand_2[y] = hand_1[x]+hand_2[y]
            except (KeyError, NameError):
                print('無効な文字列です')
                x = input_with_timeout('もう一度Player1の手を選んでください(a,b,c)',15)
                if x:
                    pass
                else:
                    print('制限時間を過ぎたので入力は無効です')
                    break
                    break
                y = input_with_timeout('もう一度Player2のどの手に足すか選んでください(A,B,C)',7)
                if y:
                    pass
                else:
                    print('制限時間を過ぎたので入力は無効です')
                    break
                    break
            else:
                break

        if hand_2[y] > 4:                                    #5以上のときは5で割った余りに数値を変える
            hand_2[y] = hand_2[y]%5
        if hand_2[y] == 0:                                   #もし手が0になったらその手を削除する
            del hand_2[y]
                
        print(f'現在のPlayer1の手は{hand_1}')
        print(f'現在のPlayer2の手は{hand_2}')
        
        if hand_1 == {}:                                     #勝敗判定
            print('Player2の勝ちです')
            break
        elif hand_2 == {}:
            print('Player1の勝ちです')
            break
        elif len(hand_1) == 1 and len(hand_2) == 1:          #もし無限ループになったら引き分け
            if list(hand_1.values()) == [2] and list(hand_2.values()) == [1]:
                print('引き分けです')
                break
            elif list(hand_1.values()) == [1] and list(hand_2.values()) == [3]:
                print('引き分けです')
                break
            elif list(hand_1.values()) == [4] and list(hand_2.values()) == [2]:
                print('引き分けです')
                break
            elif list(hand_1.values()) == [3] and list(hand_2.values()) == [4]:
                print('引き分けです')
                break
        
        
        while hand_1 != {} and hand_2 != {}:
            print('Player2のターン')
            
            Y = input_with_timeout('Player2の手を選んでください(A,B,C)',15)
            if Y:
                pass
            else:
                print('制限時間を過ぎたので入力は無効です')
                print('制限時間を過ぎたので入力は無効です')
                break
            X = input_with_timeout('Player1のどの手に足すか選んでください(a,b,c)',7)
            if X:
                pass
            else:
                print('制限時間を過ぎたので入力は無効です')
                break
        
            while True:                                         #指の本数を足す&文字列のエラー対処
                try:
                    hand_1[X] = hand_2[Y]+hand_1[X]
                except (KeyError, NameError):
                    print('無効な文字列です')
                    Y = input_with_timeout('もう一度Player2の手を選んでください(a,b,c)',15)
                    if Y:
                        pass
                    else:
                        print('制限時間を過ぎたので入力は無効です')
                        break
                        break
                    X = input_with_timeout('もう一度Player1のどの手に足すか選んでください(A,B,C)',7)
                    if X:
                        pass
                    else:
                        print('制限時間を過ぎたので入力は無効です')
                        break
                        break
                else:
                    break


            if hand_1[X]>4:                                      #5以上のときは5で割った余りに数値を変える
                hand_1[X] = hand_1[X]%5
            if hand_1[X] == 0:                                   #もし手が0になったらその手を削除する
                del hand_1[X]
            print(f'現在のPlayer1の手は{hand_1}')
            print(f'現在のPlayer2の手は{hand_2}')
    
            if hand_1 == {}:                                      #勝敗判定
                print('Player2の勝ちです')
                break
            elif hand_2 == {}:
                print('Player1の勝ちです')
                break
            elif len(hand_1) == 1 and len(hand_2) == 1:           #もし無限ループになったら引き分け
                if list(hand_1.values())==[1] and list(hand_2.values())==[2]:
                    print('引き分けです')
                    break
                elif list(hand_1.values())==[3] and list(hand_2.values())==[1]:
                    print('引き分けです')
                    break
                elif list(hand_1.values())==[2] and list(hand_2.values())==[4]:
                    print('引き分けです')
                    break
                elif list(hand_1.values())==[4] and list(hand_2.values())==[3]:
                    print('引き分けです')
                    break
        
else:
    print('Player2が先攻です')
    while hand_1 != {} and hand_2 != {}:
        print('Player2のターン')
        Y = input_with_timeout('Player2の手を選んでください(A,B,C)',15)
        if Y:
            pass
        else:
            print('制限時間を過ぎたので入力は無効です')
            break
        X = input_with_timeout('Player1のどの手に足すか選んでください(a,b,c)',7)
        if X:
            pass
        else:
            print('制限時間を過ぎたので入力は無効です')
            break
        
        while True:                                         #指の本数を足す&文字列のエラー対処
            try:
                hand_1[X] = hand_2[Y]+hand_1[X]
            except (KeyError, NameError):
                print('無効な文字列です')
                Y = input_with_timeout('もう一度Player2の手を選んでください(a,b,c)',15)
                if Y:
                    pass
                else:
                    print('制限時間を過ぎたので入力は無効です')
                    break
                    break
                X = input_with_timeout('もう一度Player1のどの手に足すか選んでください(A,B,C)',7)
                if X:
                    pass
                else:
                    print('制限時間を過ぎたので入力は無効です')
                    break
                    break
            else:
                break


        if hand_1[X]>4:                                      #5以上のときは5で割った余りに数値を変える
            hand_1[X] = hand_1[X]%5
        if hand_1[X] == 0:                                   #もし手が0になったらその手を削除する
            del hand_1[X]
        print(f'現在のPlayer1の手は{hand_1}')
        print(f'現在のPlayer2の手は{hand_2}')
    
        if hand_1 == {}:                                      #勝敗判定
            print('Player2の勝ちです')
            break
        elif hand_2 == {}:
            print('Player1の勝ちです')
            break
        elif len(hand_1) == 1 and len(hand_2) == 1:           #もし無限ループになったら引き分け
            if list(hand_1.values())==[1] and list(hand_2.values())==[2]:
                print('引き分けです')
                break
            elif list(hand_1.values())==[3] and list(hand_2.values())==[1]:
                print('引き分けです')
                break
            elif list(hand_1.values())==[2] and list(hand_2.values())==[4]:
                print('引き分けです')
                break
            elif list(hand_1.values())==[4] and list(hand_2.values())==[3]:
                print('引き分けです')
                break
        
        
        while hand_1 != {} and hand_2 != {}:
            print('Player1のターン')
        
            x = input_with_timeout('Player1の手を選んでください(a,b,c)',15)
            if x:
                pass
            else:
                print('制限時間を過ぎたので入力は無効です')
                break
            y = input_with_timeout('Player2のどの手に足すか選んでください(A,B,C)',7)
            if y:
                pass
            else:
                print('制限時間を過ぎたので入力は無効です')
                break
        
            while True:                                         #指の本数を足す&文字列のエラー対処
                try:
                    hand_2[y] = hand_1[x]+hand_2[y]
                except (KeyError, NameError):
                    print('無効な文字列です')
                    x = input_with_timeout('もう一度Player1の手を選んでください(a,b,c)',15)
                    if x:
                        pass
                    else:
                        print('制限時間を過ぎたので入力は無効です')
                        break
                        break
                    y = input_with_timeout('もう一度Player2のどの手に足すか選んでください(A,B,C)',7)
                    if y:
                        pass
                    else:
                        print('制限時間を過ぎたので入力は無効です')
                        break
                        break
                else:
                    break

            if hand_2[y] > 4:                                    #5以上のときは5で割った余りに数値を変える
                hand_2[y] = hand_2[y]%5
            if hand_2[y] == 0:                                   #もし手が0になったらその手を削除する
                del hand_2[y]
                
            print(f'現在のPlayer1の手は{hand_1}')
            print(f'現在のPlayer2の手は{hand_2}')
        
            if hand_1 == {}:                                     #勝敗判定
                print('Player2の勝ちです')
                break
            elif hand_2 == {}:
                print('Player1の勝ちです')
                break
            elif len(hand_1) == 1 and len(hand_2) == 1:          #もし無限ループになったら引き分け
                if list(hand_1.values()) == [2] and list(hand_2.values()) == [1]:
                    print('引き分けです')
                    break
                elif list(hand_1.values()) == [1] and list(hand_2.values()) == [3]:
                    print('引き分けです')
                    break
                elif list(hand_1.values()) == [4] and list(hand_2.values()) == [2]:
                    print('引き分けです')
                    break
                elif list(hand_1.values()) == [3] and list(hand_2.values()) == [4]:
                    print('引き分けです')
                    break