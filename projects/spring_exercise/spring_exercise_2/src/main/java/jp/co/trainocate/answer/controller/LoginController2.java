package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class LoginController2 {

	@GetMapping("/login2")
	public String showLoginView() {
		return "login_input2";
	}

	@PostMapping("/login2")
	public String doLogin(){ //【引数には、UserFormクラスを記載】
		
		System.out.println();
		              //【↑getIdメソッドを呼び出してください】)
		System.out.println();
		              //【↑getPasswordメソッドを呼び出してください】)
		return "index";
	}
}
