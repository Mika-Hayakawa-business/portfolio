// main.dart
import 'package:flutter/material.dart';
import 'rule_page.dart';
import 'play_2.dart';

void main() => runApp(NamoAsoApp());

class NamoAsoApp extends StatefulWidget {
  NamoAsoState createState() => NamoAsoState();
}

class NamoAsoState extends State<NamoAsoApp> {
  Widget build(BuildContext context) {
    double screenheight = MediaQuery.of(context).size.height;
    double screenwidth = MediaQuery.of(context).size.width;

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Container(
          //背景
          decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage('assets/background_rainbow.jpg'),
              fit: BoxFit.cover, //画面全体に表示
            ),
          ),
          // Topの画像
          child: Stack(
            children: [
              Align(
                alignment: Alignment(1, -1),
                child: Builder(
                  builder:
                      (context) => GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => RulePage()),
                          );
                        },
                        child: Image.asset(
                          'assets/rule.png',
                          width: screenwidth * 0.1,
                        ),
                      ),
                ),
              ),
              Align(
                alignment: Alignment(-0.05, -0.7), // 中央に配置
                child: Image.asset(
                  'assets/main_logo.png',
                  height: screenheight * 0.6,
                ),
              ),
              Align(
                alignment: Alignment(-0.9, 0.9),
                child: Builder(
                  builder: (innerContext) {
                    return _TapTwoPlay(
                      'assets/play_2.png',
                      screenwidth * 0.2,
                      innerContext,
                    );
                  },
                ),
              ),
              Align(
                alignment: Alignment(-0.3, 0.9),
                child: _TapEasyPlay('assets/play_easy.png', screenwidth * 0.2),
              ),
              Align(
                alignment: Alignment(0.3, 0.9),
                child: _TapNormalPlay(
                  'assets/play_normal.png',
                  screenwidth * 0.2,
                ),
              ),
              Align(
                alignment: Alignment(0.9, 0.9),
                child: _TapHardPlay('assets/play_hard.png', screenwidth * 0.2),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

Widget _TapTwoPlay(String assetPath, double width, BuildContext context) {
  return GestureDetector(
    onTap: () {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => Namoaso_2()),
      );
    },
    child: Image.asset(assetPath, width: width),
  );
}

Widget _TapEasyPlay(String assetPath, double width) {
  return GestureDetector(
    onTap: () {
      print('EasyPlay tapped!');
    },
    child: Image.asset(assetPath, width: width),
  );
}

Widget _TapNormalPlay(String assetPath, double width) {
  return GestureDetector(
    onTap: () {
      print('NormalPlay tapped!');
    },
    child: Image.asset(assetPath, width: width),
  );
}

Widget _TapHardPlay(String assetPath, double width) {
  return GestureDetector(
    onTap: () {
      print('HardPlay tapped!');
    },
    child: Image.asset(assetPath, width: width),
  );
}
