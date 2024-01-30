import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
import 'api/http.dart';
// import 'package:fluttertoast/fluttertoast.dart';
import 'package:tdesign_flutter/tdesign_flutter.dart';

class LoginPage extends StatelessWidget {
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  Future<void> _login(BuildContext context) async {
    String username = usernameController.text;
    String password = passwordController.text;

    // 发起POST请求
    var response = await HttpService.postForm('/api/user/token/', {
      'username': username,
      'password': password,
    });
    // .then((value) => {print(value), Navigator.pushNamed(context, "/home")});
    print("response: $response");

    if (response != null) {
      print("登录成功");
      Navigator.pushNamed(context, "/home");
      // Fluttertoast.showToast(
      //     msg: "This is Center Short Toast",
      //     toastLength: Toast.LENGTH_SHORT,
      //     gravity: ToastGravity.CENTER,
      //     timeInSecForIosWeb: 1,
      //     backgroundColor: Colors.red,
      //     textColor: Colors.white,
      //     fontSize: 16.0);

      // TDToast.showText('最多一行展示十个汉字宽度限制最多不超过三行文字', context: context);
    } else {
      print("登录失败");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('登录'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            TextFormField(
              controller: usernameController,
              decoration: InputDecoration(
                labelText: '账号',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 20),
            TextFormField(
              controller: passwordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: '密码',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                _login(context);
              },
              child: Text('登录'),
            ),
          ],
        ),
      ),
    );
  }
}
