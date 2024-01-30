import 'package:flutter/material.dart';
import 'package:tdesign_flutter/tdesign_flutter.dart';

class HomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  static const List<Widget> _widgetOptions = <Widget>[
    Text('首页内容'),
    Text('消息内容'),
    Text('我的内容'),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        resizeToAvoidBottomInset: false,
        appBar: AppBar(
          title: Text('底部导航示例'),
        ),
        body: Center(
          // child: _widgetOptions.elementAt(_selectedIndex),
          child: MessageListPage(),
        ),
        bottomNavigationBar: BottomNavigationBar(
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: '消息',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.message),
              label: '联系人',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              label: '我的',
            ),
          ],
          currentIndex: _selectedIndex,
          selectedItemColor: const Color.fromRGBO(19, 72, 87, 1),
          onTap: _onItemTapped,
        ));
  }
}

class Message {
  String title;
  String body;
  String authorInitials;

  Message(
      {required this.title, required this.body, required this.authorInitials});
}

// 定义一个消息列表
final List<Message> messages = [
  Message(
    title: '消息1',
    body: '这是第一条消息的内容',
    authorInitials: 'A',
  ),
  Message(
    title: '消息2',
    body: '这是第二条消息的内容',
    authorInitials: 'B',
  ),
  // 添加更多消息...
];

// /消息列表页面
class MessageListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: messages.length, // 假设messages是一个预定义的消息数组
      itemBuilder: (BuildContext context, int index) {
        final message = messages[index];
        return ListTile(
          title: Text(message.title),
          subtitle: Text(message.body),
          leading: CircleAvatar(child: Text(message.authorInitials)),
        );
      },
    );
  }
}
