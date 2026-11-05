package jp.co.trainocate.answer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.answer.entity.User;
import jp.co.trainocate.answer.form.UserForm;
import jp.co.trainocate.answer.repository.UserRepository;

@Controller
public class LoginController {
	@Autowired
	private UserRepository userRepo;
	
	@GetMapping("/")
	public String showLoginView() {
		return "login_input";
	}
	
	@PostMapping("/login")
	public String login(UserForm userForm) {
		//ここに、empIdとPasswordのAnd検索を呼び出してください。戻り値は、User userです
		
		System.out.println(); //userを出力してください。
		
		//ここに、userがnullなら、"redirect:/" へreturnする条件文を書いてください。
		
		
		//その他なら、"main_page"へ遷移させてください。
		return "";
	}
	

	@GetMapping("/2")
	public String showLoginView2() {
		return "login_input2";
	}

	//Sessionを直接使う例
	@PostMapping("/login2")
	                              //HttpSessionを引数に入れてください
	public String loginSession(UserForm userForm) {
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		System.out.println(user);
		if (user == null) {
			return "redirect:/";
		}

		//sessionにuserを格納してください。キーは"userData"にしてください。

		return "main_page_session";
	}

	@GetMapping("/3")
	public String showLoginView3() {
		return "login_input3";
	}

	//Modelを使う例（SessionAttributes利用可能）
	@PostMapping("/login3")
	public String loginNormal(UserForm userForm, Model model) {
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		System.out.println(user);
		if (user == null) {
			return "redirect:/";
		}
		model.addAttribute("userData", user);
		return "main_page_session";
	}
	
	@GetMapping("/4")
	public String showLoginView4(UserForm userForm) {
		return "validation_login_input";
	}

	//入力チェック機能実装
	@PostMapping("/login4")
	
	//入力チェックに必要なアノテーションと引数を付けてください
	public String loginValidation(UserForm userForm) {
		
//もし、入力チェックにエラーがあったら、validation_login_inputにreturnさせる条件文を作成してください。
		
		
		return "main_page";
	}

	@GetMapping("/5")
	public String showLoginView5(UserForm userForm) {
		return "login_input_final";
	}
}
