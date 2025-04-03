// rule_page.dart
import 'package:flutter/material.dart';

class RulePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('ルール')),
      body: Center(
        child: Text('ここにルールの説明を書くよ！', style: TextStyle(fontSize: 20)),
      ),
    );
  }
}
