package jp.co.trainocate.enshu.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.repository.EmpRepository;

@Controller
public class LoginController {
	@Autowired
	private EmpRepository empRepo;

	//初期画面(ログインページ)へ遷移
	

//演習4.3 b. LoginControllerのshowLoginViewメソッドの引数に、Formクラスを入れてください。
	@GetMapping("/")
	public String showLoginView() {
		return "index";
	}

//演習4.1
	@PostMapping("/login") 
	public String login() { //←c. loginメソッドの引数を入れてください。

//d. IDとパスワードのAnd検索を行い、ユーザデータを取得してください。

//e. 取得したデータがnullなら、“login_fail.html”へ遷移させる条件文を書いてください。

		return "emp/index";
	}

//演習4.2
//a.上記のloginメソッドの引数に、セッションオブジェクトを追記してください。
//b. idとパスワードのAnd検索から取得したユーザデータをセッションに格納してください。

	
//演習4.3
//c.LoginControllerのloginメソッドの引数の部分を、入力チェックができるように修正してください。
//d. 入力にエラーがある場合は、ログイン画面へ戻すように条件文を入れてください。
}
