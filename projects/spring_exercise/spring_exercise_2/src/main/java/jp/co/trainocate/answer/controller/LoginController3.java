package jp.co.trainocate.answer.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.answer.form.UserForm;

@Controller
public class LoginController3 {

	@GetMapping("/login3")
	public String showLoginView() {
		return "login_input3";
	}
	
	@PostMapping("/login3")
	public String doLogin(UserForm userForm) { //modelを追加してください。
		
		//modelに、userFormのデータを格納
		
		return "login_success";
	}
}
