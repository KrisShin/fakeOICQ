import 'package:flutter/material.dart';
import 'LoginPage.dart';
import 'HomePage.dart';

void main() => runApp(MyApp());

var routes = {
  '/': (context) => LoginPage(),
  '/home': (context) => HomePage(),
};

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    print("object");
    return MaterialApp(
      title: 'Flutter 登录页面示例',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: routes,
    );
  }
}
