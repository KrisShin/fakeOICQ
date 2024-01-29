import 'package:flutter/material.dart';
// import 'package:http/http.dart' as http;
import 'api/http.dart';

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

    if (response) {
      print("登录成功");
      Navigator.pushNamed(context, "/home");
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
