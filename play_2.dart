// game_page.dart
import 'package:flutter/material.dart';

class Namoaso_2 extends StatefulWidget {
  @override
  State<Namoaso_2> createState() => Namoaso_2_screen();
}


class Namoaso_2_screen extends State<Namoaso_2> {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/background_pink.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: [

            // 下段（自分の手）
            Align(
              alignment: Alignment(0, 0.9),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                  Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                  Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                ],
              ),
            ),

            // 残り時間
            Align(
              alignment: Alignment(-0.82,0.85),
              child: Text(
                '15',
                style: TextStyle(
                  fontSize: screenHeight * 0.1,
                  fontWeight: FontWeight.w100,
                  color: const Color.fromARGB(255, 125, 125, 125),
                  fontFamily: 'font',
                ),
              ),
            ),

            // Homeボタン
            Align(
              alignment: Alignment(0.85,0.3),
              child: GestureDetector(
                onTap: () {
                  Navigator.pop(context); // 戻る
                },
                child: Image.asset(
                  'assets/home.png', // ← ホームボタン画像（差し替え可）
                  height: screenHeight * 0.2,
                ),
              ),             
            ),
          
            
            // この手で決定ボタン
            Align(
              alignment: Alignment(-0.93,0.3),
              child: GestureDetector(
                onTap: () {
                  print("次へボタンが押されました"); // 戻る
                },
                child: Image.asset(
                  'assets/next_turn.png', 
                  height: screenHeight * 0.2,
                ),
              ),
            ),

            // ターン表示
            Align(
              alignment: Alignment(0.93,0.8),
              child: Text(
                'あなたのターン',
                style: TextStyle(
                  fontSize: screenHeight * 0.05,
                  fontWeight: FontWeight.w100,
                  color: const Color.fromARGB(255, 125, 125, 125),
                  fontFamily: 'font',
                ),
              ),
            ),
            
            
            // 上段（相手の手）
            Align(
              alignment: Alignment(0, -0.9),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Transform(
                    alignment: Alignment.center,
                    transform: Matrix4.identity()..scale(-1.0, -1.0),
                    child: Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                  ),
                  Transform(
                    alignment: Alignment.center,
                    transform: Matrix4.identity()..scale(-1.0, -1.0),
                    child: Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                  ),
                  Transform(
                    alignment: Alignment.center,
                    transform: Matrix4.identity()..scale(-1.0, -1.0),
                    child: Image.asset('assets/hand_1.png', width: screenWidth * 0.2),
                  ),
                ],
              ),
            ),

            // 残り時間
            Align(
              alignment: Alignment(0.82, -0.85),
              child: Transform(
                alignment: Alignment.center,
                transform: Matrix4.identity()..scale(-1.0, -1.0),
                child: Text(
                  '15',
                  style: TextStyle(
                    fontSize: screenHeight * 0.1,
                    fontWeight: FontWeight.w100,
                    color: const Color.fromARGB(255, 125, 125, 125),
                    fontFamily: 'font',
                  ),
                ),
              ),
            ),

            // Homeボタン
            Align(
              alignment: Alignment(-0.85,-0.3),
              child: GestureDetector(
                onTap: () {
                  Navigator.pop(context); // 戻る
                },
                child: Transform(
                  alignment: Alignment.center,
                  transform: Matrix4.identity()..scale(-1.0, -1.0), // 上下左右反転
                  child: Image.asset(
                    'assets/home.png',
                    height: screenHeight * 0.2,
                  ),
                ),
              ),
            ),
          
            
            // この手で決定ボタン
            Align(
              alignment: Alignment(0.93, -0.3),
              child: GestureDetector(
                onTap: () {
                  print("次へボタンが押されました");
                },
                child: Transform(
                  alignment: Alignment.center,
                  transform: Matrix4.identity()..scale(-1.0, -1.0), // 上下左右反転
                  child: Image.asset(
                    'assets/next_turn.png',
                    height: screenHeight * 0.2,
                  ),
                ),
              ),
            ),

            Align(
              alignment: Alignment(-0.93, -0.8),
              child: Transform(
                alignment: Alignment.center,
                transform: Matrix4.identity()..scale(-1.0, -1.0), // 上下左右反転
                child: Text(
                  'あなたのターン',
                  style: TextStyle(
                  fontSize: screenHeight * 0.05,
                    fontWeight: FontWeight.w100,
                    color: const Color.fromARGB(255, 125, 125, 125),
                    fontFamily: 'font',
                  ),
                ),
              ),
            ), 
          
          ],
        ),
      ),
    );
  }
}