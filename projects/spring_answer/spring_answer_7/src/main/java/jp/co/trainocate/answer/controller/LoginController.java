package jp.co.trainocate.answer.controller;

import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.SessionAttributes;

import jp.co.trainocate.answer.entity.User;
import jp.co.trainocate.answer.form.UserForm;
import jp.co.trainocate.answer.repository.UserRepository;

@Controller
@SessionAttributes("userData")
public class LoginController {
	@Autowired
	private UserRepository userRepo;

	@GetMapping("/")
	public String showLoginView() {
		return "login_input";
	}

	@PostMapping("/login")
	public String login(UserForm userForm) {
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		System.out.println(user); //検索結果がnullなら、再度ログイン画面へ
		if (user == null) {
			return "redirect:/";
		}
		return "main_page";
	}

	@GetMapping("/2")
	public String showLoginView2() {
		return "login_input2";
	}

	//Modelを使う例（SessionAttributes利用可能）
	@PostMapping("/login2")
	public String loginNormal(UserForm userForm, Model model) {
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		System.out.println(user);
		if (user == null) {
			return "redirect:/";
		}
		User userData = userRepo.findById(userForm.getEmpId()).orElse(null);
		model.addAttribute("userData", userData);
		return "main_page_session";
	}

	@GetMapping("/3")
	public String showLoginView3() {
		return "login_input3";
	}

	//Sessionを直接使う例
	@PostMapping("/login3")
	public String loginSession(UserForm userForm, HttpSession session) {
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		System.out.println(user);
		if (user == null) {
			return "redirect:/";
		}

		User userData = userRepo.findById(userForm.getEmpId()).orElse(null);
		session.setAttribute("userData", userData);

		return "main_page_session";
	}

	@GetMapping("/4")
	public String showLoginView4(UserForm userForm) {
		return "validation_login_input";
	}

	//入力チェック機能実装
	@PostMapping("/login4")
	public String loginValidation(@Valid UserForm userForm, BindingResult bdResult) {
		if (bdResult.hasErrors()) {
			System.out.println(userForm);
			return "validation_login_input"; //入力エラー発生時、入力ページへ戻る
		}
		return "main_page";
	}

	@GetMapping("/5")
	public String showLoginView5(UserForm userForm) {
		return "login_input_final";
	}

	@PostMapping("/login5")
	public String loginFinal(@Valid UserForm userForm, BindingResult bdResult, HttpSession session) {
		//入力エラーチェック
		if (bdResult.hasErrors()) {
			return "login_input_final";
		}
		
		User user = userRepo.findByEmpIdAndPassword(userForm.getEmpId(), userForm.getPassword());
		//DB照会後のID&パスワードのチェック
		if (user == null) {
			return "login_input_final";
		}

		//正しい入力の場合、ユーザ情報をセッションに格納
		User userData = userRepo.findById(userForm.getEmpId()).orElse(null);
		session.setAttribute("userData", userData);

		return "main_page_session";
	}
	
}
