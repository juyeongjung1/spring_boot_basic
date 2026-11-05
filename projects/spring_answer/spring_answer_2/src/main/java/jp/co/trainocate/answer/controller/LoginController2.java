package jp.co.trainocate.answer.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.answer.form.UserForm;

@Controller
public class LoginController2 {

	@GetMapping("/login2")
	public String showLoginView() {
		return "login_input2";
	}
	
	@PostMapping("/login2")
	public String doLogin(UserForm userForm) {
		//仮引数にFormクラスを記載するだけで、
		//自動的にデータがフィールドにセットされます
		System.out.println(userForm.getId());
		System.out.println(userForm.getPassword());
		return "index";
	}
}
