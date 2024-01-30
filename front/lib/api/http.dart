import 'package:http/http.dart' as http;
import 'dart:convert';

class HttpService {
  static const String _baseUrl = "http://8.137.53.219:26798";

  // GET请求
  static Future<dynamic> get(String path,
      {Map<String, dynamic>? queryParameters}) async {
    final queryParams = queryParameters != null
        ? queryParameters.entries.map((e) => '${e.key}=${e.value}').join('&')
        : '';

    final url = Uri.parse('$_baseUrl/$path?$queryParams');

    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception(
            'Failed to load data with status code: ${response.statusCode}');
      }
    } on Exception catch (e) {
      print('Error: $e');
      rethrow;
    }
  }

  // POST请求
  static Future<dynamic> post(String path, dynamic body,
      {Map<String, String>? headers}) async {
    final url = Uri.parse('$_baseUrl$path');

    Map<String, String> mergedHeaders = {
      'Content-Type': 'application/json',
    };

    if (headers != null) mergedHeaders.addAll(headers);

    try {
      final response =
          await http.post(url, body: jsonEncode(body), headers: headers);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception(
            'Failed to post data with status code: ${response.statusCode}');
      }
    } on Exception catch (e) {
      print('Error: $e');
      rethrow;
    }
  }

  // POST Form
  static Future<dynamic> postForm(String path, dynamic body,
      {Map<String, String>? headers}) async {
    final url = Uri.parse('$_baseUrl$path');
    print(url);
    try {
      final response = await http.post(url, body: body, headers: headers);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception(
            'Failed to post data with status code: ${response.statusCode}');
      }
    } on Exception catch (e) {
      print('Error: $e');
    }
  }
}
