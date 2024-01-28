import 'package:http/http.dart' as http;
import 'dart:convert';

class HttpRequest {
  late String baseUrl;

  HttpRequest() {
    // 设置默认的baseUrl
    this.baseUrl = "http://8.137.53.219:26798";
  }

  // HttpRequest(this.baseUrl);

  // 发送GET请求
  Future<Map<String, dynamic>> getRequest(String endpoint) async {
    var response = await http.get(Uri.parse('$baseUrl$endpoint'));

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

//发送POST请求
  Future<Map<String, dynamic>> post(String endpoint, Map<String, dynamic> body,
      {Map<String, String>? headers}) async {
    print('$baseUrl$endpoint');
    var response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      body: body,
      headers: headers,
    );
    print(response.statusCode.toString());
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to post data');
    }
  }

// 发送JSON格式的POST请求
  Future<Map<String, dynamic>> postRequestJson(
      String endpoint, Map<String, dynamic> body) async {
    print('$baseUrl$endpoint');
    var response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(body),
    );
    print(response.statusCode.toString());
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to post data');
    }
  }
}
