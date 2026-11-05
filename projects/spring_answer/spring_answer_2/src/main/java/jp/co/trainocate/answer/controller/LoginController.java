package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class LoginController {

	//Spring環境では、htmlページを直接より、
	//遷移用のメソッドを経由する方法が一般的です

	@GetMapping("/login")
	public String showLoginView() {
		return "login_input";
	}

	//同じ「login」というURLでも、
	//GetかPostかによって、異なるメソッドが実行されます
	@PostMapping("/login")
	public String doLogin(int id, String password) {
		//仮引数を記載するだけで、自動的にデータが格納されます
		System.out.println(id);
		System.out.println(password);
		return "index";
	}
}
